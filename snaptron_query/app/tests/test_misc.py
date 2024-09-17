import os

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pytest
from dash import html
from dash import no_update

from snaptron_query.app import (
    column_defs,
    callback_common,
    global_strings as gs,
    inline_styles,
    components,
    exceptions,
    components_jiq,
    components_geq,
    navbars,
    layout_jiq,
    layout_geq,
    layout,
    paths,
)


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
        (1, gs.table_jiq_col_total, gs.const_filter_total),
        (1, gs.table_jiq_col_psi, gs.const_filter_psi),
        (2, gs.table_jiq_col_avg_psi, gs.const_filter_psi),
        (2, f"{gs.table_jiq_col_total}_1", gs.const_filter_total),
        (2, f"{gs.table_jiq_col_total}_2", gs.const_filter_total),
        (3, gs.table_jiq_col_avg_psi, gs.const_filter_psi),
        (3, f"{gs.table_jiq_col_total}_1", gs.const_filter_total),
        (3, f"{gs.table_jiq_col_total}_2", gs.const_filter_total),
        (3, f"{gs.table_jiq_col_total}_3", gs.const_filter_total),
        (4, gs.table_jiq_col_avg_psi, gs.const_filter_psi),
        (4, f"{gs.table_jiq_col_total}_1", gs.const_filter_total),
        (4, f"{gs.table_jiq_col_total}_2", gs.const_filter_total),
        (4, f"{gs.table_jiq_col_total}_3", gs.const_filter_total),
        (4, f"{gs.table_jiq_col_total}_4", gs.const_filter_total),
        (5, gs.table_jiq_col_avg_psi, gs.const_filter_psi),
        (5, f"{gs.table_jiq_col_total}_1", gs.const_filter_total),
        (5, f"{gs.table_jiq_col_total}_2", gs.const_filter_total),
        (5, f"{gs.table_jiq_col_total}_3", gs.const_filter_total),
        (5, f"{gs.table_jiq_col_total}_4", gs.const_filter_total),
        (5, f"{gs.table_jiq_col_total}_5", gs.const_filter_total),
    ],
)
def test_get_jiq_table_filter_model(junction_count, column, r):
    column_def = column_defs.get_jiq_table_filter_model(junction_count)[column]["filter"]
    assert column_def == r


@pytest.mark.parametrize(
    "junction_count, dictionary_count",
    [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
    ],
)
def test_get_jiq_table_filter_model_count_of_items(junction_count, dictionary_count):
    assert len(column_defs.get_jiq_table_filter_model(junction_count)) == dictionary_count


def test_get_geq_table_filter_model_norm():
    assert column_defs.get_geq_table_filter_model(True)[gs.table_geq_col_factor]["filter"] == 0


def test_get_geq_table_filter_model():
    assert column_defs.get_geq_table_filter_model(False) == {}


@pytest.mark.parametrize(
    "filter_value",
    [
        (gs.const_filter_total),
        (gs.const_filter_psi),
    ],
)
def test_make_dash_ag_grid_greater_than_or_equal_filter(filter_value):
    assert column_defs.make_dash_ag_grid_greater_than_or_equal_filter(filter_value)["filter"] == filter_value
    assert column_defs.make_dash_ag_grid_greater_than_or_equal_filter(filter_value)["type"] == "greaterThanOrEqual"
    assert column_defs.make_dash_ag_grid_greater_than_or_equal_filter(filter_value)["filterType"] == "number"


def test_get_geq_table_filter_model_2():
    assert column_defs.get_geq_table_filter_model(False) == {}


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
    click = {"points": [{"customdata": [2171668]}]}
    assert callback_common.on_box_plot_click(click, {})[gs.snpt_col_rail_id]["filterType"] == "number"


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


def test_get_text_dmc():
    assert isinstance(components.get_text("string"), dmc.Text)


def test_get_text_dbc():
    assert isinstance(components.get_text("string", "dbc"), dbc.Label)


def test_get_text():
    assert isinstance(components.get_text("string", "anything_else"), html.Label)


def test_get_input():
    assert isinstance(components.get_input("placeholder", "id"), dbc.Input)


def test_get_input_disabled():
    assert isinstance(components.get_input("placeholder", "id", True), dbc.Input)


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


