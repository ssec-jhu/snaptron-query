"""This is the Junction Inclusion Query Layout."""

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc

from snaptron_query.app import components, components_jiq, global_strings as gs
from snaptron_query.app import inline_styles as styles


def get_form_jiq():
    """Wrapper function for the Junction Inclusion Query components.
    The width of the top and bottom row is set to fill the row
    """
    return [
        dbc.Row(
            [
                dbc.Col(
                    components.get_dropdown_compilation('id-input-compilation-jiq'),
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
                    components.get_text('dmc', gs.jiq_input_inc_txt),
                    width=4,
                    style={"border": styles.border_column},
                    align='center',
                    className='mx-0.5'
                ),
                dbc.Col(
                    components.get_text('dmc', gs.jiq_input_exc_txt),
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
                    components_jiq.get_text_junction('dmc'),
                    width=2,
                    style={"border": styles.border_column},
                    align='center',
                ),
                dbc.Col(
                    components.get_input(gs.jiq_input_inc_placeholder, 'id-input-jiq-inc-junc'),
                    width=4,
                    style={"border": styles.border_column},
                    align='center',
                    className='mx-0.5'
                ),
                dbc.Col(
                    components.get_input(gs.jiq_input_exc_placeholder, 'id-input-jiq-exc-junc'),
                    width=4,
                    style={"border": styles.border_column},
                    align='center',
                ),
                dbc.Col(
                    components_jiq.get_button_add_junction(),
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
                    components_jiq.get_button_jiq_results(),
                    style={"border": styles.border_column},
                    class_name="d-grid gap-0 col-12"  # this will make the button take over full width
                ),
            ],
            className="g-2 my-2",  # my-2: creates the padding at the top
        ),
    ]


def get_card_histogram_jiq():
    """Wrapper function for the histogram component in a card layout"""
    card = dbc.Card(
        id='id-card-histogram',
        children=[
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(width=7, style={'border': styles.border_column}),
                            dbc.Col(
                                [
                                    components.get_switch(switch_id='id-switch-jiq-log-psi-histogram',
                                                          switch_label=gs.jiq_log_psi, switch_on=True),
                                    dmc.Space(w=10),
                                    components.get_switch(switch_id='id-switch-jiq-log-y-histogram',
                                                          switch_label=gs.switch_log_geq_hist_y)

                                ],
                                width=5,
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
                            html.Div(dcc.Graph(id="id-histogram-jiq"))
                        ],
                        style={'border': styles.border_column}
                    )
                ]
            ),
        ],
        style=styles.boundary_style,
    )
    return card


def get_card_box_plot_jiq():
    """Wrapper function for the box plot component in a card layout"""
    card = dbc.Card(
        id='id-card-box-plot',
        children=[
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(width=7, style={'border': styles.border_column}),
                            dbc.Col(
                                [
                                    components.get_switch(switch_id='id-switch-jiq-log-psi-box-plot',
                                                          switch_label=gs.jiq_log_psi, switch_on=True),
                                    dmc.Space(w=10),
                                    components.get_switch(switch_id='id-switch-jiq-violin-box-plot',
                                                          switch_label=gs.switch_violin)
                                ],
                                width=5,
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
                            dcc.Graph(id="id-box-plot-jiq")
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


def get_card_table_jiq():
    """Wrapper function for the table component
    """
    card = dmc.Card(
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            components.get_button_download('id-button-jiq-download')
                        ],
                        width=2,
                        align='center',  # vertical alignment of the column
                        style={'border': styles.border_column}
                    ),
                    dbc.Col(),
                    dbc.Col(
                        [
                            components.get_switch_lock_data_with_table('id-switch-jiq-lock-with-table', gs.switch_lock),
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
                            components.get_table(table_id='id-ag-grid-jiq')
                        ],
                        className="dbc dbc-ag-grid"
                    )
                ],
                # className="gy-4",  # button too close to the table, needs some gutter
            )
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
                            dbc.Col(
                                [
                                    html.Div(get_form_jiq())
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
                title=gs.jiq_form_title,
            ),
        ]
    )


def get_accordian_graphs_jiq():
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row(
                        [
                            # row equally divided for the plots
                            dbc.Col(id='id-jiq-box-plot-col',
                                    children=[html.Div(get_card_box_plot_jiq())]
                                    ),
                            dbc.Col(id='id-jiq-histogram-col',
                                    children=[html.Div(get_card_histogram_jiq())]
                                    )
                        ]
                    ),
                ],
                title=gs.graphs_group_title
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
                    get_accordian_form_jiq(),
                ],
                style={"box-shadow": "1px 2px 7px 0px grey",
                       "border-radius": "10px"},
                className='g-0',  # no gutters in between the cards
            ),

            html.Div(id='id-alert-jiq'),
            # Second row  of the layout contains the plots and graphs
            dmc.Space(h=20),
            dbc.Row(
                [
                    get_accordian_graphs_jiq(),
                ],
                id='id-display-graphs-jiq',
                style={"box-shadow": "1px 2px 7px 0px grey",
                       "border-radius": "10px",
                       # Note: Setting the 'display': 'None' creates a delay in the rendering of the plots. They
                       # render to the screen then shift to their position.
                       # visibility will keep the space, so when the plots come in, they render fast
                       'visibility': 'hidden'
                       },
                className='g-0',  # no gutters in between the cards
            ),

            # Third row is the row containing the table
            dmc.Space(h=20),
            dbc.Row(
                [
                    html.Div(get_card_table_jiq())
                ],
                id='id-ag-grid-display-jiq',
                style={'display': 'None'}
            ),
        ],
    )
    return layout
