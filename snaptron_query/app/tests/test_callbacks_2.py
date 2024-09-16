import dash.exceptions
import pytest

from snaptron_query.app import inline_styles, exceptions, global_strings as gs
from snaptron_query.app.exceptions import alert_message_from_exception


@pytest.mark.parametrize(
    "n_clicks,is_open,result",
    [
        (1, True, False),
        (1, False, True),
        (0, True, True),
        (0, False, False),
    ],
)
def test_on_image_click(monkeypatch_meta_data, n_clicks, is_open, result):
    from snaptron_query.app.main_dash_app import on_image_click_jiq, on_image_click_geq

    assert on_image_click_jiq(n_clicks, is_open) == result
    assert on_image_click_geq(n_clicks, is_open) == result


def test_on_button_click_jiq_clear(monkeypatch_meta_data):
    # this test needs to mock the callback context
    from contextvars import copy_context
    from dash._callback_context import context_value
    from dash._utils import AttributeDict
    from snaptron_query.app.main_dash_app import on_button_click_jiq_clear

    def run_callback():
        context_value.set(
            AttributeDict(**{"triggered_inputs": [{"prop_id": "id-button-jiq-generate-results.n_clicks"}]})
        )
        return on_button_click_jiq_clear(1, False)

    ctx = copy_context()
    output = ctx.run(run_callback)
    assert output[0] == []
    assert output[1] == inline_styles.display_none
    assert output[2] == inline_styles.display_none
    assert output[3]


def test_on_button_click_jiq_clear_error(monkeypatch_meta_data):
    # this test needs to mock the callback context
    from contextvars import copy_context
    from dash._callback_context import context_value
    from dash._utils import AttributeDict
    from snaptron_query.app.main_dash_app import on_button_click_jiq_clear

    def run_callback():
        context_value.set(
            AttributeDict(**{"triggered_inputs": [{"prop_id": "id-button-jiq-generate-results-typo.n_clicks"}]})
        )
        return on_button_click_jiq_clear(1, False)

    ctx = copy_context()
    with pytest.raises(dash.exceptions.PreventUpdate):
        ctx.run(run_callback)


def test_on_button_click_geq_clear(monkeypatch_meta_data):
    # this test needs to mock the callback context
    from contextvars import copy_context
    from dash._callback_context import context_value
    from dash._utils import AttributeDict
    from snaptron_query.app.main_dash_app import on_button_click_geq_clear

    def run_callback():
        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": "id-button-geq-run-query.n_clicks"}]}))
        return on_button_click_geq_clear(1, False)

    ctx = copy_context()
    output = ctx.run(run_callback)
    assert output[0] == []
    assert output[1] == inline_styles.display_none
    assert output[2] == inline_styles.display_none
    assert output[3]


def test_on_button_click_geq_clear_error(monkeypatch_meta_data):
    # this test needs to mock the callback context
    from contextvars import copy_context
    from dash._callback_context import context_value
    from dash._utils import AttributeDict
    from snaptron_query.app.main_dash_app import on_button_click_geq_clear

    def run_callback():
        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": "id-button-geq-run-query.n_clicks"}]}))
        return on_button_click_geq_clear(1, True)

    ctx = copy_context()
    with pytest.raises(dash.exceptions.PreventUpdate):
        ctx.run(run_callback)


@pytest.mark.parametrize(
    "exc,msg",
    [
        (exceptions.BadURL, gs.bad_url),
        (exceptions.EmptyResponse, gs.empty_response),
        (exceptions.MissingUserInputs, gs.missing_user_input),
        (exceptions.BadCoordinates, gs.bad_coordinates),
        (exceptions.QueryGeneNotFound, gs.query_gene_not_found),
        (exceptions.NormalizationGeneNotFound, gs.normalization_gene_not_found),
    ],
)
def test_alerts(exc, msg):
    try:
        raise exc
    except exc as e:
        assert alert_message_from_exception(e) == msg


def test_alert_httpx():
    import httpx

    try:
        raise httpx.RemoteProtocolError("random error")
    except httpx.RemoteProtocolError as e:
        assert alert_message_from_exception(e) == gs.httpx_remote_protocol_error


def test_alert_httpx_2():
    import httpx

    try:
        raise httpx.ConnectError("random error")
    except httpx.ConnectError as e:
        assert alert_message_from_exception(e) == gs.httpx_connect_error


def test_alert_not9_covered():
    assert len(alert_message_from_exception("some_exception")) != 0
