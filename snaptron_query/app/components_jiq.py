"""This file includes components related to the junction inclusion query"""

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from snaptron_query.app import global_strings as gs


def get_button_add_junction():
    """Wrapper function to retrieve the multi junction component"""
    # search here for icon: https://icon-sets.iconify.design/
    return dbc.Button(
        id='id-button-jiq-add-more-junctions',
        children=[html.I(DashIconify(icon="ic:round-add-box")), gs.button_add_junction],
        size="sm",
        color="link",
        n_clicks=0,
    )


def get_button_jiq_results():
    """Wrapper function to retrieve the button component"""
    return dbc.Button(
        gs.button_run,
        n_clicks=0,
        id='id-button-jiq-generate-results',
        size="md",  # button size
        class_name="btn-primary",
    )


"""Functions Below: Wrapper functions to to dynamically create text components given their string, and style"""


def get_text_junction(component_style):
    # the size of this is bigger, may change it to sm later
    # TODO: MultiJunction query: id fields for the text boxes need to be generated dynamically
    string = gs.input_junction_txt_list[0]
    if component_style == 'dmc':
        return dmc.Text(string, weight=500, size="sm")
    elif component_style == 'dbc':
        return dbc.Label(string, className='text-primary me-1 sm')
    else:
        return html.Label(string)


def get_button_download():
    return dbc.Button(
        gs.button_download,
        id='id-button-jiq-download',
        n_clicks=0,
        size="md",  # button size
        class_name="d-grid gap-2 col-8 btn-primary",  # bg-secondary text-light #mx-auto
    )


def get_table_jiq():
    table = dag.AgGrid(
        id="id-ag-grid-jiq",
        persistence=True,  # https://community.plotly.com/t/how-to-add-persistence-to-dash-ag-grid/74944
        style={'height': 600},
        defaultColDef={"flex": 1,  # snaps the end
                       "sortable": True, "resizable": True, "filter": True,
                       },
        dashGridOptions={'rowSelection': 'multiple',
                         'checkboxSelection': 'True',
                         'isRowSelectable': {"function": "log(params)"},
                         'pagination': True,
                         },
    )
    return table
