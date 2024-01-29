"""
    This file includes components related to the junction inclusion query form
"""

import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash_iconify import DashIconify

import inline_styles
import global_strings

# TODO: GLOBAL: move text into global strings

"""
    Wrapper function to retrieve the dropdown component based on the style
"""


def get_dropdown_compilation(component_style):
    # component_style='dbc'
    string = global_strings.drop_compilation
    data_list = global_strings.compilation_list
    placeholder = global_strings.drop_compilation_placeholder
    dropdown_id = 'id-input-compilation'

    # TODO: check whether default is wanted or have client proactively select
    default = data_list[0]

    if component_style == 'dmc':
        return dmc.Select(
            id=dropdown_id,
            label=string,
            placeholder="Can't get the width of this to match exactly with bottom",
            data=data_list,
            searchable=True,
            nothingFound="No options found",
            value=default,
            # style={"width": 200},
        )
    # elif component_style == 'dbc':
    #     return dbc.Select(
    #         id=dropdown_id,
    #         options=[
    #             {"label": "Option 1", "value": 1},
    #             {"label": "Option 2", "value": 2},
    #         ]
    #     )
    elif component_style == 'dcc':
        # dcc dropdown component doesn't have an automatic label, so I am bundling it into a html.Div
        return html.Div(
            [
                html.Label(string),
                dcc.Dropdown(data_list,
                             # 'srav3h', #removing default value for now.
                             placeholder=placeholder,
                             value=default,
                             id=dropdown_id)
            ]
        )


"""
    Wrapper function to retrieve the button component based on the style
"""


def get_button_add_junction(component_style):
    # search here for icon: https://icon-sets.iconify.design/
    add_icon = DashIconify(icon="ic:round-add-box")
    string = global_strings.button_add_junction
    button_id = 'id-button-add-more-junctions'
    if component_style == 'dmc':
        return dmc.Button(
            string,
            id=button_id,
            leftIcon=add_icon,
            variant='subtle',
            size="sm",
            n_clicks=0
        )
    elif component_style == 'dbc':
        return dbc.Button(
            id=button_id,
            children=[html.I(add_icon), string],
            size="sm",
            color="link",
            n_clicks=0,
        )


"""
    Wrapper function to retrieve the button component based on the style
"""


def get_button_generate_results(component_style):
    string = global_strings.button_run
    button_id = 'id-button-generate-results'
    if component_style == 'dmc':
        return dmc.Button(
            string,
            id=button_id,
            n_clicks=0,
            # the rest is styling related
            variant="light",
            color="indigo",
            # colors=[
            #     "gray",
            #     "red",
            #     "pink",
            #     "grape",
            #     "violet",
            #     "indigo",
            #     "blue",
            #     "lime",
            #     "yellow",
            #     "orange",
            # ]
            fullWidth=True,
            mt="md",
            radius="md",
        )
    elif component_style == 'dbc':
        return dbc.Button(
            string,
            n_clicks=0,
            id=button_id,
            # the rest is styling related
            size="sm",  # smaller button size
            # STYLE notes:
            # mx-auto: centers it
            # col-8: sets the width of the button to 8 columns...
            # class_name="d-grid mx-auto, btn-outline-primary"
            color="light",
            # outline=True,
            class_name="d-grid gap-2 col-8 mx-auto",  # bg-secondary text-light
            style={'backgroundColor': inline_styles.buttonColor}
        )


"""
    Wrapper function to retrieve the texted boxes used in the JIQ query based on the style only
"""


def get_input(component_style, input_placeholder, input_id):
    # debounce:
    # if True, changes to input will be sent back to the Dash server only on enter or
    # when losing focus.

    if component_style == 'dmc':
        return dmc.TextInput(
            id=input_id,
            placeholder=input_placeholder,
            debounce=True,
            size='sm',  # or md
            mr='5px',  # add some margin to the right of the textbox

        )
    elif component_style == 'dcc':
        return dcc.Input(
            id=input_id,
            placeholder=input_placeholder,
            type="text",
            debounce=True
        )


"""
    Wrapper functions to dynamically create input textbox components given their id and style
"""


def get_input_chrom(component_style):
    input_placeholder = global_strings.input_chr_placeholder
    input_id = 'id-input-chromosome'
    return get_input(component_style, input_placeholder, input_id)


def get_input_inc_junction(component_style):
    input_placeholder = global_strings.input_inc_placeholder
    input_id = 'id-input-inc-junc'
    return get_input(component_style, input_placeholder, input_id)


def get_input_exc_junction(component_style):
    input_placeholder = global_strings.input_exc_placeholder
    input_id = 'id-input-exc-junc'
    return get_input(component_style, input_placeholder, input_id)


def get_text(component_style, string):
    """
        Wrapper function to retrieve the text used in the JIQ query based on the style only
    """
    if component_style == 'dmc':
        return dmc.Text(string, weight=500, size="sm")  # semi bold
    elif component_style == 'dcc':
        return html.Label(string)


"""
    Functions Below: Wrapper functions to to dynamically create text components given their string, and style
"""


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
        return dmc.Text(string, weight=500, size="md")
    elif component_style == 'dcc':
        return html.Label(string)
