"""This is the Gene Expression Query Layout."""

import dash_bootstrap_components as dbc
import dash_loading_spinners as dls
import dash_mantine_components as dmc
from dash import html, dcc

from snaptron_query.app import components, components_geq, global_strings as gs, inline_styles as styles


def get_form_geq():
    """Wrapper function for the Gene Expression Query components."""
    return [
        # ROW: Select Compilation Information
        dbc.Row(
            [components.get_dropdown_compilation("id-input-compilation-geq")],
            className="g-0 form-control-sm",
            justify="start",
            style=styles.border_column,
        ),
        dmc.Space(h=10),
        dbc.Row(
            components_geq.get_checkbox_geq_optional_coordinates(), class_name="g-0 form-control-sm", align="start"
        ),
        # ROW: Query Information - gene id and normalization switch
        dmc.Space(h=20),
        dbc.Row([dbc.Col([components.get_text(gs.geq_query_info, "dbc")])], class_name="g-0"),
        dbc.Row(
            [  # use d-flex justify-content-end to right align it horizontally, align will align vertically
                dbc.Col([components.get_text(gs.geq_gene_id)], width=3, align="center", style=styles.border_column),
                dbc.Col(
                    [components.get_input(gs.geq_gene_id_placeholder, "id-input-geq-gene-id")],
                    width=4,
                    align="center",
                    style=styles.border_column,
                ),
                dbc.Col([components_geq.get_switch_normalize()], class_name="mx-3", style=styles.border_column),
            ],
            class_name="g-0 form-control-sm",
            align="start",
        ),
        # ROW: Query Information - Coordinates in failure cases
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        [components.get_text(gs.geq_gene_coord)], width=3, align="center", style=styles.border_column
                    ),
                    dbc.Col(
                        [components.get_input(gs.geq_gene_coord_placeholder, "id-input-geq-gene-coord")],
                        width=4,
                        align="center",
                        style=styles.border_column,
                    ),
                ],
                class_name="g-0 form-control-sm",
                align="start",
            ),
            id="id-row-query-gene-coordinates",
            style={"display": "none"},
        ),
        # ROW: Normalization Information - gene id
        dmc.Space(h=10),
        dbc.Row([dbc.Col([components.get_text(gs.geq_normalized_info, "dbc")])]),
        dbc.Row(
            [
                dbc.Col([components.get_text(gs.geq_gene_id)], width=3, align="center", style=styles.border_column),
                dbc.Col(
                    [
                        components.get_input(
                            gs.geq_gene_id_norm_placeholder, "id-input-geq-gene-id-norm", disabled="True"
                        )
                    ],
                    width=4,
                    align="center",
                    style=styles.border_column,
                ),
            ],
            class_name="g-0 form-control-sm",
            align="start",
        ),
        # ROW: Normalization Information - Coordinates in failure cases
        html.Div(
            dbc.Row(
                [
                    dbc.Col([components.get_text(gs.geq_gene_coord)], width=3, align="center"),
                    dbc.Col(
                        [
                            components.get_input(
                                gs.geq_gene_coord_norm_placeholder, "id-input-geq-gene-coord-norm", disabled="True"
                            )
                        ],
                        width=4,
                        align="center",
                    ),
                ],
                class_name="g-0 form-control-sm",
            ),
            id="id-row-norm-gene-coordinates",
            style={"display": "none"},
        ),
        # ROW: Main Calculate Button
        dbc.Row(
            [
                dbc.Col(
                    components.get_button_run_query("id-button-geq-run-query", gs.geq_button_run),
                    style=styles.border_column,
                    class_name="d-grid gap-0 col-12",
                )
                # this will make the button take over full width
            ],
            class_name="g-2 my-2",  # my-2: creates the padding at the top
        ),
    ]


def get_accordian_form_geq():
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row(
                        [
                            dbc.Col([html.Div(get_form_geq())], width=7),
                            dbc.Col(
                                [
                                    html.Img(src="assets/240318_gex.png", width="100%")
                                ],  # this will force align the height to the column next to it
                                style=styles.border_column,
                            ),
                        ],
                        justify="start",
                    )
                ],
                title=gs.geq_form_title,
            )
        ]
    )