def test_empty_inc_junction():
    assert exceptions.EmptyIncJunction(2).get_message().find("Inclusion Junction 2") != -1


def test_empty_exc_junction():
    assert exceptions.EmptyExcJunction(2).get_message().find("Exclusion Junction 2") != -1


def test_get_button_add_junction():
    assert len(components_jiq.get_button_add_junction()) == 2
    assert isinstance(components_jiq.get_button_add_junction()[0], dbc.Button)
    assert isinstance(components_jiq.get_button_add_junction()[1], dbc.Tooltip)


@pytest.mark.parametrize(
    "junction",
    [
        (1, 2, 3, 4),
    ],
)
def test_get_button_delete_junction(junction):
    assert len(components_jiq.get_button_delete_junction(junction)) == 2


@pytest.mark.parametrize(
    "junction, index, instance",
    [
        (1, 0, dbc.Button),
        (1, 1, dbc.Tooltip),
        (2, 0, dbc.Button),
        (2, 1, dbc.Tooltip),
        (3, 0, dbc.Button),
        (3, 1, dbc.Tooltip),
        (4, 0, dbc.Button),
        (4, 1, dbc.Tooltip),
    ],
)
def test_get_button_delete_junction_2(junction, index, instance):
    assert isinstance(components_jiq.get_button_delete_junction(junction)[index], instance)


def test_get_text_junction():
    assert isinstance(components_jiq.get_text_junction(1), dmc.Text)


def test_get_switch_normalize():
    assert isinstance(components_geq.get_switch_normalize(), dbc.Switch)


def test_get_checkbox_geq_optional_coordinates():
    assert len(components_geq.get_checkbox_geq_optional_coordinates()) == 2
    assert isinstance(components_geq.get_checkbox_geq_optional_coordinates()[0], dbc.Checklist)


def test_get_navbar_top():
    assert isinstance(navbars.get_navbar_top(), html.Div)


def test_get_navbar_bottom():
    assert isinstance(navbars.get_navbar_bottom(), html.Div)


def test_create_junction_row():
    assert len(layout_jiq.create_junction_row(1)) == 3


def test_get_form_jiq():
    assert len(layout_jiq.get_form_jiq()) == 4


def test_get_card_histogram_jiq():
    assert isinstance(layout_jiq.get_card_histogram_jiq(), dbc.Card)


def test_get_card_box_plot_jiq():
    assert isinstance(layout_jiq.get_card_box_plot_jiq(), dbc.Card)


def test_get_card_table_jiq():
    assert isinstance(layout_jiq.get_card_table_jiq(), dmc.Card)


def test_get_accordian_form_jiq():
    assert isinstance(layout_jiq.get_accordian_form_jiq(), dbc.Accordion)


def test_get_accordian_graphs_jiq():
    assert isinstance(layout_jiq.get_accordian_graphs_jiq(), dbc.Accordion)


def test_get_layout_junction_inclusion():
    assert isinstance(layout_jiq.get_layout_junction_inclusion(), dbc.Container)


def test_get_form_geq():
    assert len(layout_geq.get_form_geq()) > 0


def test_get_card_histogram_geq():
    assert isinstance(layout_geq.get_card_histogram_geq(), dbc.Card)


def test_get_accordian_form_geq():
    assert isinstance(layout_geq.get_accordian_form_geq(), dbc.Accordion)


def test_get_card_table_geq():
    assert isinstance(layout_geq.get_card_table_geq(), dmc.Card)


def test_get_accordian_graphs_geq():
    assert isinstance(layout_geq.get_accordian_graphs_geq(), dbc.Accordion)


def test_get_layout_gene_expression_query():
    assert isinstance(layout_geq.get_layout_gene_expression_query(), dbc.Container)


def test_get_tabs():
    assert isinstance(layout.get_tabs(), dbc.Tabs)


@pytest.mark.parametrize(
    "file_path, name",
    [
        (paths.srav3h_meta, paths.filename_srav3h),
        (paths.gtexv2_meta, paths.filename_gtexv2),
        (paths.tcgav2_meta, paths.filename_tcgav2),
        (paths.srav1m_meta, paths.filename_srav1m),
    ],
)
def test_paths(file_path, name):
    assert os.path.basename(file_path) == name
