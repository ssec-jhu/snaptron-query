import pytest
from dash import no_update
from dash.exceptions import PreventUpdate

from snaptron_query.app import components, global_strings as gs


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
    "junction_counts,",
    [1, 2, 3, 4],
)
def test_update_junction_inputs(monkeypatch_meta_data, junction_counts):
    from snaptron_query.app.main_dash_app import update_junction_inputs

    assert update_junction_inputs(1, junction_counts)[junction_counts - 1]["display"] == "flex"


def test_update_junction_inputs_exception(monkeypatch_meta_data):
    from snaptron_query.app.main_dash_app import update_junction_inputs

    with pytest.raises(PreventUpdate):
        update_junction_inputs(1, 5)


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
