import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pytest
from dash import html
from dash import no_update

from snaptron_query.app import column_defs, callback_common, global_strings as gs, inline_styles, components


@pytest.mark.parametrize(
    "string, result",
    [(gs.snpt_col_rail_id, "Rail_Id"), (gs.snpt_col_external_id, "External_Id")],
)
def test_capitalize_underscored_string(string, result):
    assert result == column_defs.capitalize_underscored_string(string)


def test_get_rail_id():
    assert column_defs.get_rail_id()[0]["field"] == gs.snpt_col_rail_id
    assert column_defs.get_col_meta_tcgav2_a()[0]["field"] == gs.snpt_col_rail_id
    assert column_defs.get_col_meta_gtexv2_a()[0]["field"] == gs.snpt_col_rail_id


def test_get_study():
    assert column_defs.get_study()[0]["field"] == "study"


def test_get_col_meta_srav3h_a():
    assert column_defs.get_col_meta_srav3h_a()[0]["field"] == gs.snpt_col_rail_id
    assert column_defs.get_col_meta_srav3h_a()[1]["field"] == gs.snpt_col_external_id
    assert column_defs.get_col_meta_srav3h_a()[2]["field"] == "study"


def test_get_col_meta_srav3h_b():
    assert column_defs.get_col_meta_srav3h_b()[0]["field"] == "study_title"


def test_get_col_meta_gtexv2_b():
    assert column_defs.get_col_meta_gtexv2_b()[0]["field"] == "run_acc"


@pytest.mark.parametrize(
    "compilation, junction_count, index",
    [
        (gs.compilation_srav3h, 2, 4),
        (gs.compilation_srav3h, 3, 4),
        (gs.compilation_srav3h, 4, 4),
        (gs.compilation_gtexv2, 2, 2),
        (gs.compilation_gtexv2, 3, 2),
        (gs.compilation_gtexv2, 4, 2),
        (gs.compilation_tcgav2, 2, 2),
        (gs.compilation_tcgav2, 3, 2),
        (gs.compilation_tcgav2, 4, 2),
        (gs.compilation_srav1m, 2, 4),
        (gs.compilation_srav1m, 3, 4),
        (gs.compilation_srav1m, 4, 4),
    ],
)
def test_get_junction_query_column_def(compilation, junction_count, index):
    columns = column_defs.get_junction_query_column_def(compilation, junction_count)
    assert columns[index]["field"] == "psi_1"


@pytest.mark.parametrize(
    "compilation, normalized,index",
    [
        (gs.compilation_srav3h, True, 3),
        (gs.compilation_srav3h, False, 3),
        (gs.compilation_gtexv2, True, 1),
        (gs.compilation_gtexv2, False, 1),
        (gs.compilation_tcgav2, True, 1),
        (gs.compilation_tcgav2, False, 1),
        (gs.compilation_srav1m, True, 3),
        (gs.compilation_srav1m, False, 3),
    ],
)
def test_get_gene_expression_query_column_def(compilation, normalized, index):
    c = column_defs.get_gene_expression_query_column_def(compilation, normalized)
    assert c[index]["field"] == gs.table_geq_col_raw_count


@pytest.mark.parametrize(
    "junction_count, column, r",
    [
        (1, gs.table_jiq_col_total, 15),
        (1, gs.table_jiq_col_psi, 5),
        (3, gs.table_jiq_col_avg_psi, 5),
    ],
)
def test_get_jiq_table_filter_model(junction_count, column, r):
    assert column_defs.get_jiq_table_filter_model(junction_count)[column]["filter"] == r


@pytest.mark.parametrize(
    "norm, column, r",
    [
        (True, gs.table_geq_col_factor, 0),
    ],
)
def test_get_geq_table_filter_model(norm, column, r):
    assert column_defs.get_geq_table_filter_model(norm)[column]["filter"] == r


@pytest.mark.parametrize(
    "index, name",
    [
        (0, gs.table_jiq_col_inc),
        (1, gs.table_jiq_col_exc),
        (2, gs.table_jiq_col_total),
    ],
)
def test_get_col_jiq(index, name):
    assert column_defs.get_col_jiq()[index]["field"] == name


def test_on_box_plot_click():
    # TODO: get a click data instance and add to test
    assert callback_common.on_box_plot_click(None, None) == no_update


@pytest.mark.parametrize(
    "click_data, result",
    [
        (None, no_update),
        ("anything", {}),
    ],
)
def test_rest_table(click_data, result):
    assert callback_common.on_reset_table(click_data) == result


@pytest.mark.parametrize(
    "lock, result",
    [
        (True, inline_styles.inactive_lock),
        (False, inline_styles.active_lock),
    ],
)
def test_on_lock_switch(lock, result):
    assert callback_common.on_lock_switch(lock)[0] == result


@pytest.mark.parametrize(
    "option, string",
    [
        (components.DownloadType.FILTERED.value, "filteredAndSorted"),
        (components.DownloadType.ORIGINAL.value, "all"),
    ],
)
def test_export(option, string):
    filename = callback_common.export_data_as_csv(option, "test_file")[1]["fileName"]
    assert filename.find(string) != -1


def test_switch_lock_data_with_table():
    assert len(components.get_switch_lock_data_with_table("id", "id2", "id3")) > 0


def test_switch_box_plot_points():
    assert len(components.get_switch_box_plot_points("id")) > 0


def test_get_alert():
    assert len(components.get_alert("id")) > 0


def test_get_button_download():
    assert len(components.get_button_download("id")) > 0


def test_get_radio_items_download_options():
    assert len(components.get_radio_items_download_options("id")) > 0


def test_get_button_reset():
    assert len(components.get_button_reset("id")) > 0


def test_get_text():
    assert isinstance(components.get_text("string"), dmc.Text)


def test_get_input():
    assert isinstance(components.get_input("placeholder", "id"), dbc.Input)


def test_get_dropdown_compilation():
    assert isinstance(components.get_dropdown_compilation("id"), html.Div)


def test_get_button_run_query():
    assert isinstance(components.get_button_run_query("id", "string"), dbc.Button)


def test_get_switch():
    assert isinstance(components.get_switch("id", "label"), dbc.Switch)


def test_get_table():
    assert isinstance(components.get_table("id"), dag.AgGrid)


def test_get_tooltip():
    assert isinstance(components.get_tooltip("id", "string", "tip"), dbc.Tooltip)


def test_get_info_icon_tooltip_bundle():
    assert isinstance(components.get_info_icon_tooltip_bundle("id", "string", "location"), html.Div)
