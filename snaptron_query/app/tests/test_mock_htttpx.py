from unittest.mock import MagicMock
import pytest
import httpx
import pandas as pd


from snaptron_query.app import exceptions
from snaptron_query.app.snaptron_client import (
    get_snpt_query_results_df,
    gather_snpt_query_results_into_dict,
    SpliceJunctionPair,
    JunctionCoordinates,
)


@pytest.fixture
def mock_httpx_get(mocker):
    """
    Fixture to mock httpx.get requests.
    """
    return mocker.patch("httpx.get")


@pytest.fixture
def mock_httpx_response_data(mock_httpx_get):
    """
    Fixture to mock a response
    """
    # Mock response content
    mock_data = "col1\tcol2\nval1\tval2"
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.read.return_value = mock_data.encode()  # Mocking read() to return bytes

    return mock_response


@pytest.fixture
def mock_httpx_response_empty(mock_httpx_get):
    """
    Fixture to mock a response
    """
    # empty response
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.read.return_value = b""  # Empty bytes

    return mock_response


@pytest.fixture
def mock_httpx_response_error(mock_httpx_get):
    """
    Fixture to mock a response
    """
    # empty response
    # Mock response that raises an HTTP error
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Error", request=MagicMock(), response=MagicMock()
    )

    return mock_response


@pytest.fixture
def mock_df_snpt_results_dict_empty(mocker):
    """
    Fixture to mock a response
    """
    # empty response
    mock = mocker.patch("snaptron_query.app.snaptron_client.get_snpt_query_results_df")
    mock.return_value = pd.DataFrame()  # empty data frame
    return mock


# need to have pytest-mock installed
def test_get_snpt_query_results_df(mock_httpx_get, mock_httpx_response_data):
    # Set our mock object as the return value of httpx.get
    mock_httpx_get.return_value = mock_httpx_response_data

    # Call the function under test
    df = get_snpt_query_results_df("compilation", "region", "query_mode")

    # Verify the returned DataFrame
    expected_df = pd.DataFrame({"col1": ["val1"], "col2": ["val2"]})
    pd.testing.assert_frame_equal(df, expected_df)


def test_get_snpt_query_results_df_empty(mock_httpx_get, mock_httpx_response_empty):
    # Set our mock object as the return value of httpx.get
    mock_httpx_get.return_value = mock_httpx_response_empty

    # Call the function under test
    with pytest.raises(exceptions.EmptyResponse):
        get_snpt_query_results_df("compilation", "region", "query_mode")


def test_get_snpt_query_results_df_error(mock_httpx_get, mock_httpx_response_error):
    # Set our mock object as the return value of httpx.get
    mock_httpx_get.return_value = mock_httpx_response_error

    # Call the function under test
    with pytest.raises(httpx.HTTPStatusError):
        get_snpt_query_results_df("compilation", "region", "query_mode")


def test_gather_snpt_query_results_into_dict(mock_httpx_get, mock_httpx_response_data):
    # Set our mock object as the return value of httpx.get
    mock_httpx_get.return_value = mock_httpx_response_data

    junction_list = [
        SpliceJunctionPair(
            exc_coordinates=JunctionCoordinates(chr="chr19", start=4491836, end=4493702),
            inc_coordinates=JunctionCoordinates(chr="chr19", start=4491836, end=4492014),
        ),
        SpliceJunctionPair(
            exc_coordinates=JunctionCoordinates(chr="chr19", start=4491836, end=4493702),
            inc_coordinates=JunctionCoordinates(chr="chr19", start=4492153, end=4493702),
        ),
    ]

    snpt_results_dict = gather_snpt_query_results_into_dict("compilation", junction_list)

    # exclusion junction is duplicate so it must be 1
    assert len(snpt_results_dict) == 1


def test_gather_snpt_query_results_into_dic_exception(mock_httpx_get, mock_httpx_response_empty):
    # Set our mock object as the return value of httpx.get
    mock_httpx_get.return_value = mock_httpx_response_empty

    junction_list = [
        SpliceJunctionPair(
            exc_coordinates=JunctionCoordinates(chr="chr19", start=4491836, end=4493702),
            inc_coordinates=JunctionCoordinates(chr="chr19", start=4491836, end=4492014),
        ),
    ]

    with pytest.raises(exceptions.EmptyResponse):
        gather_snpt_query_results_into_dict("compilation", junction_list)


def test_gather_snpt_query_results_into_dic_exception_2(mock_httpx_get, mock_df_snpt_results_dict_empty):
    # this exception is raised in the function itself not in get_snpt_query_results_df

    junction_list = [
        SpliceJunctionPair(
            exc_coordinates=JunctionCoordinates(chr="chr19", start=4491836, end=4493702),
            inc_coordinates=JunctionCoordinates(chr="chr19", start=4491836, end=4492014),
        ),
    ]

    with pytest.raises(exceptions.EmptyResponse):
        gather_snpt_query_results_into_dict("compilation", junction_list)
