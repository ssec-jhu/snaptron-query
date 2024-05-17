"""This file includes the general layout inside the tabs"""

import dash_bootstrap_components as dbc
from snaptron_query.app import layout_jiq, layout_geq, global_strings as gs


def get_tabs():
    """This defines the tab layout."""
    tabs = dbc.Tabs(
        [
            # Junction Inclusion Query Tab
            dbc.Tab(
                layout_jiq.get_layout_junction_inclusion(),
                label=gs.tab_jiq,
                tab_id="id-tab-horizontal-bootstrap-jiq",
            ),

            # Gene Expression Query Tab
            dbc.Tab(
                layout_geq.get_layout_gene_expression_query(),
                label=gs.tab_geq,
                tab_id="id-tab-horizontal-bootstrap-geq",
            ),
        ],
        active_tab="id-tab-horizontal-bootstrap-jiq",
        className="dbc nav-fill",  # Use Bootstrap's nav-fill class to fill the tab_horizontal_bootstrap space
    )
    return tabs
