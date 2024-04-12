"""This is the Junction Inclusion Query Layout."""

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_loading_spinners as dls
from dash import html, dcc

from snaptron_query.app import components, components_jiq, global_strings as gs, icons
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
                            dbc.Col(
                                [
                                    components.get_switch(switch_id='id-switch-jiq-log-psi-histogram',
                                                          switch_label=gs.jiq_log_psi, switch_on=True),
                                    dmc.Space(w=10),
                                    components.get_switch(switch_id='id-switch-jiq-log-y-histogram',
                                                          switch_label=gs.switch_log_geq_hist_y)

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
                            dbc.Col(
                                [
                                    components.get_switch(switch_id='id-switch-jiq-log-psi-box-plot',
                                                          switch_label=gs.jiq_log_psi, switch_on=True),
                                    dmc.Space(w=10),
                                    components.get_switch(switch_id='id-switch-jiq-violin-box-plot',
                                                          switch_label=gs.switch_violin)
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
                            dcc.Graph(id="id-box-plot-jiq"),
                            # dbc.Alert(
                            #     [icons.point_up, gs.box_plot_click_help],
                            #     id="id-jiq-box-plot-alert",
                            #     is_open=False,
                            #     # TODO: keep this dismissable or with duration?
                            #     # duration=10000,
                            #     dismissable=True,
                            #     class_name='user-tip',
                            # ),
                        ],
                        style={'border': styles.border_column},
                        className="g-0"
                    ),
                    dbc.Row(
                        dbc.Col([
                            components.get_text('dmc', [icons.info, gs.box_plot_click_help])
                        ],
                            className='d-flex justify-content-center',
                            align='center',  # vertical alignment of the column
                            style={'border': styles.border_column}
                        ),
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
                            components.get_button_download('id-button-jiq-download-all',
                                                           html.Span([icons.download, gs.download_original])),
                            components.get_tooltip("id-button-jiq-download-all", gs.download_original_help)
                        ],
                        width=2,
                        align='center',  # vertical alignment of the column
                        style={'border': styles.border_column}
                    ),
                    # dbc.Col(
                    #     [
                    #         dmc.Space(w=8),
                    #         dbc.Checklist(
                    #             id="id-checkbox-download_filtered",
                    #             options=[{"label": "download results with table filters applied", "value": 1}],
                    #             label_checked_style={"color": "var(--bs-danger)"},
                    #             input_checked_style={
                    #                 "backgroundColor": "var(--bs-danger)",
                    #                 "borderColor": "#ea6258",
                    #             }
                    #         )
                    #     ],
                    #     align='center',  # vertical alignment of the column
                    # ),
                    dbc.Col(
                        [
                            components.get_button_download('id-button-jiq-download-filtered',
                                                           html.Span([icons.download, gs.download_filtered])),
                            components.get_tooltip("id-button-jiq-download-filtered", gs.download_filtered_help)
                        ],
                        width=2,
                        align='center',  # vertical alignment of the column
                        style={'border': styles.border_column}
                    ),
                    # dbc.Col(
                    #     [
                    #         components.get_radio_items_download_options("id-jiq-download-options")
                    #     ],
                    #     width=4,
                    #     align='center',  # vertical alignment of the column
                    #     className='d-flex justify-content-start',
                    #     style={'border': styles.border_column}
                    # ),
                    dbc.Col([
                        components.get_text('dmc', [icons.info, gs.jiq_table_help])
                    ],
                        className='d-flex justify-content-center',
                        align='center',  # vertical alignment of the column
                        style={'border': styles.border_column}
                    ),
                    dbc.Col(
                        [
                            components.get_text('dmc', icons.lock_open),
                            dmc.Space(w=8),
                            components.get_switch_lock_data_with_table('id-switch-jiq-lock-with-table', gs.switch_lock),
                            dmc.Space(w=3),
                            components.get_text('dmc', icons.lock_closed),
                            dmc.Space(w=10),
                            components.get_text('dmc', gs.switch_lock),
                            components.get_tooltip("id-switch-jiq-lock-with-table", gs.switch_lock_help)
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
            dls.Propagate(show_initially=False,
                          color='var(--bs-secondary)',
                          children=[html.Div(id="id-loading-graph-jiq")]
                          ),

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
                        get_card_table_jiq()
                    ],
                    id='id-ag-grid-display-jiq',
                    style={'display': 'None'}
                ),
            ),
        ],
    )
    return layout
