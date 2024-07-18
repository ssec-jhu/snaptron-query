import os
from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict
import pytest

# Import the names of callback functions you want to test
from snaptron_query.app import main_dash_app as mapp
from snaptron_query.app import global_strings as gs, column_defs as cd
from snaptron_query.app.runner_geq import run_query

# tests will run locally as the tests start higher up the front end pipeline and will make calls to the snaptron API
IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping test on Github")
def test_callback_geq():
    """
    Tests the UI function with the call back context
    """

    def run_callback():
        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": "id-button-geq-run-query.n_clicks"}]}))
        return mapp.on_button_click_geq(
            n_clicks=1,
            compilation=gs.compilation_srav3h,
            use_coordinates=False,
            query_gene_id="TARDBP",
            query_gene_coordinates=None,
            normalize_data=True,
            norm_gene_id="EDF1",
            norm_gene_coordinates=None,
            box_plot_log_x=True,
            violin_overlay=False,
            # normalized_data,
            histogram_log_x=True,
            histogram_log_y=False,
        )

    ctx = copy_context()
    (
        display,
        row_data,
        column_defs,
        filter_model,
        spinner,
        alert,
        box_plot,
        histogram,
        width_box,
        width_hist,
        hist_display,
        style_section,
    ) = ctx.run(run_callback)
    assert len(row_data) == 269157
    assert column_defs == cd.get_gene_expression_query_column_def(gs.compilation_srav3h, normalized=True)
    assert filter_model == cd.get_geq_table_filter_model(1)
    assert len(histogram["data"]) == 1
    assert len(box_plot["data"]) == 2
    assert box_plot["data"][0]["name"] == gs.geq_plot_label_raw_count
    assert box_plot["data"][1]["name"] == gs.geq_plot_label_norm_count
    assert width_box == {"size": 6}
    assert width_hist == {"size": 6}


def test_run_query():
    (row_data, column_defs, filter_model, box_plot, histogram, width_box, width_hist, hist_display) = run_query(
        meta_data_dict=mapp.get_meta_data("SRAv3h"),
        normalize_data=True,
        use_coordinates=None,
        norm_gene_coordinates=None,
        query_gene_coordinates=None,
        compilation="SRAv3h",
        norm_gene_id="EDF1",
        query_gene_id="TARDBP",
        histogram_log_x=True,
        histogram_log_y=False,
        box_plot_log_x=True,
        violin_overlay=False,
    )
    assert len(row_data) == 269157
    assert column_defs == cd.get_gene_expression_query_column_def(gs.compilation_srav3h, normalized=True)
    assert filter_model == cd.get_geq_table_filter_model(1)
    assert len(histogram["data"]) == 1
    assert len(box_plot["data"]) == 2
    assert box_plot["data"][0]["name"] == gs.geq_plot_label_raw_count
    assert box_plot["data"][1]["name"] == gs.geq_plot_label_norm_count
    assert width_box == {"size": 6}
    assert width_hist == {"size": 6}
