"""
    This file includes the general layout inside the tabs

"""

import dash_bootstrap_components as dbc
from dash import html, dcc

import inline_styles as styles
import layout_jiq
import global_strings

"""
    This is the component at the top of the page. It can be
"""
jumbotron = html.Div(
    dbc.Container(
        [
            html.P("Snaptron Custom Query"),
            # html.Hr(className="my-2"),
        ],
        fluid=True,
        className="display-4",  # py-6, display-4 is bigger
    ),
    style={'box-shadow': "0 5px 5px -5px #333"},
    className="bg-primary bg-gradient text-light py-4 text-center fs-1 fw-light",  # bg-secondary
)

"""
    This layout puts the user queries in horizontal tab format.
    Style: Bootstrap
    Pros: gives the form layout more room
    Cons: The aesthetics
"""
tab_horizontal_bootstrap = dbc.Tabs(
    [
        # Junction Inclusion Query Tab
        dbc.Tab(
            layout_jiq.get_layout_junction_inclusion(),
            label=global_strings.tab_jiq,
            tab_id="id-tab-horizontal-bootstrap-jiq",
        ),

        # Gene Expression Query Tab
        dbc.Tab(
            label=global_strings.tab_geq,
            tab_id="id-tab-horizontal-bootstrap-geq",
        ),
    ],
    # id="id-tabs",
    active_tab="id-tab-horizontal-bootstrap-jiq",
    className="dbc nav-fill",  # Use Bootstrap's nav-fill class to fill the tab_horizontal_bootstrap space
)

"""
    This layout puts the user queries in vertical tab format.
    Style: DCC tabs
    Pros: gives the form layout more room
    Cons: The aesthetics
"""
tab_horizontal_styled = dcc.Tabs(
    children=[
        dcc.Tab(
            layout_jiq.get_layout_junction_inclusion(),
            label=global_strings.tab_jiq,
            value='jiq',
            style=styles.horizontal_tab,
            selected_style=styles.horizontal_tab_selected,
            # selected_className='custom-tab--selected'
        ),
        dcc.Tab(  # TODO: Gene expression layout here
            label=global_strings.tab_geq,
            value='geq',
            style=styles.horizontal_tab,
            selected_style=styles.horizontal_tab_selected,
            # className='bg-primary',
            # selected_className='bg-light'
        ),
    ],
    # style=custom_inline_styles.horizontal_tabs,
    # className='custom-tabs',
    # className="dbc", #uncomment this to get the dbc theme applied to the tabs
    id='tabs',
    value='jiq',  # active tab
)
