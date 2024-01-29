"""
    This is the Junction Inclusion Query Layout.
"""

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc

import components
import components_jiq_form as fc
import inline_styles as styles

col_width = 2


def get_jiq_form():
    """
        Grid is defined with dash bootstrap components (dbc)
        Individual components are defined with dash mantine components (dmc)
        The width of the top and bottom row is set to fill the row
        The width of the junction textbox column is set to 3 so the rest of the columns balance out

    """
    return [
        dbc.Row(
            [
                dbc.Col(
                    fc.get_dropdown_compilation('dmc'),
                    # width=col_width * 5,
                    style={
                        "border": styles.border_column,
                    },
                ),
            ],
            className="g-0 form-control-sm",
            justify="start",
        ),
        # html.Br(),

        # ROW 2 has the titles of the textbooks so subsequent rows
        # just have textbooks added, not the labels
        dbc.Row(
            [
                dbc.Col(
                    width=col_width,
                    style={
                        "border": styles.border_column,
                    },
                ),
                dbc.Col(
                    fc.get_text_chromosome('dmc'),
                    width=col_width,
                    style={
                        "border": styles.border_column,
                    },
                ),
                dbc.Col(
                    fc.get_text_inclusion_junction('dmc'),
                    width=col_width + 1,
                    style={
                        "border": styles.border_column,
                    },
                ),
                dbc.Col(
                    fc.get_text_exclusion_junction('dmc'),
                    width=col_width + 1,
                    style={
                        "border": styles.border_column,
                    },
                ),
                dbc.Col(
                    width=col_width,
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
                    fc.get_text_junction('dmc'),
                    width=col_width,
                    style={
                        "border": styles.border_column,
                    },
                    align='center',  # vertical alignment: center start end
                    className='ml-auto',  # will justify to the right side
                ),
                dbc.Col(
                    fc.get_input_chrom('dmc'),
                    width=col_width,
                    style={
                        "border": styles.border_column,
                    },
                ),
                dbc.Col(
                    fc.get_input_inc_junction('dmc'),
                    width=col_width + 1,
                    style={
                        "border": styles.border_column,
                    },
                ),
                dbc.Col(
                    fc.get_input_exc_junction('dmc'),
                    width=col_width + 1,
                    style={
                        "border": styles.border_column,
                    },
                ),
                dbc.Col(
                    fc.get_button_add_junction('dmc'),
                    width=col_width,
                    style={
                        "border": styles.border_column,
                    },
                ),
            ],
            # border border-danger: add for border and gutter debugging
            className="g-1 form-control-sm",
            justify="start",
        ),
        dbc.Row(
            dbc.Col(
                fc.get_button_generate_results('dbc'),
                # width=col_width * 5,
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


def get_card_query_form():
    """
        Bundles the junction inclusion query form in one card.
        Card borders are set to 0.
    """
    card = dmc.Card(
        children=[
            dmc.CardSection(
                # dmc.Title('Form card', order=2, align='center'),
                # dmc.Title('Junction Inclusion Query', order=2, align='center'),
            ),
            # dmc.Space(h=50),
            dmc.Group(
                [
                    # html.Div(get_dmc_simple_grid())
                    html.Div(get_jiq_form())
                ],
                position="center",  # centering it makes everything fall into place nicely
                mt="md",
                mb="xs",
            ),
        ],
        # withBorder=True,
        # shadow="sm",
        radius="md",
        # style=styles.boundary_style,
    )
    return card


def get_card_image():
    """
         Bundles the image in one card.
         Card borders are set to 0.
    """
    card = dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Image(
                    src='assets/junction_query.png',
                    withPlaceholder=True,
                    # height='155%',
                )
            ),
        ],
        # withBorder=True,
        # shadow="sm",
        radius="md",
        # style=styles.boundary_style,
    )
    return card


def get_card_histogram():
    """

    """
    card = dmc.Card(
        id='id-card-histogram',
        children=[
            # dmc.CardSection(
            #     dmc.Title('PSI histogram', order=4, align='center'),
            # ),
            dmc.Grid(
                children=[
                    dmc.Col(components.get_switch_log_psi('dmc'), span=3, style={'border': styles.border_grids, }),
                    dmc.Col(span=9, style={'border': styles.border_grids, }),
                    dmc.Col(html.Div(dcc.Graph(id="id-histogram")), span=12, style={'border': styles.border_grids, }),
                ],
                gutter="xs",
            ),
        ],
        # withBorder=True,
        # shadow="md",
        radius="md",
        style=styles.boundary_style,
    )
    return card


