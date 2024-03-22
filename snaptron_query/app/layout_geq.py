"""This is the Gene Expression Query Layout."""

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html

from snaptron_query.app import components, components_geq, global_strings as gs, inline_styles as styles


def get_form_geq():
    """Wrapper function for the Gene Expression Query components."""
    return [
        dbc.Row(
            [components.get_dropdown_compilation('id-input-compilation-geq')],
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
                                dmc.Col(components.get_text('dmc', gs.geq_gene_id)),
                                dmc.Col(components.get_input(gs.geq_gene_id_placeholder, 'id-input-geq-gene-id')),
                                dmc.Col(components.get_text(dmc, gs.geq_gene_coord)),
                                dmc.Col(components.get_input(gs.geq_gene_coord_placeholder, 'id-input-geq-gene-coord')),
                            ],
                            gutter="xsm",
                            grow=True,  # each component will take the 12 width, don't need to do it manually
                        )
                    ],
                ),
                dbc.Col(
                    [
                        dmc.Grid(
                            [dmc.Col(components_geq.get_switch_normalize(), span=12)],
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
                                dmc.Col(components.get_text('dmc', gs.geq_gene_id)),
                                dmc.Col(components.get_input(gs.geq_gene_id_norm_placeholder,
                                                             'id-input-geq-gene-id-norm', disabled='True')),
                                dmc.Col(components.get_text('dmc', gs.geq_gene_coord)),
                                dmc.Col(components.get_input(gs.geq_gene_coord_norm_placeholder,
                                                             'id-input-geq-gene-coord-norm', disabled='True')),
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
                    components_geq.get_button_geq_results(),
                    style={"border": styles.border_column},
                    class_name="d-grid gap-0 col-12"  # this will make the button take over full width
                ),
            ],
            className="g-2 my-2",  # my-2: creates the padding at the top
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


def get_accordian_graphs_geq():
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                width=1
                            ),
                            dbc.Col(
                                components.get_switch(switch_id='id-switch-geq-log-raw-box-plot',
                                                      switch_label=gs.switch_log),
                                width=3
                            ),
                            dbc.Col(
                                components.get_switch(switch_id='id-switch-geq-violin-raw-box-plot',
                                                      switch_label=gs.switch_violin),
                                width=3
                            )

                        ],
                        style={'border': styles.border_column},
                        className="g-0 form-control-sm"
                    ),
                    dbc.Row(id='id-row-graph-geq', style={'border': styles.border_column}, class_name="g-0")
                ],
                title=gs.graphs_group_title
            ),
        ]
    )


def get_card_table_geq():
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
                            components.get_switch_lock_data_with_table('id-switch-geq-lock-with-table', gs.switch_lock)
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
                            components_geq.get_table_geq()
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

            # Second row  of the layout contains the plots and graphs
            dmc.Space(h=20),
            dbc.Row(
                [
                    get_accordian_graphs_geq(),
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
                            get_card_table_geq()
                        ],
                        style={'border': styles.border_column}
                    )
                ]
            ),
        ],
    )
    return layout
