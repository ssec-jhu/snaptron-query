"""
    This file includes components related to the junction inclusion query form
"""

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc
from dash_iconify import DashIconify

import global_strings


def get_dropdown_compilation():
    """
        Wrapper function to retrieve the dropdown component
    """
    string = global_strings.drop_compilation
    data_list = global_strings.compilation_list
    # TODO: verify placeholder text with PI
    placeholder = global_strings.drop_compilation_placeholder
    dropdown_id = 'id-input-compilation'
    # TODO: check whether default is wanted or have client proactively select
    default = data_list[0]

    dropdown = html.Div(
        [
            dbc.Label(string, className='fw-bold'),
            dcc.Dropdown(
                data_list,
                default,
                id=dropdown_id,
            ),
        ],
        className="dbc",
    )
    return dropdown


def get_button_add_junction():
    """
        Wrapper function to retrieve the multi junction component
    """
    # search here for icon: https://icon-sets.iconify.design/
    add_icon = DashIconify(icon="ic:round-add-box")
    string = global_strings.button_add_junction
    button_id = 'id-button-add-more-junctions'

    return dbc.Button(
        id=button_id,
        children=[html.I(add_icon), string],
        size="sm",
        color="link",
        n_clicks=0,
    )


"""
    Wrapper function to retrieve the button component
"""


def get_button_generate_results():
    string = global_strings.button_run
    button_id = 'id-button-generate-results'

    return dbc.Button(
        string,
        n_clicks=0,
        id=button_id,
        # the rest is styling related
        size="md",  # button size
        # STYLE notes:
        # mx-auto: centers it
        # col-8: sets the width of the button to 8 columns...
        # class_name="d-grid mx-auto, btn-outline-primary"
        # color="light",
        # outline=True,
        class_name="d-grid gap-2 col-8 mx-auto btn-primary",  # bg-secondary text-light
        # style={'backgroundColor': inline_styles.buttonColor}
    )


def get_input(input_placeholder, input_id):
    """
        Wrapper function to retrieve the texted boxes used in the JIQ query based on the style only
    """
    return dbc.Input(
        id=input_id,
        placeholder=input_placeholder,
        size="sm",
        # className="mr-5"
    )


"""
    Wrapper functions to dynamically create input textbox components given their id and style
"""


def get_input_chrom():
    input_placeholder = global_strings.input_chr_placeholder
    input_id = 'id-input-chromosome'
    return get_input(input_placeholder, input_id)


def get_input_inc_junction():
    input_placeholder = global_strings.input_inc_placeholder
    input_id = 'id-input-inc-junc'
    return get_input(input_placeholder, input_id)


def get_input_exc_junction():
    input_placeholder = global_strings.input_exc_placeholder
    input_id = 'id-input-exc-junc'
    return get_input(input_placeholder, input_id)


"""
    Functions Below: Wrapper functions to to dynamically create text components given their string, and style
"""


def get_text(component_style, string):
    """
        Wrapper function to retrieve the text used in the JIQ query based on the style only
    """
    if component_style == 'dmc':
        return dmc.Text(string, weight=500, size="sm")  # 500=semi bold
    elif component_style == 'dbc':
        return dbc.Label(string, className='fw-bold')
    elif component_style == 'dcc':
        return html.Label(string)


def get_text_chromosome(component_style):
    string = global_strings.input_chr_txt
    return get_text(component_style, string)


def get_text_inclusion_junction(component_style):
    string = global_strings.input_inc_txt
    return get_text(component_style, string)


def get_text_exclusion_junction(component_style):
    string = global_strings.input_exc_txt
    return get_text(component_style, string)


def get_text_junction(component_style):
    # the size of this is bigger, may change it to sm later
    # TODO: MultiJunction query: id fields for the text boxes need to be generated dynamically
    string = global_strings.input_junction_txt_list[0]
    if component_style == 'dmc':
        return dmc.Text(string, weight=500, size="sm")
    elif component_style == 'dbc':
        return dbc.Label(string, className='text-primary me-1 sm')
    elif component_style == 'dcc':
        return html.Label(string)
