"""This is the Gene Expression Query Layout."""

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_loading_spinners as dls
from dash import html, dcc

from snaptron_query.app import components, components_geq, global_strings as gs, inline_styles as styles


def get_form_geq():
    """Wrapper function for the Gene Expression Query components."""
    return [
        dbc.Row(
            [components.get_dropdown_compilation('id-input-compilation-geq')],
            className="g-5 form-control-sm",
            justify="start",
        ),
        dmc.Space(h=10),
        dbc.Row(
            dbc.Col(
                [
                    components_geq.get_checkbox_geq_optional_coordinates(),
                    components.get_tooltip("id-checkbox-use-coordinates", gs.geq_checkbox_help, 'left')
                ]
            ),
            class_name="g-0 form-control-sm",
            align='start'
        ),
        # ROW: Query Information
        dmc.Space(h=20),
        dbc.Row([dbc.Col([components.get_text('dbc', gs.geq_query_info)])], class_name="g-0"),
        dbc.Row(
            [
                dbc.Col([components.get_text('dmc', gs.geq_gene_id)],
                        width=3, align='center',  # this will align the text vertically wrt the text box next to it.
                        style={"border": styles.border_column}),
                dbc.Col([components.get_input(gs.geq_gene_id_placeholder, 'id-input-geq-gene-id')],
                        width=4, align='center',
                        style={"border": styles.border_column}),
                dbc.Col([components_geq.get_switch_normalize()],
                        class_name='mx-3',  # use d-flex justify-content-end  to right align it horizontally
                        style={"border": styles.border_column})
            ],
            class_name="g-0 form-control-sm",
            align='start'
        ),
        # ROW: Query Information - Coordinates in failure cases
        html.Div(
            dbc.Row(
                [
                    dbc.Col([components.get_text('dmc', gs.geq_gene_coord)],
                            width=3, align='center',
                            style={"border": styles.border_column}),
                    dbc.Col([components.get_input(gs.geq_gene_coord_placeholder, 'id-input-geq-gene-coord')],
                            width=4, align='center',
                            style={"border": styles.border_column})
                ],
                class_name="g-0 form-control-sm",
                align='start',
            ),
            id='id-row-query-gene-coordinates',
            style={'display': 'none'}
        ),
        dmc.Space(h=10),
        # ROW 3 Normalization Information
        dbc.Row([dbc.Col([components.get_text('dbc', gs.geq_normalized_info)])]),
        dbc.Row(
            [
                dbc.Col([components.get_text('dmc', gs.geq_gene_id)],
                        width=3, align='center',
                        style={"border": styles.border_column}),
                dbc.Col([components.get_input(gs.geq_gene_id_norm_placeholder,
                                              'id-input-geq-gene-id-norm', disabled='True')],
                        width=4, align='center',
                        style={"border": styles.border_column}),
            ],
            class_name="g-0 form-control-sm",
            align='start'
        ),
        # ROW Normalization Information - Coordinates in failure cases
        html.Div(
            dbc.Row([
                dbc.Col([components.get_text('dmc', gs.geq_gene_coord)],
                        width=3, align='center'),
                dbc.Col([components.get_input(gs.geq_gene_coord_norm_placeholder,
                                              'id-input-geq-gene-coord-norm', disabled='True')],
                        width=4, align='center')
            ],
                class_name="g-0 form-control-sm"
            ),
            id='id-row-norm-gene-coordinates',
            style={'display': 'none'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    components_geq.get_button_geq_results(),
                    style={"border": styles.border_column},
                    class_name="d-grid gap-0 col-12"  # this will make the button take over full width
                ),
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
                            dbc.Col(
                                [
                                    html.Div(get_form_geq())
                                ],
                                # TODO: picture may be inserted to the right when available
                                width=7
                            ),
                            dbc.Col(
                                [
                                    html.Img(
                                        src='assets/240318_gex.png',
                                        width='100%',  # this will force align the height to the column next to it
                                    )
                                ],
                                style={"border": styles.border_column},
                            )
                        ],
                        justify="start",
                    ),
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
                                    components.get_switch(switch_id='id-switch-geq-log-raw-box-plot',
                                                          switch_label=gs.geq_log_count, switch_on=True),
                                    dmc.Space(w=10),
                                    components.get_switch(switch_id='id-switch-geq-violin-raw-box-plot',
                                                          switch_label=gs.switch_violin),
                                ],
                                align='center',
                                className='d-flex justify-content-end',
                                style={'border': styles.border_column},
                            ),
                        ],
                        style={'border': styles.border_column},
                        className="g-0 form-control-sm"
                    ),
                    dbc.Row(
                        [
                            dcc.Graph(id='id-box-plot-geq')
                        ],
                        style={'border': styles.border_column},
                        class_name="g-0"
                    )
                ]
            )
        ],
        style=styles.boundary_style,
    )
    return card


