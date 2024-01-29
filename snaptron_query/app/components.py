"""
    This file includes most general components used in all the queries
    Form specific components relative to specific queries are are put in a separate file
"""

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html
import global_strings
import inline_styles


def get_button_download(component_style):
    string = global_strings.button_download_str
    button_id = 'id-button-download'
    # TODO: add the icon
    # add_icon = DashIconify(icon="ic:round-add-box")
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
            id=button_id,
            n_clicks=0,
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


def get_switch_log_psi(component_style):
    string = global_strings.switch_log_str
    switch_id = 'id-switch-log-psi'
    if component_style == 'dmc':
        return dmc.Switch(
            id=switch_id,
            label=string,
            onLabel="ON",
            offLabel="OFF",
            size='md',
            checked=False,
            # TODO: manage toggle switch persistence later, is this wanted?
            # https://www.dash-mantine-components.com/components/switch
            # persistence,
        )
    elif component_style == 'dbc':
        return dbc.Switch(
            id=switch_id,
            label=string,
            # class_name="d-grid gap-2 col-8 mx-auto",  # bg-secondary text-light
            # style={'backgroundColor': inline_styles.tabBackgroundColor}
        )


def get_switch_lock_data_with_table(component_style):
    string = global_strings.switch_lock_str
    switch_id = 'id-switch-lock-with-table'
    # TODO: add the icon
    # add_icon = DashIconify(icon="ic:round-add-box")
    if component_style == 'dmc':
        return dmc.Switch(
            id=switch_id,
            label=string,
            onLabel="ON",
            offLabel="OFF",
            size='md',
            checked=False,
            # TODO: manage toggle switch persistence, is this wanted
            # https://www.dash-mantine-components.com/components/switch
            # persistence,
        )
    elif component_style == 'dbc':
        return html.Div(
            [
                # TODO: One option if the button doesn't fit is the take the label out as a separate component
                # html.Label(string),
                dbc.Switch(
                    id=switch_id,
                    label=string,
                    style={'backgroundColor': inline_styles.borderColor}
                )
            ]
        )
