"""
    This file includes components related to the junction inclusion query
"""

from dash import html, dcc
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_ag_grid as dag
import global_strings
import inline_styles


def get_dropdown_compilation():
    """
        Wrapper function to retrieve the dropdown component
    """
    string = global_strings.drop_compilation
    data_list = global_strings.compilation_list
    # TODO: verify placeholder text with PI
    # placeholder = global_strings.drop_compilation_placeholder
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


def get_button_download():
    string = global_strings.button_download_str
    button_id = 'id-button-download'
    # TODO: add the icon
    return dbc.Button(
        string,
        id=button_id,
        n_clicks=0,
        size="md",  # button size
        class_name="d-grid gap-2 col-8 btn-primary",  # bg-secondary text-light #mx-auto
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
    # TODO: Bug: this needs to switch to a dmc type but for some reason the plots don't pick up the dmc switch changes
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


def get_table_jiq():
    table = dag.AgGrid(
        id="id-ag-grid",
        # ag grid and persistence: data will get lost when tab switches
        # https://community.plotly.com/t/how-to-add-persistence-to-dash-ag-grid/74944
        persistence=True,
        # columnDef and rowData will be dynamically defined via callback
        # columnDefs=[{"field": i} for i in df.columns.to_list()],
        # rowData=df.to_dict("records"),

        # TODO: height of the table may need to be dynamic depending on compilation data
        style={'height': 600},

        # TODO: multi-junction query will need column size to fit
        # columnSize="sizeToFit",
        defaultColDef={"flex": 1,  # snaps the end
                       "sortable": True, "resizable": True, "filter": True,
                       # "minWidth": 150,
                       # TODO: is cell wrapping required when the abstract of the study is
                       #  included. Both of below must be on for cell wrapping
                       # 'wrapText': True,
                       # 'autoHeight': True,
                       },
        dashGridOptions={'rowSelection': 'multiple',
                         'checkboxSelection': 'True',
                         'isRowSelectable': {"function": "log(params)"},
                         'pagination': True,
                         },
        # TODO: this will NOT change the table theme to dbc
        # className="header-style-on-filter ag-theme-alpine dbc-ag-grid",
    )
    return table