def get_card_histogram_geq():
    card = dbc.Card(
        children=[
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    components.get_switch(switch_id='id-switch-geq-log-count-histogram',
                                                          switch_label=gs.geq_log_count, switch_on=True),
                                    dmc.Space(w=10),
                                    components.get_switch(switch_id='id-switch-geq-log-y-histogram',
                                                          switch_label=gs.switch_log_geq_hist_y)
                                ],
                                align='center',
                                className='d-flex justify-content-end',
                            )
                        ],
                        style={'border': styles.border_column},
                        className="g-0 form-control-sm"
                    ),
                    dbc.Row(
                        [
                            html.Div(dcc.Graph(id="id-row-graph-geq-hist"))
                        ],
                        class_name="g-0"
                    ),
                ]
            )
        ],
        style=styles.boundary_style,
    ),
    return card


def get_accordian_graphs_geq():
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row(
                        [
                            dbc.Col(id='id-geq-box-plot-col',
                                    children=[html.Div(get_card_box_plot_geq())],
                                    ),
                            dbc.Col(id='id-geq-histogram-col',
                                    children=[html.Div(get_card_histogram_geq())],
                                    )
                        ],
                    ),
                ],
                title=gs.graphs_group_title
            ),
        ],
    )


def get_card_table_geq():
    """Wrapper function for the table component
    """
    card = dmc.Card(
        id='id-card-table-geq',
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            components.get_button_download('id-button-geq-download', gs.download_original)
                        ],
                        width=2,
                        align='center',  # vertical alignment of the column
                        style={'border': styles.border_column}
                    ),
                    dbc.Col(),
                    dbc.Col(
                        [
                            components.get_switch_lock_data_with_table('id-switch-geq-lock-with-table', gs.switch_lock),
                            dmc.Space(w=10),
                            components.get_text('dmc', gs.switch_lock)
                        ],
                        width=3,
                        align='center',
                        className='d-flex justify-content-end',
                        style={'border': styles.border_column},
                    ),
                ],
                className="g-1",  # button too close to the table, needs some gutter
                justify='end'
            ),
            dmc.Space(h=10),
            dbc.Row(
                [
                    dbc.Container(
                        [
                            components.get_table(table_id='id-ag-grid-geq')
                        ],
                        className="ag-theme-alpine dbc dbc-ag-grid"
                    )
                ]
            )
        ],
        radius="md",
        style=styles.boundary_style,
    )
    return card


def get_layout_gene_expression_query():
    """This is the query/form layout for the gene expression query"""
    layout = dbc.Container(
        [
            # Top row  contains input form
            dmc.Space(h=30),  # this will create a space with the tab above it
            dbc.Row(
                [
                    get_accordian_form_geq(),
                ],
                style={"box-shadow": "1px 2px 7px 0px grey",
                       "border-radius": "10px"},
                className='g-0',  # no gutters in between the cards
            ),
            html.Div(id='id-alert-geq'),
            # Second row  of the layout contains the plots and graphs
            dmc.Space(h=20),
            dls.Propagate(show_initially=False,
                          color='var(--bs-secondary)',
                          children=[html.Div(id="id-loading-graph-geq")]
                          ),

            dbc.Row(
                [
                    get_accordian_graphs_geq(),
                ],
                id='id-display-graphs-geq',
                style={"box-shadow": "1px 2px 7px 0px grey",
                       "border-radius": "10px",
                       'visibility': 'hidden',
                       "height": "70px"
                       },
                className='g-0',  # no gutters in between the cards
            ),

            # Third row is the row containing the table
            dmc.Space(h=20),
            dls.Fade(
                show_initially=False,
                color='var(--bs-secondary)',
                children=dbc.Row(
                    [
                        get_card_table_geq()
                    ],
                    id='id-ag-grid-display-geq',
                    style={'display': 'None'}
                )
            )
        ],
    )
    return layout
