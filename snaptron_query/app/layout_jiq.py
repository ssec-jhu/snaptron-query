"""This is the Junction Inclusion Query Layout."""

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_loading_spinners as dls
from dash import html, dcc

from snaptron_query.app import components, components_jiq, global_strings as gs, icons
from snaptron_query.app import inline_styles as styles


def create_junction_row(index):
    return [
        dbc.Col(components_jiq.get_text_junction(index), width=2, align="center", style=styles.border_column),
        dbc.Col(
            components.get_input(gs.jiq_input_inc_placeholder, f"id-input-jiq-inc-junc-{index}"),
            width=4,
            className="mx-0.5",
            align="center",
            style=styles.border_column,
        ),
        dbc.Col(
            components.get_input(gs.jiq_input_exc_placeholder, f"id-input-jiq-exc-junc-{index}"),
            width=4,
            align="center",
            style=styles.border_column,
        ),
    ]


def get_form_jiq():
    """Wrapper function for the Junction Inclusion Query components.
    The width of the top and bottom row is set to fill the row
    """
    return [
        # ROW: Select Compilation Information
        dbc.Row(
            [components.get_dropdown_compilation("id-input-compilation-jiq")],
            className="g-0 form-control-sm",
            justify="start",
            style=styles.border_column,
        ),
        # ROW: the titles of the text boxes
        dbc.Row(
            [
                dbc.Col(width=2, style=styles.border_column),
                dbc.Col(
                    components.get_text(gs.jiq_input_inc_txt),
                    width=4,
                    className="mx-0.5",
                    align="center",
                    style=styles.border_column,
                ),
                dbc.Col(components.get_text(gs.jiq_input_exc_txt), width=4, align="center", style=styles.border_column),
                dbc.Col(width=2, style=styles.border_column),
            ],
            className="g-0 form-control-sm",
            justify="start",
        ),
        # ROW: JIQ form components
        html.Div(
            id="id-jiq-input-container",
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            components_jiq.get_text_junction(0), width=2, align="center", style=styles.border_column
                        ),
                        dbc.Col(
                            components.get_input(gs.jiq_input_inc_placeholder, "id-input-jiq-inc-junc-0"),
                            width=4,
                            className="mx-0.5",
                            align="center",
                            style=styles.border_column,
                        ),
                        dbc.Col(
                            components.get_input(gs.jiq_input_exc_placeholder, "id-input-jiq-exc-junc-0"),
                            width=4,
                            align="center",
                            style=styles.border_column,
                        ),
                        dbc.Col(
                            components_jiq.get_button_add_junction(),  # fit column to text
                            width=2,
                            className="col-md-auto",
                            align="center",
                            style=styles.border_column,
                        ),
                    ],
                    className="g-1 form-control-sm",
                    justify="start",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            components_jiq.get_text_junction(1), width=2, align="center", style=styles.border_column
                        ),
                        dbc.Col(
                            components.get_input(gs.jiq_input_inc_placeholder, "id-input-jiq-inc-junc-1"),
                            width=4,
                            className="mx-0.5",
                            align="center",
                            style=styles.border_column,
                        ),
                        dbc.Col(
                            components.get_input(gs.jiq_input_exc_placeholder, "id-input-jiq-exc-junc-1"),
                            width=4,
                            align="center",
                            style=styles.border_column,
                        ),
                    ],
                    className="g-1 form-control-sm",
                    justify="start",
                    id="id-row-input-jiq-1",
                    style={"display": "none"},
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            components_jiq.get_text_junction(2), width=2, align="center", style=styles.border_column
                        ),
                        dbc.Col(
                            components.get_input(gs.jiq_input_inc_placeholder, "id-input-jiq-inc-junc-2"),
                            width=4,
                            className="mx-0.5",
                            align="center",
                            style=styles.border_column,
                        ),
                        dbc.Col(
                            components.get_input(gs.jiq_input_exc_placeholder, "id-input-jiq-exc-junc-2"),
                            width=4,
                            align="center",
                            style=styles.border_column,
                        ),
                    ],
                    className="g-1 form-control-sm",
                    justify="start",
                    id="id-row-input-jiq-2",
                    style={"display": "none"},
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            components_jiq.get_text_junction(3), width=2, align="center", style=styles.border_column
                        ),
                        dbc.Col(
                            components.get_input(gs.jiq_input_inc_placeholder, "id-input-jiq-inc-junc-3"),
                            width=4,
                            className="mx-0.5",
                            align="center",
                            style=styles.border_column,
                        ),
                        dbc.Col(
                            components.get_input(gs.jiq_input_exc_placeholder, "id-input-jiq-exc-junc-3"),
                            width=4,
                            align="center",
                            style=styles.border_column,
                        ),
                    ],
                    className="g-1 form-control-sm",
                    justify="start",
                    id="id-row-input-jiq-3",
                    style={"display": "none"},
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            components_jiq.get_text_junction(4), width=2, align="center", style=styles.border_column
                        ),
                        dbc.Col(
                            components.get_input(gs.jiq_input_inc_placeholder, "id-input-jiq-inc-junc-4"),
                            width=4,
                            className="mx-0.5",
                            align="center",
                            style=styles.border_column,
                        ),
                        dbc.Col(
                            components.get_input(gs.jiq_input_exc_placeholder, "id-input-jiq-exc-junc-4"),
                            width=4,
                            align="center",
                            style=styles.border_column,
                        ),
                    ],
                    className="g-1 form-control-sm",
                    justify="start",
                    id="id-row-input-jiq-4",
                    style={"display": "none"},
                ),
            ],
        ),
        # ROW: Main Calculate Button
        dbc.Row(
            [
                dbc.Col(
                    components.get_button_run_query("id-button-jiq-generate-results", gs.jiq_button_run),
                    style=styles.border_column,
                    class_name="d-grid gap-0 col-12",
                )  # this will make the button take over full width
            ],
            className="g-2 my-2",  # my-2: creates the padding at the top
        ),
    ]


