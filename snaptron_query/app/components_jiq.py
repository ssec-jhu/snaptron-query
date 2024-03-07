"""This file includes components related to the junction inclusion query"""

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from snaptron_query.app import components as c_component
from snaptron_query.app import global_strings


def get_button_add_junction():
    """Wrapper function to retrieve the multi junction component"""
    # search here for icon: https://icon-sets.iconify.design/
    return dbc.Button(
        id='id-button-add-more-junctions',
        children=[html.I(DashIconify(icon="ic:round-add-box")), global_strings.button_add_junction],
        size="sm",
        color="link",
        n_clicks=0,
    )


def get_button_generate_results():
    """Wrapper function to retrieve the button component"""
    return dbc.Button(
        global_strings.button_run,
        n_clicks=0,
        id='id-button-generate-results',
        size="md",  # button size
        class_name="btn-primary",
    )


"""Wrapper functions to dynamically create input textbox components given their id and style"""


def get_input_inc_junction():
    return c_component.get_input(global_strings.input_inc_placeholder, 'id-input-inc-junc')


def get_input_exc_junction():
    return c_component.get_input(global_strings.input_exc_placeholder, 'id-input-exc-junc')


"""Functions Below: Wrapper functions to to dynamically create text components given their string, and style"""


def get_text(component_style, string):
    """Wrapper function to retrieve the text used in the JIQ query based on the style only"""
    if component_style == 'dmc':
        return dmc.Text(string, weight=500, size="sm")  # 500=semi bold
    elif component_style == 'dbc':
        return dbc.Label(string, className='fw-bold')
    else:
        return html.Label(string)


def get_text_inclusion_junction(component_style):
    return c_component.get_text(component_style, global_strings.input_inc_txt)


def get_text_exclusion_junction(component_style):
    return c_component.get_text(component_style, global_strings.input_exc_txt)


def get_text_junction(component_style):
    # the size of this is bigger, may change it to sm later
    # TODO: MultiJunction query: id fields for the text boxes need to be generated dynamically
    string = global_strings.input_junction_txt_list[0]
    if component_style == 'dmc':
        return dmc.Text(string, weight=500, size="sm")
    elif component_style == 'dbc':
        return dbc.Label(string, className='text-primary me-1 sm')
    else:
        return html.Label(string)


def get_button_download():
    return dbc.Button(
        global_strings.button_download,
        id='id-button-download',
        n_clicks=0,
        size="md",  # button size
        class_name="d-grid gap-2 col-8 btn-primary",  # bg-secondary text-light #mx-auto
    )


def get_switch_log_psi_histogram():
    return dbc.Switch(
        id='id-switch-log-psi-histogram',
        label=global_strings.switch_log,
    )


def get_switch_log_psi_box_plot():
    return dbc.Switch(
        id='id-switch-log-psi-box-plot',
        label=global_strings.switch_log,
    )


def get_switch_violin_box_plot():
    return dbc.Switch(
        id='id-switch-violin-box-plot',
        label=global_strings.switch_violin,
    )


def get_switch_lock_data_with_table():
    return html.Div(
        [
            # TODO: Keep label here for now, string needs to come out of switch later,
            #  the width doesn't fit at the moment
            # html.Label(string),
            dbc.Switch(
                id='id-switch-lock-with-table',
                label=global_strings.switch_lock,
            )
        ]
    )


def get_table_jiq():
    table = dag.AgGrid(
        id="id-ag-grid",
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
