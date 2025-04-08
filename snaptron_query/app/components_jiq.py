"""This file includes components related to the junction inclusion query"""

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from snaptron_query.app import global_strings as gs, icons, components


def get_button_add_junction():
    """Wrapper function to retrieve the multi junction component"""
    # search here for icon: https://icon-sets.iconify.design/
    button_id = "id-button-jiq-add-more-junctions"
    return [
        dbc.Button(
            id=button_id,
            n_clicks=0,
            children=[icons.add_box, gs.jiq_button_add_junction],
            color="link",
            # outline=True,
            style={"color": "var(--bs-primary)"},
            class_name="icon-button",
            size="sm",
        ),
        components.get_tooltip(button_id, gs.jiq_help_add_junction, "right"),
    ]


def get_button_delete_junction(index):
    """Wrapper function to retrieve the multi junction component"""
    # search here for icon: https://icon-sets.iconify.design/
    button_id = f"id-button-jiq-delete-junctions-{index}"
    return [
        dbc.Button(
            id=button_id,
            n_clicks=0,
            children=[icons.del_box, gs.jiq_button_delete_junction],
            color="link",
            # since this button is a dynamic component that is added to the layout,
            # the display changes override the style={"color": "var(--bs-secondary)"} properties,
            # but defining it as a class in assets seems to do the trick.
            class_name="del-button",
            size="sm",
        ),
        dbc.Tooltip(
            id=f"{button_id}-tip",
            children=gs.jiq_help_delete_junction,
            is_open=False,
            target=button_id,
            placement="right",
            # some style is overriding the tooltip and making the strings all caps
            # overriding the text transform here
            # the tooltips for the delete button also need to be set to a none display
            style={"text-transform": "none", "display": "none"},
        ),
    ]


def get_text_junction(index):
    return dmc.Text(gs.jiq_input_junction_txt_list[index], weight=500, size="sm")


def get_checkbox_jiq_expanded_coordinates():
    return [
        dbc.Checklist(
            id="id-checkbox-expanded-coordinates",
            options=[{"label": gs.jiq_expanded_coordinates, "value": 1}],
            label_checked_style={"color": "var(--bs-danger)"},
            input_checked_style={"backgroundColor": "var(--bs-danger)", "borderColor": "#ea6258"},
        ),
        components.get_tooltip("id-checkbox-expanded-coordinates", gs.jiq_caution_expanded_coordinates, "left"),
    ]