def get_card_histogram_jiq():
    """Wrapper function for the histogram component in a card layout"""
    card = dbc.Card(
        children=[
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    components.get_switch(
                                        switch_id="id-switch-jiq-log-psi-histogram",
                                        switch_label=gs.jiq_log_psi,
                                        switch_on=True,
                                    ),
                                    dmc.Space(w=10),
                                    components.get_switch(
                                        switch_id="id-switch-jiq-log-y-histogram", switch_label=gs.switch_log_geq_hist_y
                                    ),
                                ],
                                className="d-flex justify-content-end",
                                align="center",
                            ),
                        ],
                        className="g-0 form-control-sm",
                    ),
                    dbc.Row([html.Div(dcc.Graph(id="id-histogram-jiq"))], style=styles.border_column),
                ]
            )
        ],
        style=styles.boundary_style,
    )
    return card


def get_card_box_plot_jiq():
    """Wrapper function for the box plot component in a card layout"""
    card = dbc.Card(
        children=[
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    components.get_info_icon_tooltip_bundle(
                                        "id-info-box-plot-jiq", gs.help_box_plot_click, "left"
                                    )
                                ],
                                className="d-flex justify-content-start",
                                align="center",
                                style=styles.border_column,
                            ),
                            dbc.Col(
                                [
                                    components.get_switch(
                                        switch_id="id-switch-jiq-log-psi-box-plot",
                                        switch_label=gs.jiq_log_psi,
                                        switch_on=True,
                                    ),
                                    dmc.Space(w=10),
                                    components.get_switch(
                                        switch_id="id-switch-jiq-violin-box-plot", switch_label=gs.switch_violin
                                    ),
                                ],
                                className="d-flex justify-content-end",
                                align="center",
                                style=styles.border_column,
                            ),
                        ],
                        className="g-0 form-control-sm",
                        style=styles.border_column,
                    ),
                    dbc.Row([dcc.Graph(id="id-box-plot-jiq")], className="g-0", style=styles.border_column),
                ]
            )
        ],
        style=styles.boundary_style,
    )
    return card


