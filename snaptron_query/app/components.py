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


def get_dropdown_compilation():
    """Wrapper function to retrieve the dropdown component"""
    dropdown = html.Div(
        [
            dbc.Label(gs.drop_compilation, className='fw-bold'),
            dcc.Dropdown(
                options=gs.compilation_names_dict,
                id='id-input-compilation',
            ),
        ],
        className="dbc",
    )
    return dropdown
