"""
    This is the Junction Inclusion Query Layout.
"""

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc

import components_jiq as components
import global_strings
import inline_styles as styles


# TODO: texts on the form are still using DMC, DBC puts a margin on the bottom, investigate.
def get_jiq_form():
    """
        Grid and components are defined with dash bootstrap components (dbc)
        The width of the top and bottom row is set to fill the row
        The width of the junction textbox column is set to 3 so the rest of the columns balance out
    """
    return [
        dbc.Row(
            [
                dbc.Col(
                    components.get_dropdown_compilation(),
                    style={
                        "border": styles.border_column,
                    },
                ),
            ],
            className="g-0 form-control-sm",
            justify="start",
        ),

        # ROW 2 has the titles of the textbooks so subsequent rows
        dbc.Row(
            [
                dbc.Col(
                    width=2,
                    style={
                        "border": styles.border_column,
                    },
                    align='center',  # vertical alignment: center start end
                    # className='col-md-auto mx-2',  # will fit the column to the text
                ),
                dbc.Col(
                    components.get_text_chromosome('dmc'),
                    # TODO: switching to dbc puts a space under the text, needs investigation
                    width=2,
                    style={
                        "border": styles.border_column,
                    },
                    align='center',  # vertical alignment: center start end
                    className='mx-0.5'
                ),
                dbc.Col(
                    components.get_text_inclusion_junction('dmc'),
                    # TODO: switching to dbc puts a space under the text, needs investigation
                    width=3,
                    style={
                        "border": styles.border_column,
                    },
                    align='center',  # vertical alignment: center start end
                    className='mx-0.5'
                ),
                dbc.Col(
                    components.get_text_exclusion_junction('dmc'),
                    # TODO: switching to dbc puts a space under the text, needs investigation
                    width=3,
                    style={
                        "border": styles.border_column,
                    },
                    align='center',  # vertical alignment: center start end
                ),
                dbc.Col(
                    width=2,
                    style={
                        "border": styles.border_column,
                    },
                ),
            ],
            # border border-primary: add for border and gutter debugging
            className="g-0 form-control-sm",
            justify="start",
        ),
        dbc.Row(
            [
                dbc.Col(
                    components.get_text_junction('dmc'),
                    width=2,
                    style={
                        "border": styles.border_column,
                    },
                    align='center',  # vertical alignment: center start end
                    className='ml-auto',  # will justify to the right side
                ),
                dbc.Col(
                    components.get_input_chrom(),
                    width=2,
                    style={
                        "border": styles.border_column,
                    },
                    align='center',  # vertical alignment: center start end
                    className='mx-0.5'
                ),
                dbc.Col(
                    components.get_input_inc_junction(),
                    width=3,
                    style={
                        "border": styles.border_column,
                    },
                    align='center',  # vertical alignment: center start end
                    className='mx-0.5'
                ),
                dbc.Col(
                    components.get_input_exc_junction(),
                    width=3,
                    style={
                        "border": styles.border_column,
                    },
                    align='center',  # vertical alignment: center start end
                ),
                dbc.Col(
                    components.get_button_add_junction(),
                    width=2,
                    style={
                        "border": styles.border_column,
                    },
                    align='center',  # vertical alignment: center start end
                    className='col-md-auto'  # will fit the column to the text
                ),
            ],
            # border border-danger: add for border and gutter debugging
            className="g-1 form-control-sm",
            justify="start",
        ),
        dbc.Row(
            dbc.Col(
                components.get_button_generate_results(),
                style={
                    "border": styles.border_column,
                },
                # className="d-grid gap-2 d-md-flex justify-content-md-end", # will justify to the right side
            ),
            # ROW style notes:
            # gap-3: does not apply to the row
            # my-2: creates the padding at the top
            # border border-primary : add  to see the border for debugging
            className="g-2 my-2",
        ),
    ]


def get_card_histogram():
    """
        Wrapper function for the histogram component in a card layout
    """
    card = dbc.Card(
        id='id-card-histogram',
        children=[
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            components.get_switch_log_psi('dmc')
                        ],
                        style={'border': styles.border_column, }
                    ),
                    dbc.Row(
                        [
                            html.Div(dcc.Graph(id="id-histogram"))
                        ],
                        style={'border': styles.border_column}
                    )
                ]
            ),
        ],
        style=styles.boundary_style,
    )
    return card


def get_card_box_plot():
    """
        Wrapper function for the box plot component in a card layout
    """
    card = dbc.Card(
        id='id-card-box-plot',
        children=[
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            components.get_switch_log_psi('dmc')
                        ],
                        style={'border': styles.border_column}
                    ),
                    dbc.Row(
                        [
                            html.Div(dcc.Graph(id="id-box-plot"))
                        ],
                        style={'border': styles.border_column}
                    )
                ]
            ),
        ],
        style=styles.boundary_style,
    )
    return card


def get_card_table():
    """
        A wrapper function that puts the table in a dmc card container
        Card layout uses dbc grid layout
    """
    card = dmc.Card(
        id='id-card-table',
        children=[
            # TODO: may need a card section for the table, need to finalize this
            # dmc.CardSection(
            #     dmc.Title('Query Results', order=3, align='center'),
            # ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            components.get_button_download()
                        ],
                        width=2,
                        # align='center',
                        style={'border': styles.border_column}
                        # className='ml-auto'
                    ),
                    dbc.Col(
                        [
                            components.get_switch_lock_data_with_table('dbc')
                        ],
                        width=3,
                        align='end',
                        style={'border': styles.border_column},
                        # className='ms-auto' # will justify to the right
                    ),
                ],
                className="g-1",  # button too close to the table, needs some gutter
                justify='between'
            ),
            dbc.Row(
                [
                    dbc.Container(
                        [
                            components.get_table_jiq()
                        ],
                        # TODO: this will change the table theme to follow dbc
                        className="ag-theme-alpine dbc dbc-ag-grid"
                    )
                ]
            )
        ],
        # withBorder=True,
        # shadow="md",
        radius="md",
        style=styles.boundary_style,
    )
    return card


def get_accordian_jiq():
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div(get_jiq_form())
                                ],
                                width=8
                            ),
                            dbc.Col(
                                [
                                    html.Img(
                                        src='assets/junction_query.png',
                                        # withPlaceholder=True,
                                        width='80%',
                                    )
                                ]
                            )
                        ]
                    ),
                ],
                title=global_strings.jiq_form_title,
            ),
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
                                [
                                    html.Div(get_card_box_plot())
                                ],
                            ),
                            dbc.Col(
                                [
                                    html.Div(get_card_histogram())
                                ]
                            )
                        ]
                    ),
                ],
                title=global_strings.jiq_graphs_group_title
            ),
        ]
    )


def get_layout_junction_inclusion():
    """
        This is the query/form layout for the junction inclusion query
    """
    layout = dbc.Container(
        [
            # Top row  contains input form
            dmc.Space(h=30),  # this will create a space with the tab above it
            dbc.Row(
                [
                    get_accordian_jiq(),
                ],

                # TODO: using the general boundary messes with the layout, need to figure out why?
                # style=styles.boundary_style,
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

                # TODO: using the general boundary messes with the layout, need to figure out why?
                # style=styles.boundary_style,
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
        # className='shadow-sm' # puts the shadow background around the div
    )
    return layout
