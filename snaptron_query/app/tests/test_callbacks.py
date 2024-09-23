import pytest
import dash.exceptions
from dash import no_update
from dash.exceptions import PreventUpdate

from snaptron_query.app import components, inline_styles, exceptions, global_strings as gs
from snaptron_query.app.exceptions import alert_message_from_exception


@pytest.mark.parametrize(
    "lock,index,value",
    [
        (0, 0, {"color": "var(--bs-primary)"}),
        (0, 1, {"color": "var(--bs-gray-400)"}),
        (1, 1, {"color": "var(--bs-primary)"}),
        (1, 0, {"color": "var(--bs-gray-400)"}),
    ],
)
def test_on_lock_switch_geq_callback(monkeypatch_meta_data, lock, index, value):
    # import here on purpose to control the flow of the mock fixture before the imports
    from snaptron_query.app.main_dash_app import on_lock_switch_geq, on_lock_switch_jiq

    assert on_lock_switch_geq(lock)[index] == value
    assert on_lock_switch_jiq(lock)[index] == value


@pytest.mark.parametrize(
    "click_data, value",
    [
        (1, {}),
        (0, no_update),
    ],
)
def test_on_reset_table_callback(monkeypatch_meta_data, click_data, value):
    from snaptron_query.app.main_dash_app import on_reset_table_jiq, on_reset_table_geq

    assert on_reset_table_jiq(click_data) == value
    assert on_reset_table_geq(click_data) == value


def test_on_box_plot_click(monkeypatch_meta_data):
    from snaptron_query.app.main_dash_app import on_box_plot_click_geq, on_box_plot_click_jiq

    assert on_box_plot_click_geq(0, {}) == no_update
    assert on_box_plot_click_jiq(0, {}) == no_update


@pytest.mark.parametrize(
    "option",
    [
        components.DownloadType.FILTERED.value,
        components.DownloadType.ORIGINAL.value,
    ],
)
def test_export_as_csv_geq(monkeypatch_meta_data, option):
    from snaptron_query.app.main_dash_app import export_data_as_csv_geq

    r = export_data_as_csv_geq(1, option)
    assert r[0]
    assert r[1]["fileName"].endswith(".csv")


@pytest.mark.parametrize(
    "option",
    [
        components.DownloadType.FILTERED.value,
        components.DownloadType.ORIGINAL.value,
    ],
)
def test_export_as_csv_jiq(monkeypatch_meta_data, option):
    from snaptron_query.app.main_dash_app import export_data_as_csv_jiq

    r = export_data_as_csv_jiq(1, option)
    assert r[0]
    assert r[1]["fileName"].endswith(".csv")


@pytest.mark.parametrize(
    "normalize_value,index,result",
    [(True, 0, False), (True, 1, False), (False, 0, True), (False, 1, True)],
)
def test_enable_normalization(monkeypatch_meta_data, normalize_value, index, result):
    from snaptron_query.app.main_dash_app import enable_normalization

    assert enable_normalization(normalize_value)[index] == result


@pytest.mark.parametrize(
    "use_coordinates,index,result",
    [(True, 0, "block"), (True, 1, "block"), (False, 0, "none"), (False, 1, "none")],
)
def test_enable_coordinate_inputs(monkeypatch_meta_data, use_coordinates, index, result):
    from snaptron_query.app.main_dash_app import enable_coordinate_inputs

    assert enable_coordinate_inputs(use_coordinates)[index]["display"] == result


