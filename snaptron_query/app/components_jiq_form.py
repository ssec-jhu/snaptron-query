"""
    This file includes components related to the junction inclusion query form
"""

import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash_iconify import DashIconify

import inline_styles


#####################
#       DROP DOWN
#####################

def get_dropdown_compilation(comp):
    string = 'Compilation'
    # TODO: GLOBAL: compilation list
    data_list = ['srav3h', 'gtexv2', 'srav1m', 'tcaga2']
    placeholder = 'Select a compilation'
    dropdown_id = 'id-input-compilation'

    # TODO: check whether default is wanted ot have client proactively select
    default = data_list[0]

    if comp == 'dmc':
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
    # elif comp == 'dbc':
    #     return dbc.Select(
    #         id=dropdown_id,
    #         options=[
    #             {"label": "Option 1", "value": 1},
    #             {"label": "Option 2", "value": 2},
    #         ]
    #     )
    elif comp == 'dcc':
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


#####################
#       BUTTONS
#####################
def get_button_add_junction(comp):
    # search here for icon: https://icon-sets.iconify.design/
    add_icon = DashIconify(icon="ic:round-add-box")
    string = 'Add Junction'
    button_id = 'id-button-add-more-junctions'
    if comp == 'dmc':
        return dmc.Button(
            string,
            id=button_id,
            leftIcon=add_icon,
            variant='subtle',
            size="sm",
            n_clicks=0
        )
    elif comp == 'dbc':
        return dbc.Button(
            id=button_id,
            children=[html.I(add_icon), string],
            size="sm",
            color="link",
            n_clicks=0,
        )


def get_button_generate_results(comp):
    string = 'Generate Results'
    button_id = 'id-button-generate-results'
    if comp == 'dmc':
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
    elif comp == 'dbc':
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


#####################
#       TEXT INPUTS
#####################
def get_input(comp, input_placeholder, input_id):
    # debounce:
    # if True, changes to input will be sent back to the Dash server only on enter or
    # when losing focus.

    if comp == 'dmc':
        return dmc.TextInput(
            id=input_id,
            placeholder=input_placeholder,
            debounce=True,
            size='sm',  # or md
            mr='5px',  # add some margin to the right of the textbox

        )
    elif comp == 'dcc':
        return dcc.Input(
            id=input_id,
            placeholder=input_placeholder,
            type="text",
            debounce=True
        )


def get_input_chrom(comp):
    input_placeholder = 'ex: 19'
    input_id = 'id-input-chromosome'
    return get_input(comp, input_placeholder, input_id)


def get_input_inc_junction(comp):
    input_placeholder = 'ex: 4491836-4492014'
    input_id = 'id-input-inc-junc'
    return get_input(comp, input_placeholder, input_id)


def get_input_exc_junction(comp):
    input_placeholder = 'ex: 4491836-4493702'
    input_id = 'id-input-exc-junc'
    return get_input(comp, input_placeholder, input_id)


#####################
#       TEXT
#####################

def get_text(comp, string):
    if comp == 'dmc':
        return dmc.Text(string, weight=500, size="sm")  # semi bold
    elif comp == 'dcc':
        return html.Label(string)


def get_text_chromosome(comp):
    string = 'Chromosome'
    return get_text(comp, string)


def get_text_inclusion_junction(comp):
    string = 'Inclusion Junction'
    return get_text(comp, string)


def get_text_exclusion_junction(comp):
    string = 'Exclusion Junction'
    return get_text(comp, string)


def get_text_junction(comp):
    # the size of this is bigger, may change it to sm later
    string = 'Junction 1'
    if comp == 'dmc':
        return dmc.Text(string, weight=500, size="md")
    elif comp == 'dcc':
        return html.Label(string)
