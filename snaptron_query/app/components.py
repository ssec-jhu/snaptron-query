from enum import Enum

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc
import dash_ag_grid as dag

from snaptron_query.app import global_strings as gs, icons


def get_text(string, component_style="dmc"):
    """Wrapper function to retrieve the text used  queries"""
    if component_style == "dmc":
        return dmc.Text(string, weight=500, size="sm", span=True)  # 500=semi bold
    elif component_style == "dbc":
        return dbc.Label(string, className="fw-bold")
    else:
        return html.Label(string)


def get_input(input_placeholder, input_id, disabled=False):
    """Wrapper function to retrieve the texted boxes used in the queries"""
    return dbc.Input(id=input_id, placeholder=input_placeholder, size="sm", debounce=True, disabled=disabled)


def get_dropdown_compilation(component_id):
    """Wrapper function to retrieve the dropdown component"""
    return html.Div(
        [
            html.Span(
                [
                    # create a bundle with the tooltip icon here
                    dbc.Label(gs.drop_compilation, className="fw-bold me-2 mt-1"),
                    get_info_icon_tooltip_bundle(f"{component_id}_info", gs.drop_compilation_help, "top"),
                ],
                style={"display": "flex"},
            ),
            dcc.Dropdown(id=component_id, options=gs.compilation_names_dict, value=gs.compilation_srav3h),
        ],
        className="dbc",
    )


def get_button_run_query(button_id, button_string):
    """Wrapper function to retrieve the button component"""
    return dbc.Button(id=button_id, n_clicks=0, class_name="btn-primary", size="md", children=button_string)


def get_switch(switch_id, switch_label, switch_on=False):
    return dbc.Switch(id=switch_id, label=switch_label, value=switch_on)


def get_switch_lock_data_with_table(switch_id, lock_id, unlock_id):
    return [
        get_text(icons.get_lock_opened(unlock_id)),
        dmc.Space(w=8),
        dbc.Switch(
            id=switch_id,  # label=switch_label,
            # dbc switch follows the text size of its label, so you can use something like class_name="fs-6"
            # https://community.plotly.com/t/dbc-switch-make-larger/80146
            value=True,
        ),
        dmc.Space(w=3),
        get_text(icons.get_lock_closed(lock_id)),
        # dmc.Space(w=10),
        # components.get_text(gs.switch_lock),
        get_tooltip(switch_id, gs.switch_lock_help, "top"),
    ]


def get_switch_box_plot_points(switch_id):
    return html.Span(
        [
            get_text(gs.box_plot_points_outlier),
            dmc.Space(w=10),
            dbc.Switch(
                id=switch_id,
                # dbc switch follows the text size of its label, so you can use something like class_name="fs-6"
                # https://community.plotly.com/t/dbc-switch-make-larger/80146
                value=False,
            ),
            dmc.Space(w=3),
            get_text(gs.box_plot_points_all),
            get_tooltip(switch_id, gs.box_plot_points_tip, "top"),
        ],
        style={"display": "flex"},
    )


def get_alert(alert_message):
    return [
        dmc.Space(h=20),
        dbc.Alert(children=f"{alert_message}", duration=4000, dismissable=True, is_open=True, class_name="user-alert"),
    ]


def get_table(table_id):
    table = dag.AgGrid(
        id=table_id,
        persistence=True,  # https://community.plotly.com/t/how-to-add-persistence-to-dash-ag-grid/74944
        style={"height": 700},
        defaultColDef={
            # do NOT set "flex": 1 in default col def as it overrides all the column widths
            "sortable": True,
            "resizable": True,
            "filter": True,
            # Set BOTH items below to True for header to wrap text
            "wrapHeaderText": True,
            "autoHeaderHeight": True,
        },
        dashGridOptions={
            "rowSelection": "multiple",
            "checkboxSelection": "True",
            "isRowSelectable": {"function": "log(params)"},
            "pagination": True,
            # this will set the number of items per page be a function of the height
            # if we load too many rows that are not visible, the graphics is not smart enough
            # to hide what is not visible, so it takes longer for the page to load
            "paginationAutoPageSize": True,
            # Tooltip options https://dashaggridexamples.pythonanywhere.com/tooltips
            "tooltipShowDelay": 0,  # Makes tooltip show immediately.  Default 2000ms
            # "tooltipHideDelay": 3000,  # Hides tooltip after 3000ms
            "tooltipInteraction": True,  # Won't hide when hover on toolip.  Can select and copy content.
            # https://ag-grid.com/javascript-data-grid/selection-overview/#cell-text-selection
            "enableCellTextSelection": True,
            "ensureDomOrder": True,
            # ag-grid has issues with headers with dots in the string, it will show empty cells. known
            # issue https://community.plotly.com/t/dash-ag-grid-showing-empty-cells-where-there-shouldnt
            # -be-empty-cells/76108/2
            "suppressFieldDotNotation": True,
        },
        # NOTE: don't put the className="ag-theme-alpine dbc dbc-ag-grid" here,
        # assign it to the outer container that's holding the grid.
    )
    return table


def get_button_download(button_id):
    return [
        dbc.Button(
            children=html.Span([icons.download, gs.download_results]),
            id=button_id,
            n_clicks=0,
            size="md",
            class_name="d-grid gap-2 col-12 btn-primary",
        ),
        get_tooltip(button_id, gs.help_download, "left"),
    ]


class DownloadType(Enum):
    ORIGINAL = 1
    FILTERED = 2


def get_radio_items_download_options(radio_id):
    # Note: tooltips will only bind with the first radio_id that comes in, the GEQ one that comes after will not bind
    # the tooltips because the tooltip id is the same as the radio item id not the radio button group as a whole
    id_1 = f"{radio_id}_1"
    id_2 = f"{radio_id}_2"
    return [
        dbc.RadioItems(
            options=[
                {
                    "label": get_text(html.Span(id=id_1, children=[icons.download, gs.download_original])),
                    "value": DownloadType.ORIGINAL.value,
                },
                {
                    "label": get_text(html.Span(id=id_2, children=[icons.download, gs.download_filtered])),
                    "value": DownloadType.FILTERED.value,
                },
            ],
            value=DownloadType.ORIGINAL.value,
            id=radio_id,
            inline=True,
        ),
        get_tooltip(id_1, gs.help_download_mode_unfiltered, "top"),
        get_tooltip(id_2, gs.help_download_mode_filtered, "top"),
    ]


def get_tooltip(target_id, string, tip_placement):
    return dbc.Tooltip(
        children=string,
        is_open=False,
        target=target_id,
        placement=tip_placement,
        # some style is overriding the tooltip and making the strings all caps
        # overriding the text transform here
        style={"text-transform": "none"},
    )


def get_button_reset(button_id):
    return [
        dbc.Button(
            html.Span([icons.reset]),
            id=button_id,
            n_clicks=0,
            outline=True,
            size="md",  # button size
            # Note: setting the col-12 will fill the dbc column. since this is an icon I am removing that option.
            # Note: if you set the color using "color" parameter, it would not apply the outline and button
            # will be a button with background. Setting it as style will remove the background and color the text
            style={"color": "var(--bs-primary)"},
            class_name="icon-button",
        ),
        get_tooltip(button_id, gs.help_reset, "top"),
    ]


def get_info_icon_tooltip_bundle(info_icon_id, help_string, location):
    return html.Div(
        [dmc.Text(icons.info, id=info_icon_id, weight=500, size="md"), get_tooltip(info_icon_id, help_string, location)]
    )
