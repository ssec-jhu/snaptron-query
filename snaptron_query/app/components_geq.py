import dash_bootstrap_components as dbc
from snaptron_query.app import global_strings as gs, components


def get_switch_normalize():
    return dbc.Switch(id='id-switch-geq-normalize', label=gs.geq_normalized, className='text-primary')


def get_checkbox_geq_optional_coordinates():
    return [
        dbc.Checklist(id="id-checkbox-use-coordinates", options=[{"label": gs.geq_provide_coordinates, "value": 1}],
                      label_checked_style={"color": "var(--bs-danger)"},
                      input_checked_style={"backgroundColor": "var(--bs-danger)", "borderColor": "#ea6258"}),
        components.get_tooltip("id-checkbox-use-coordinates", gs.geq_help_checkbox, 'left')
    ]
