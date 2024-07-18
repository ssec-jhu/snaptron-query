import os
from contextvars import copy_context

from dash._callback_context import context_value
from dash._utils import AttributeDict
import pytest

from snaptron_query.app import global_strings as gs, column_defs as cd

# Import the names of callback functions you want to test
from snaptron_query.app.main_dash_app import on_button_click_jiq

# tests will run locally as the tests start higher up the front end pipeline and will make calls to the snaptron API
IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping test on Github")
def test_callback_jiq(sample_ui_children):
    def run_callback():
        context_value.set(
            AttributeDict(**{"triggered_inputs": [{"prop_id": "id-button-jiq-generate-results.n_clicks"}]})
        )
        n_clicks = 1
        compilation = gs.compilation_srav3h
        children = sample_ui_children
        junction_count = None
        box_log_psi = True
        violin_overlay = False
        histogram_log_psi = True
        histogram_log_y = False
        return on_button_click_jiq(
            n_clicks,
            compilation,
            children,
            junction_count,
            box_log_psi,
            violin_overlay,
            histogram_log_psi,
            histogram_log_y,
        )

    ctx = copy_context()
    (
        display,
        row_data,
        column_defs,
        filter_model,
        spinner,
        alert,
        histogram,
        box_plot,
        col_width,
        col_width2,
        display_style,
    ) = ctx.run(run_callback)
    assert display == {"display": "block"}
    assert len(row_data) == 160576
    assert column_defs == cd.get_junction_query_column_def(gs.compilation_srav3h, 1)
    assert filter_model == cd.get_jiq_table_filter_model(1)
    assert len(histogram["data"]) == 1
    assert len(box_plot["data"]) == 1
    assert col_width == {"size": 6}
    assert col_width2 == {"size": 6}
