"""This is the Junction Inclusion Query Layout."""

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc

from snaptron_query.app import components as c_components, components_geq as components
from snaptron_query.app import global_strings as gs
from snaptron_query.app import inline_styles as styles


def get_geq_form():
    """Wrapper function for the Gene Expression Query components."""
    return [
        dbc.Row(
            [c_components.get_dropdown_compilation('id-input-compilation-geq')],
            className="g-5 form-control-sm",
            justify="start",
        ),
        # ROW 2 has the titles of the text boxes
        dmc.Space(h=10),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label(gs.geq_query, className='fs-6 fw-bold'),
                        dmc.Grid(
                            [
                                dmc.Col(components.get_text_gene_id('dmc')),
                                dmc.Col(components.get_input_gene_id()),
                                dmc.Col(components.get_text_gene_coordinates('dmc')),
                                dmc.Col(components.get_input_gene_coordinates()),
                            ],
                            gutter="xsm",
                            grow=True,  # each component will take the 12 width, don't need to do it manually
                        )
                    ],
                ),
                dbc.Col(
                    [
                        dmc.Grid(
                            [dmc.Col(components.get_switch_normalize(), span=12)],
                            gutter="sm",
                        ),
                    ],
                    width=2,
                    className='d-flex align-items-center',
                ),
                dbc.Col(
                    [
                        dbc.Label(gs.geq_normalized_info, className='fs-6 fw-bold'),
                        dmc.Grid(
                            [
                                dmc.Col(components.get_text_gene_id_norm('dmc'), ),
                                dmc.Col(components.get_input_gene_id_norm()),
                                dmc.Col(components.get_text_gene_coordinates_norm('dmc')),
                                dmc.Col(components.get_input_gene_coordinates_norm()),
                            ],
                            gutter="xsm",
                            grow=True,  # each component will take the 12 width, don't need to do it manually
                        ),
                    ]
                )
            ],
            className="g-5 form-control-sm",
        ),
        dbc.Row(
            [
                dbc.Col(
                    components.get_button_geq_results(),
                    style={"border": styles.border_column},
                    class_name="d-grid gap-0 col-12"  # this will make the button take over full width
                ),
            ],
            className="g-2 my-2",  # my-2: creates the padding at the top
        ),
    ]


def get_card_box_plot_geq():
    """Wrapper function for the box plot component in a card layout"""
    card = dbc.Card(
        id='id-card-box-plot-geq',
        children=[
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                width=1
                            ),
                            dbc.Col(
                                c_components.get_switch('id-switch-log-psi-box-plot-geq', gs.switch_log),
                                width=3
                            ),
                            dbc.Col(
                                c_components.get_switch('id-switch-violin-box-plot-geq', gs.switch_violin),
                                width=3
                            )

                        ],
                        style={'border': styles.border_column},
                        className="g-0 form-control-sm"
                    ),
                    dbc.Row(
                        [
                            dcc.Graph(id="id-box-plot-geq")
                        ],
                        style={'border': styles.border_column},
                        className="g-0"
                    )
                ]
            ),
        ],
        style=styles.boundary_style,
    )
    return card


def get_accordian_geq():
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div(get_geq_form())
                                ],
                                # TODO: picture may be inserted to the right when available
                                # width=8
                            ),
                        ],
                        justify="start",
                    ),
                ],
                title=gs.geq_form_title,
            )
        ]
    )


def get_accordian_graphs():
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row(
                        [
                            # row equally divided for the plots
                            dbc.Col(
                                [html.Div(get_card_box_plot_geq())]
                            ),
                            # dbc.Col(
                            #     [html.Div(get_card_histogram())]
                            # )
                        ]
                    ),
                ],
                title=gs.graphs_group_title
            ),
        ]
    )


def get_card_table():
    """Wrapper function for the table component
    """
    card = dmc.Card(
        id='id-card-table-geq',
        children=[
            dbc.Row(
                [
                    # dbc.Col(
                    #     [
                    #         components.get_button_download()
                    #     ],
                    #     width=2,
                    #     style={'border': styles.border_column}
                    # ),
                    dbc.Col(
                        [
                            components.get_switch_lock_data_with_table()
                        ],
                        width=3,
                        align='end',
                        style={'border': styles.border_column},
                    ),
                ],
                className="g-1",  # button too close to the table, needs some gutter
                justify='between'
            ),
            dbc.Row(
                [
                    dbc.Container(
                        [
                            components.get_table_geq()
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
                    get_accordian_geq(),
                ],
                style={"box-shadow": "1px 2px 7px 0px grey",
                       "border-radius": "10px"},
                className='g-0',  # no gutters in between the cards
            ),

            # Second row  of the layout contains the plots and graphs
            dmc.Space(h=20),
            dbc.Row(
                [
                    get_accordian_graphs(),
                ],
                style={"box-shadow": "1px 2px 7px 0px grey",
                       "border-radius": "10px"},
                className='g-0',  # no gutters in between the cards
            ),

            # Third row is the row containing the table
            dmc.Space(h=20),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            get_card_table()
                        ],
                        style={'border': styles.border_column}
                    )
                ]
            ),
        ],
    )
    return layout
