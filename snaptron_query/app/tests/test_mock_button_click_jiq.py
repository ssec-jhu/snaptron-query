import dash.exceptions
import pytest
from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict
from dash import no_update
import dash_bootstrap_components as dbc

import snaptron_query.app.global_strings as gs
from snaptron_query.app.snaptron_client import JunctionCoordinates


def run_callback(sample_ui_children):
    # keep the import of main file contained here
    from snaptron_query.app.main_dash_app import on_button_click_jiq_run

    context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": "id-results-cleared-jiq.n_clicks"}]}))
    return on_button_click_jiq_run(
        n_clicks=1,
        results_are_cleared=True,
        compilation=gs.compilation_srav3h,
        children=sample_ui_children,
        junction_count=1,  # not important for this at all as get_element_id_and_value() is mocked
        box_log_psi=True,
        violin_overlay=False,
        histogram_log_psi=True,
        histogram_log_y=False,
    )


@pytest.fixture()
def mock_get_snpt_results(mocker, df_sample_junctions_from_srav3h):
    # mock the httpx return results
    mock = mocker.patch("snaptron_query.app.snaptron_client.gather_snpt_query_results_into_dict")
    mock.return_value = {JunctionCoordinates(chr="chr19", start=4491836, end=4493702): df_sample_junctions_from_srav3h}
    return mock


@pytest.fixture()
def mock_get_element_id_and_value(mocker, df_sample_junctions_from_srav3h):
    mock = mocker.patch("snaptron_query.app.utils.get_element_id_and_value")
    inc_junctions = ["chr19:4491836-4492014"]
    exc_junctions = ["chr19:4491836-4493702"]
    mock.return_value = (inc_junctions, exc_junctions)
    return mock


@pytest.fixture()
def mock_get_element_id_and_value_missing_junction(mocker, df_sample_junctions_from_srav3h):
    mock = mocker.patch("snaptron_query.app.utils.get_element_id_and_value")
    inc_junctions = []
    exc_junctions = ["chr19:4491836-4493702"]
    mock.return_value = (inc_junctions, exc_junctions)
    return mock


@pytest.fixture()
def mock_get_element_id_and_value_multi_junction(mocker, df_sample_junctions_from_srav3h):
    mock = mocker.patch("snaptron_query.app.utils.get_element_id_and_value")
    inc_junctions = ["chr19:4491836-4492014", "chr19:4492153-4493702"]
    exc_junctions = ["chr19:4491836-4493702", "chr19:4491836-4493702"]

    mock.return_value = (inc_junctions, exc_junctions)

    return mock


@pytest.fixture()
def mock_get_element_id_and_value_multi_junction_not_found_inc_junction(mocker, df_sample_junctions_from_srav3h):
    mock = mocker.patch("snaptron_query.app.utils.get_element_id_and_value")
    inc_junctions = ["chr19:4491836-4492014", "chr19:4492153-4493722"]  # inclusion junction[1] is a made up number
    exc_junctions = ["chr19:4491836-4493702", "chr19:4491836-4493702"]

    mock.return_value = (inc_junctions, exc_junctions)

    return mock


def test_mock_on_button_click_jiq_run(
    sample_ui_children, monkeypatch_meta_data, mock_get_snpt_results, mock_get_element_id_and_value
):
    ctx = copy_context()
    output = ctx.run(run_callback, sample_ui_children)
    assert len(output) == 12
    assert len(output[1]) == 2000
    assert output[5] == no_update  # no alerts were given


def test_mock_on_button_click_jiq_run_missing_input(
    sample_ui_children, monkeypatch_meta_data, mock_get_snpt_results, mock_get_element_id_and_value_missing_junction
):
    ctx = copy_context()
    output = ctx.run(run_callback, sample_ui_children)
    assert len(output) == 12
    assert isinstance(output[5][1], dbc.Alert)  # alerts was given


def test_mock_on_button_click_jiq_run_not_found_input_junction(
    sample_ui_children,
    monkeypatch_meta_data,
    mock_get_snpt_results,
    mock_get_element_id_and_value_multi_junction_not_found_inc_junction,
):
    ctx = copy_context()
    output = ctx.run(run_callback, sample_ui_children)
    assert len(output) == 12
    assert isinstance(output[5][1], dbc.Alert)  # alerts was given


def test_mock_on_button_click_jiq_run_multi_junction(
    sample_ui_children, monkeypatch_meta_data, mock_get_snpt_results, mock_get_element_id_and_value_multi_junction
):
    ctx = copy_context()
    output = ctx.run(run_callback, sample_ui_children)
    assert len(output) == 12


def test_mock_on_button_click_jiq_run_callback_with_incorrect_trigger(sample_ui_children, monkeypatch_meta_data):
    def run_callback_with_errors():
        from snaptron_query.app.main_dash_app import on_button_click_jiq_run

        # input trigger to the function is incorrect.
        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": "id-results-cleared-jiq-typo.n_clicks"}]}))
        return on_button_click_jiq_run(
            n_clicks=1,
            results_are_cleared=True,
            compilation=gs.compilation_srav3h,
            children=sample_ui_children,
            junction_count=1,
            box_log_psi=True,
            violin_overlay=False,
            histogram_log_psi=True,
            histogram_log_y=False,
        )

    ctx = copy_context()
    with pytest.raises(dash.exceptions.PreventUpdate):
        ctx.run(run_callback_with_errors)


def test_mock_on_button_click_jiq_run_callback_missing_compilation(sample_ui_children, monkeypatch_meta_data):
    def run_callback_with_errors():
        from snaptron_query.app.main_dash_app import on_button_click_jiq_run

        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": "id-results-cleared-jiq.n_clicks"}]}))
        return on_button_click_jiq_run(
            n_clicks=1,
            results_are_cleared=True,
            compilation="",
            children=sample_ui_children,
            junction_count=1,
            box_log_psi=True,
            violin_overlay=False,
            histogram_log_psi=True,
            histogram_log_y=False,
        )

    ctx = copy_context()
    output = ctx.run(run_callback_with_errors)
    assert len(output) == 12
    assert isinstance(output[5][1], dbc.Alert)  # alerts was given


def test_mock_on_button_click_jiq_run_callback_junction_zero(sample_ui_children, monkeypatch_meta_data):
    def run_callback_with_errors():
        from snaptron_query.app.main_dash_app import on_button_click_jiq_run

        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": "id-results-cleared-jiq.n_clicks"}]}))
        return on_button_click_jiq_run(
            n_clicks=1,
            results_are_cleared=True,
            compilation=gs.compilation_srav3h,
            children=sample_ui_children,
            junction_count=None,
            box_log_psi=True,
            violin_overlay=False,
            histogram_log_psi=True,
            histogram_log_y=False,
        )

    ctx = copy_context()
    output = ctx.run(run_callback_with_errors)
    assert len(output) == 12
