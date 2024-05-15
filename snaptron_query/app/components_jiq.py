"""This file includes components related to the junction inclusion query"""
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from snaptron_query.app import global_strings as gs, icons, components


def get_button_add_junction():
    """Wrapper function to retrieve the multi junction component"""
    # search here for icon: https://icon-sets.iconify.design/
    button_id = 'id-button-jiq-add-more-junctions'
    return [dbc.Button(id=button_id, n_clicks=0, children=[icons.add_box, gs.jiq_button_add_junction],
                       # TODO: confirm with PI of the removal of the green link to make it actually look like a button
                       color="link",
                       # outline=True,
                       style={'color': 'var(--bs-primary)'}, class_name='icon-button', size="sm"),
            components.get_tooltip(button_id, gs.jiq_help_add_junction, 'right')]


def get_text_junction(index):
    return dmc.Text(gs.jiq_input_junction_txt_list[index], weight=500, size="sm")