def get_card_table_jiq():
    """Wrapper function for the table component"""
    card = dmc.Card(
        children=[
            dbc.Row(
                [  # align='center' for vertical alignment of the column
                    dbc.Col(
                        components.get_button_download("id-button-jiq-download"),
                        width=2,
                        align="center",
                        style=styles.border_column,
                    ),
                    dbc.Col(
                        components.get_radio_items_download_options("id-jiq-download-options"),
                        width=3,
                        align="center",
                        style=styles.border_column,
                    ),
                    dbc.Col(
                        [components.get_text([icons.info, gs.jiq_help_table])],
                        width=3,
                        className="d-flex justify-content-start",
                        align="center",
                        style=styles.border_column,
                    ),
                    dbc.Col(),
                    dbc.Col(  # RESET TABLE
                        components.get_button_reset("id-button-jiq-reset"),
                        width=1,
                        align="center",
                        className="d-flex justify-content-end",
                        style=styles.border_column,
                    ),
                    dbc.Col(  # LOCKS
                        components.get_switch_lock_data_with_table(
                            "id-switch-jiq-lock-with-table", "id-jiq-lock", "id-jiq-unlock"
                        ),
                        width=1,
                        align="center",
                        className="d-flex justify-content-end",
                        style=styles.border_column,
                    ),
                ],
                className="g-1",
                justify="end",
            ),
            dmc.Space(h=10),
            dbc.Row(
                [
                    dbc.Container(
                        [components.get_table(table_id="id-ag-grid-jiq")], className="ag-theme-alpine dbc dbc-ag-grid"
                    )
                ]
            ),
        ],
        radius="md",
        style=styles.boundary_style,
    )
    return card


def get_accordian_form_jiq():
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row(
                        [
                            dbc.Col([html.Div(get_form_jiq())], width=8),
                            dbc.Col(
                                [
                                    html.Img(src="assets/junction_query.png", width="100%")
                                ],  # this will force align the height to the column next to it
                                style=styles.border_column,
                            ),
                        ],
                        justify="start",
                    )
                ],
                title=gs.jiq_form_title,
            )
        ]
    )


def get_accordian_graphs_jiq():
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row(
                        [  # row equally divided for the plots
                            dbc.Col(id="id-jiq-box-plot-col", children=[html.Div(get_card_box_plot_jiq())]),
                            dbc.Col(id="id-jiq-histogram-col", children=[html.Div(get_card_histogram_jiq())]),
                        ]
                    )
                ],
                title=gs.graphs_group_title,
            )
        ]
    )


def get_layout_junction_inclusion():
    """This is the query/form layout for the junction inclusion query"""
    layout = dbc.Container(
        [
            # FORM
            dmc.Space(h=30),  # this will create a space with the tab above it
            dbc.Row([get_accordian_form_jiq()], style=styles.section, className="g-0"),
            # ALERT
            html.Div(id="id-alert-jiq"),
            # spinners in the background until the graphs load
            dmc.Space(h=50),
            # dls.Propagate(
            #     show_initially=False, color="var(--bs-secondary)", children=[html.Div(id="id-loading-graph-jiq")]
            # ),
            dls.Fade(show_initially=False, color="var(--bs-secondary)", children=[html.Div(id="id-loading-table-jiq")]),
            # ROW: the plots and graphs
            dbc.Row(
                [get_accordian_graphs_jiq()],
                id="id-display-graphs-jiq",
                className="g-0",
                style={**styles.section, **styles.section_vis},
            ),
            # Row: Table
            dmc.Space(h=20),
            dbc.Row([get_card_table_jiq()], id="id-ag-grid-display-jiq", style={"display": "None"}),
        ],
    )
    return layout