def get_card_box_plot_geq():
    card = dbc.Card(
        children=[
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    components.get_info_icon_tooltip_bundle(
                                        "id-info-box-plot-geq", gs.help_box_plot_click, "left"
                                    )
                                ],
                                className="d-flex justify-content-start",
                                align="center",
                                style=styles.border_column,
                                width=1,
                            ),
                            dbc.Col(
                                [
                                    components.get_switch_box_plot_points("id-switch-geq-show-points"),
                                    dmc.Space(w=20),
                                    components.get_switch(
                                        switch_id="id-switch-geq-log-raw-box-plot",
                                        switch_label=gs.geq_log_count,
                                        switch_on=True,
                                    ),
                                    dmc.Space(w=10),
                                    components.get_switch(
                                        switch_id="id-switch-geq-violin-raw-box-plot", switch_label=gs.switch_violin
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
                    dbc.Row([dcc.Graph(id="id-geq-box-plot")], class_name="g-0", style=styles.border_column),
                ]
            )
        ],
        style=styles.boundary_style,
    )
    return card


def get_card_histogram_geq():
    card = (
        dbc.Card(
            children=[
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        components.get_switch(
                                            switch_id="id-switch-geq-log-count-histogram",
                                            switch_label=gs.geq_log_count,
                                            switch_on=True,
                                        ),
                                        dmc.Space(w=10),
                                        components.get_switch(
                                            switch_id="id-switch-geq-log-y-histogram",
                                            switch_label=gs.switch_log_geq_hist_y,
                                        ),
                                    ],
                                    className="d-flex justify-content-end",
                                    align="center",
                                )
                            ],
                            className="g-0 form-control-sm",
                        ),
                        dbc.Row([html.Div(dcc.Graph(id="id-geq-histogram"))], class_name="g-0"),
                    ]
                )
            ],
            style=styles.boundary_style,
        ),
    )
    return card


def get_accordian_graphs_geq():
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row(
                        [
                            dbc.Col(id="id-geq-box-plot-col", children=[html.Div(get_card_box_plot_geq())]),
                            dbc.Col(id="id-geq-histogram-col", children=[html.Div(get_card_histogram_geq())]),
                        ]
                    )
                ],
                title=gs.graphs_group_title,
            )
        ]
    )


def get_card_table_geq():
    """Wrapper function for the table component"""
    card = dmc.Card(
        id="id-card-table-geq",
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        components.get_button_download("id-button-geq-download"),
                        width=2,
                        align="center",
                        style=styles.border_column,
                    ),
                    dbc.Col(
                        components.get_radio_items_download_options("id-geq-download-options"),
                        width=3,
                        align="center",
                        style=styles.border_column,
                    ),
                    dbc.Col(),
                    dbc.Col(  # RESET TABLE
                        components.get_button_reset("id-button-geq-reset"),
                        width=1,
                        align="center",
                        className="d-flex justify-content-end",
                        style=styles.border_column,
                    ),
                    dbc.Col(  # LOCKS
                        components.get_switch_lock_data_with_table(
                            "id-switch-geq-lock-with-table", "id-geq-lock", "id-geq-unlock"
                        ),
                        width=1,
                        align="center",
                        style=styles.border_column,
                        className="d-flex justify-content-end",
                    ),
                ],
                className="g-1",
                justify="end",
            ),
            dmc.Space(h=10),
            dbc.Row(
                [
                    dbc.Container(
                        [components.get_table(table_id="id-ag-grid-geq")], className="ag-theme-alpine dbc dbc-ag-grid"
                    )
                ]
            ),
        ],
        radius="md",
        style=styles.boundary_style,
    )
    return card


def get_layout_gene_expression_query():
    """This is the query/form layout for the gene expression query"""
    layout = dbc.Container(
        [
            # FORM
            dmc.Space(h=30),  # this will create a space with the tab above it
            dbc.Row([get_accordian_form_geq()], style=styles.section, className="g-0"),
            # ALERT
            html.Div(id="id-alert-geq"),
            dmc.Space(h=50),
            # dls.Propagate(
            #     show_initially=False, color="var(--bs-secondary)", children=[html.Div(id="id-loading-graph-geq")]
            # ),
            dls.Propagate(
                show_initially=False, color="var(--bs-secondary)", children=[html.Div(id="id-loading-table-geq")]
            ),
            # GRAPHS
            dbc.Row(
                [get_accordian_graphs_geq()],
                id="id-display-graphs-geq",
                className="g-0",
                style={**styles.section, **styles.section_vis},
            ),
            # TABLE
            dmc.Space(h=20),
            dbc.Row([get_card_table_geq()], id="id-ag-grid-display-geq", style={"display": "None"}),
        ],
    )
    return layout