def get_card_box_plot():
    """

    """
    card = dmc.Card(
        id='id-card-box-plot',
        children=[
            # dmc.CardSection(
            #     dmc.Title('PSI Box plot', order=4, align='center'),
            # ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            components.get_switch_log_psi('dbc'),
                        ],
                        width=3,
                        style={'border': styles.border_column},
                    )
                ],
                className="g-1"  # border border-primary",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(dcc.Graph(id="id-box-plot"))
                        ],
                        # width=3,
                        style={'border': styles.border_column},
                    )
                ],
                className="g-0"  # border border-primary",
            ),

            # dmc.Grid(
            #     children = [
            #             dmc.Col(components.get_switch_log_psi('dmc'),span=3,style={'border': border_grids, }),
            #             dmc.Col(span=9, style={'border': border_grids, }),
            #             dmc.Col(html.Div(dcc.Graph(id="id-box-plot")), span=12, style={'border': border_grids, }),
            #         ],
            #         gutter="xs",
            # ),
        ],
        # withBorder=True,
        # shadow="sm",
        radius="md",
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
                            components.get_button_download('dbc')
                        ],
                        width=2,
                        align='center',
                        style={'border': styles.border_column}
                        # className='ml-auto'
                    ),
                    dbc.Col(
                        [
                            components.get_switch_lock_data_with_table('dbc')
                        ],
                        width=3,
                        align='center',
                        style={'border': styles.border_column},
                        # className='ms-auto' # will justify to the right
                    ),
                ],
                className="g-0",  # border border-primary",
                justify='between'
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dag.AgGrid(
                                id="id-ag-grid",
                                # ag grid and persistence: data will get lost when tab switches
                                # https://community.plotly.com/t/how-to-add-persistence-to-dash-ag-grid/74944
                                persistence=True,
                                # columnDef and rowData will be dynamically defined via callback
                                # columnDefs=[{"field": i} for i in df.columns.to_list()],
                                # rowData=df.to_dict("records"),

                                # TODO: height of the table may need to be dynamic depending on compilation data
                                style={'height': 800},

                                # TODO: multijunction query will need column size to fit
                                # columnSize="sizeToFit",
                                defaultColDef={"flex": 1,  # snaps the end
                                               "sortable": True, "resizable": True, "filter": True,
                                               # "minWidth": 150,
                                               # TODO: is cellwrapping required when the abstract of the study is
                                               #  included. Both of below must be on for cell wrapping
                                               # 'wrapText': True,
                                               # 'autoHeight': True,
                                               },
                                dashGridOptions={'rowSelection': 'multiple',
                                                 'checkboxSelection': 'True',
                                                 'isRowSelectable': {"function": "log(params)"},
                                                 'pagination': True,
                                                 },
                                className="header-style-on-filter ag-theme-alpine",
                            ),
                        ]
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


"""
    This is the query/form layout for the junction inclusion query
"""
junction_inclusion_query_layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        get_card_query_form()
                    ],
                    # className="bg-light",
                    style={'border': styles.border_column}),
                dbc.Col(
                    [
                        get_card_image()
                    ],
                    width=4,
                    style={'border': styles.border_column}
                )
            ],
            # TODO: using the general boundary messes with the layout, need to figure out why?
            # style=styles.boundary_style,
            style={"box-shadow": "1px 2px 7px 0px grey",
                   "border-radius": "10px"},
            className='g-0',  # no gutters in between the cards
        ),
        # an alternative option to the card and the image
        # dbc.Row(
        #     [
        #         dbc.Col(
        #             [
        #                 get_card_query_form_and_image()
        #             ],
        #             # className="bg-light",
        #             style={'border': styles.border_column}),
        #     ],
        #     className='g-0',  # no gutters in between the cards
        # ),

        # Second row  contains the plots and graphs
        dmc.Space(h=20),
        dbc.Row(
            [
                dbc.Col(
                    [
                        get_card_box_plot()
                    ],
                    width=6,
                    style={'border': styles.border_column}
                ),
                dbc.Col(
                    [
                        get_card_histogram()
                    ],
                    width=6,
                    style={'border': styles.border_column}
                )
            ],
            className='g-2',  # leave some gutter in between plots
            justify="center",
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

        # # You can uncomment here:for the other grid structure layouts
        # html.Br(),
        # get_card_query_form_and_image(),
        # html.Br(),
        # get_testing_card_dbc_vc_dmc(),

    ],
    # className='shadow-sm' # puts the shadow background around the div
)
