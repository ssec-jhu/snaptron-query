import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc

from snaptron_query.app import global_strings as gs


def get_text(component_style, string):
    """Wrapper function to retrieve the text used  queries"""
    if component_style == 'dmc':
        return dmc.Text(string, weight=500, size="sm")  # 500=semi bold
    elif component_style == 'dbc':
        return dbc.Label(string, className='fw-bold')
    elif component_style == 'dcc':
        return html.Label(string)


def get_input(input_placeholder, input_id, disabled=False):
    """Wrapper function to retrieve the texted boxes used in the queries"""
    return dbc.Input(
        id=input_id,
        placeholder=input_placeholder,
        size="sm",
        disabled=disabled
        # className="mr-5"
    )


def get_dropdown_compilation(component_id):
    """Wrapper function to retrieve the dropdown component"""
    dropdown = html.Div(
        [
            dbc.Label(gs.drop_compilation, className='fw-bold'),
            dcc.Dropdown(
                options=gs.compilation_names_dict,
                id=component_id,
            ),
        ],
        className="dbc",
    )
    return dropdown


def get_switch(switch_id, switch_label):
    return dbc.Switch(
        id=switch_id,
        label=switch_label
    )


def get_switch_lock_data_with_table(switch_id, switch_label):
    return html.Div(
        [
            # TODO: Keep label here for now, string needs to come out of switch later,
            #  the width doesn't fit at the moment
            # html.Label(string),
            dbc.Switch(
                id=switch_id,
                label=switch_label,
            )
        ]
    )