@pytest.mark.parametrize(
    "junction_counts,index,value",
    [
        # one default junction
        (0, 0, "none"),
        (0, 1, "none"),
        (0, 2, "none"),
        (0, 3, "none"),
        (0, 4, "none"),
        (0, 5, "none"),
        (0, 6, "none"),
        (0, 7, "none"),
        (0, 8, "none"),
        (0, 9, "none"),
        (0, 10, "none"),
        (0, 11, "none"),
        # one junction added
        (1, 0, "flex"),  # junction rows
        (1, 1, "none"),
        (1, 2, "none"),
        (1, 3, "none"),
        (1, 4, "flex"),  # del button
        (1, 5, "none"),
        (1, 6, "none"),
        (1, 7, "none"),
        (1, 8, "block"),  # tip
        (1, 9, "none"),
        (1, 3, "none"),
        (1, 10, "none"),
        (1, 11, "none"),
        # two junctions added
        (2, 0, "flex"),  # junction rows
        (2, 1, "flex"),
        (2, 2, "none"),
        (2, 3, "none"),
        (2, 4, "none"),  # del button
        (2, 5, "flex"),
        (2, 6, "none"),
        (2, 7, "none"),
        (2, 8, "none"),
        (2, 9, "block"),
        (2, 10, "none"),
        (2, 11, "none"),
        # 3 junctions
        (3, 0, "flex"),  # junction rows
        (3, 1, "flex"),
        (3, 2, "flex"),
        (3, 3, "none"),
        (3, 4, "none"),  # del button
        (3, 5, "none"),
        (3, 6, "flex"),
        (3, 7, "none"),
        (3, 8, "none"),
        (3, 9, "none"),
        (3, 10, "block"),
        (3, 11, "none"),
        # # 4 junctions
        (4, 0, "flex"),  # junction rows
        (4, 1, "flex"),
        (4, 2, "flex"),
        (4, 3, "flex"),
        (4, 4, "none"),
        (4, 5, "none"),  # del button
        (4, 6, "none"),
        (4, 7, "flex"),
        (4, 8, "none"),
        (4, 9, "none"),
        (4, 10, "none"),
        (4, 11, "block"),
    ],
)
def test_update_junction_inputs(monkeypatch_meta_data, junction_counts, index, value):
    from snaptron_query.app.main_dash_app import update_junction_inputs

    ret = update_junction_inputs(1, junction_counts, {}, {}, {}, {})
    assert ret[index]["display"] == value


def test_update_junction_inputs_exception(monkeypatch_meta_data):
    from snaptron_query.app.main_dash_app import update_junction_inputs

    with pytest.raises(PreventUpdate):
        update_junction_inputs(1, 5, {}, {}, {}, {})


@pytest.mark.parametrize(
    "junction_counts,result",
    [(None, 0), (1, 2), (2, 3), (3, 4), (4, 5)],
)
def test_on_add_junction_click(monkeypatch_meta_data, junction_counts, result):
    from snaptron_query.app.main_dash_app import on_add_junction_click

    assert on_add_junction_click(1, junction_counts) == result
    assert on_add_junction_click(0, junction_counts) == result


def test_on_add_junction_click_exception(monkeypatch_meta_data):
    from snaptron_query.app.main_dash_app import on_add_junction_click

    with pytest.raises(PreventUpdate):
        on_add_junction_click(1, 6)


@pytest.mark.parametrize(
    "junction_counts,result",
    [(None, 0), (1, 0), (2, 1), (3, 2), (4, 3), (5, 4)],
)
def test_on_delete_junction_click(monkeypatch_meta_data, junction_counts, result):
    from snaptron_query.app.main_dash_app import on_delete_junction_click

    assert on_delete_junction_click(1, 0, 0, 0, junction_counts) == result
    assert on_delete_junction_click(0, 0, 0, 0, junction_counts) == result


def test_on_delete_junction_click_exception(monkeypatch_meta_data):
    from snaptron_query.app.main_dash_app import on_delete_junction_click

    with pytest.raises(PreventUpdate):
        on_delete_junction_click(1, 0, 0, 0, 0)


@pytest.mark.parametrize(
    "compilation",
    [
        gs.compilation_srav3h,
        gs.compilation_gtexv2,
        gs.compilation_tcgav2,
        gs.compilation_srav1m,
    ],
)
def test_get_meta_data(monkeypatch_meta_data, compilation):
    """ "
    path to the metadata files has been mocked here to read the sample metadata file
    """
    from snaptron_query.app.main_dash_app import get_meta_data

    assert len(get_meta_data(compilation)) != 0


def test_get_meta_data_exception(monkeypatch_meta_data):
    with pytest.raises(PreventUpdate):
        from snaptron_query.app.main_dash_app import get_meta_data

        get_meta_data("unimportant-string")


def test_time_function():
    from snaptron_query.app import profile_timer

    test_timer = profile_timer.Timer("starting:test_time_function")
    test_timer.turn_on()
    test_timer.start()
    test_timer.split("split here")
    test_timer.split("split again")
    test_timer.stop("stopping:test_time_function")


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


def test_alert_not_covered():
    assert len(alert_message_from_exception("some_exception")) != 0
