"""This is the Junction Inclusion Query Layout."""

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc

from snaptron_query.app import components_jiq as components
from snaptron_query.app import global_strings
from snaptron_query.app import inline_styles as styles


def get_jiq_form():
    """Wrapper function for the Junction Inclusion Query components.
    The width of the top and bottom row is set to fill the row
    """
    return [
        dbc.Row(
            [
                dbc.Col(
                    components.get_dropdown_compilation(),
                    style={"border": styles.border_column},
                ),
            ],
            className="g-0 form-control-sm",
            justify="start",
        ),

        # ROW 2 has the titles of the text boxes
        dbc.Row(
            [
                dbc.Col(
                    width=2,
                    style={"border": styles.border_column},
                    align='center',  # vertical alignment: center start end
                ),
                dbc.Col(
                    components.get_text_inclusion_junction('dmc'),
                    width=4,
                    style={"border": styles.border_column},
                    align='center',
                    className='mx-0.5'
                ),
                dbc.Col(
                    components.get_text_exclusion_junction('dmc'),
                    width=4,
                    style={"border": styles.border_column},
                    align='center',
                ),
                dbc.Col(
                    width=2,
                    style={"border": styles.border_column},
                ),
            ],
            className="g-0 form-control-sm",
            justify="start",
        ),
        # ROW 3 has the form components
        dbc.Row(
            [
                dbc.Col(
                    components.get_text_junction('dmc'),
                    width=2,
                    style={"border": styles.border_column},
                    align='center',
                ),
                dbc.Col(
                    components.get_input_inc_junction(),
                    width=4,
                    style={"border": styles.border_column},
                    align='center',
                    className='mx-0.5'
                ),
                dbc.Col(
                    components.get_input_exc_junction(),
                    width=4,
                    style={"border": styles.border_column},
                    align='center',
                ),
                dbc.Col(
                    components.get_button_add_junction(),
                    width=2,
                    style={"border": styles.border_column},
                    align='center',
                    className='col-md-auto'  # will fit the column to the text
                ),
            ],
            className="g-1 form-control-sm",
            justify="start",
        ),
        dbc.Row(
            [
                dbc.Col(
                    components.get_button_generate_results(),
                    style={"border": styles.border_column},
                    class_name="d-grid gap-0 col-12"  # this will make the button take over full width
                ),
            ],
            className="g-2 my-2",  # my-2: creates the padding at the top
        ),
    ]


def get_card_histogram():
    """Wrapper function for the histogram component in a card layout"""
    card = dbc.Card(
        id='id-card-histogram',
        children=[
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            components.get_switch_log_psi_histogram()
                        ],
                        style={'border': styles.border_column}
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
    """Wrapper function for the box plot component in a card layout"""
    card = dbc.Card(
        id='id-card-box-plot',
        children=[
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            components.get_switch_log_psi_box_plot()
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
    """Wrapper function for the table component
    """
    card = dmc.Card(
        id='id-card-table',
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            components.get_button_download()
                        ],
                        width=2,
                        style={'border': styles.border_column}
                    ),
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
                            components.get_table_jiq()
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
                                        width='100%',  # this will force align the height to the column next to it
                                    )
                                ],
                                style={"border": styles.border_column},
                            )
                        ],
                        justify="start",
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
                                [html.Div(get_card_box_plot())]
                            ),
                            dbc.Col(
                                [html.Div(get_card_histogram())]
                            )
                        ]
                    ),
                ],
                title=global_strings.jiq_graphs_group_title
            ),
        ]
    )


def get_layout_junction_inclusion():
    """This is the query/form layout for the junction inclusion query"""
    layout = dbc.Container(
        [
            # Top row  contains input form
            dmc.Space(h=30),  # this will create a space with the tab above it
            dbc.Row(
                [
                    get_accordian_jiq(),
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
