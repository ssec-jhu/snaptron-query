import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc
import dash_ag_grid as dag

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


def get_switch(switch_id, switch_label, switch_on=False):
    return dbc.Switch(
        id=switch_id,
        label=switch_label,
        value = switch_on
    )


def get_switch_lock_data_with_table(switch_id, switch_label):
    return html.Div(
        [
            # html.Label(switch_label),
            dbc.Switch(
                # dbc switch follows the text size of it's label
                id=switch_id,
                # label=switch_label,
                # dbc switch follows the text size of its label, so you can use something like class_name="fs-6"
                # https://community.plotly.com/t/dbc-switch-make-larger/80146
                value=True,


            )
            # dmc.Switch(
            #     id=switch_id,
            #     left=True,
            #     #label=switch_label,
            #     #color="rgba(23, 8, 8, 1)",
            #     # #color='var(--bs-primary)',
            #     # styles={"track": {"background-color": 'var(--bs-primary)'},
            #     #         "input:checked":  {"background-color": 'var(--bs-success)'},
            #     # },
            #     # style={'color': 'var(--bs-primary)'},
            #     thumbIcon=DashIconify(
            #         icon="mdi:lock-outline", width=16, color=dmc.theme.DEFAULT_COLORS["teal"][5]
            #     ),
            #     size="lg",
            #     checked=True,
            # )
        ]
    )


def get_alert(alert_message):
    return [
        dmc.Space(h=20),
        dbc.Alert(
            children=f'{alert_message}',
            # id="id-alert-fade",
            # color="var(--bs-danger-border-subtle)",
            dismissable=True,
            is_open=True,
            class_name='user-alert'
        )
    ]


def get_table(table_id):
    table = dag.AgGrid(
        id=table_id,
        # csvExportParams={
        #     "fileName": "query_data.csv",
        # },
        persistence=True,  # https://community.plotly.com/t/how-to-add-persistence-to-dash-ag-grid/74944
        style={'height': 700},
        defaultColDef={
            # do NOT set "flex": 1 in default col def as it overrides all the column widths
            "sortable": True, "resizable": True, "filter": True,
            # Set BOTH items below to True for header to wrap text
            "wrapHeaderText": True, "autoHeaderHeight": True,
        },
        dashGridOptions={'rowSelection': 'multiple',
                         'checkboxSelection': 'True',
                         'isRowSelectable': {"function": "log(params)"},
                         'pagination': True,
                         # this will set the number of items per page be a function of the height
                         # if we load too many rows that are not visible, the graphics is not smart enough
                         # to hide what is not visible, so it takes longer for the page to load
                         'paginationAutoPageSize': True,
                         # Tooltip options https://dashaggridexamples.pythonanywhere.com/tooltips
                         "tooltipShowDelay": 0,  # Makes tooltip show immediately.  Default 2000ms
                         # "tooltipHideDelay": 3000,  # Hides tooltip after 3000ms
                         "tooltipInteraction": True,  # Won't hide when hover on toolip.  Can select and copy content.
                         },
        # NOTE: don't put the className="ag-theme-alpine dbc dbc-ag-grid" here,
        # assign it to the outer container that's holding the grid.
    )
    return table


def get_button_download(button_id):
    return dbc.Button(
        gs.button_download,
        id=button_id,
        n_clicks=0,
        size="md",  # button size
        class_name="d-grid gap-2 col-8 btn-primary",  # bg-secondary text-light #mx-auto
    )
