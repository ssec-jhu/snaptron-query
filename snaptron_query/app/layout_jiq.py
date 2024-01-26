"""
    This is the Junction Inclusion Query Layout.
"""

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc

import components
import components_jiq_form as fc

# --------------------
#       USE FOR DEBUGGING LAYOUT
# --------------------
# set the 0 to 1 to see the grids for alignment and layout changes
border_card = f'0px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}'
border_column = f'0px solid {dmc.theme.DEFAULT_COLORS['green'][4]}'
border_grids = f'0px solid {dmc.theme.DEFAULT_COLORS['orange'][4]}'
style_debugging = {
    'border': border_grids,
    # "textAlign": "center",
}
# set this value to 'block' to see the layout without running the query
display_style = 'block'  # none or block for debugging
# --------------------


col_width = 2


def get_dbc_grid_with_dcc_com():
    """
        Grid is defined with dash bootstrap components (dbc)
        Individual components are defined with dash core components (dcc)
        The width of the top and bottom row is set to 10 for this design
    """
    return [
        dbc.Row(
            [
                dbc.Col(
                    [
                        fc.get_dropdown_compilation('dcc'),
                    ],
                    width=col_width * 5,
                    style={
                        "border": border_column,
                    },
                ),
            ],
            className="g-2 form-control-sm",
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
                        "border": border_column,
                    },
                ),
                dbc.Col(
                    fc.get_text_chromosome('dcc'),
                    width=col_width,
                    style={
                        "border": border_column,
                    },
                ),
                dbc.Col(
                    fc.get_text_inclusion_junction('dcc'),
                    width=col_width,
                    style={
                        "border": border_column,
                    },
                ),
                dbc.Col(
                    fc.get_text_exclusion_junction('dcc'),
                    width=col_width,
                    style={
                        "border": border_column,
                    },
                ),
                dbc.Col(
                    width=col_width,
                    style={
                        "border": border_column,
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
                    fc.get_text_junction('dcc'),
                    width=col_width,
                    style={
                        "border": border_column,
                    },
                ),
                dbc.Col(
                    fc.get_input_chrom('dcc'),
                    width=col_width,
                    style={
                        "border": border_column,
                    },
                ),
                dbc.Col(
                    fc.get_input_inc_junction('dcc'),
                    width=col_width,
                    style={
                        "border": border_column,
                    },
                ),
                dbc.Col(
                    fc.get_input_exc_junction('dcc'),
                    width=col_width,
                    style={
                        "border": border_column,
                    },
                ),
                dbc.Col(
                    fc.get_button_add_junction('dbc'),
                    width=col_width,
                    style={
                        "border": border_column,
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
                style={
                    "border": border_column,
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


def get_dbc_cols_with_dmc_comp():
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
                        "border": border_column,
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
                        "border": border_column,
                    },
                ),
                dbc.Col(
                    fc.get_text_chromosome('dmc'),
                    width=col_width,
                    style={
                        "border": border_column,
                    },
                ),
                dbc.Col(
                    fc.get_text_inclusion_junction('dmc'),
                    width=col_width + 1,
                    style={
                        "border": border_column,
                    },
                ),
                dbc.Col(
                    fc.get_text_exclusion_junction('dmc'),
                    width=col_width + 1,
                    style={
                        "border": border_column,
                    },
                ),
                dbc.Col(
                    width=col_width,
                    style={
                        "border": border_column,
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
                        "border": border_column,
                    },
                    align='center',  # vertical alignment: center start end
                    className='ml-auto',  # will justify to the right side
                ),
                dbc.Col(
                    fc.get_input_chrom('dmc'),
                    width=col_width,
                    style={
                        "border": border_column,
                    },
                ),
                dbc.Col(
                    fc.get_input_inc_junction('dmc'),
                    width=col_width + 1,
                    style={
                        "border": border_column,
                    },
                ),
                dbc.Col(
                    fc.get_input_exc_junction('dmc'),
                    width=col_width + 1,
                    style={
                        "border": border_column,
                    },
                ),
                dbc.Col(
                    fc.get_button_add_junction('dmc'),
                    width=col_width,
                    style={
                        "border": border_column,
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
                    "border": border_column,
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


def get_dmc_grid():
    """
            This uses the dmc grid. Rows and columns are not defined with dmc. The column just wrap around
            You  need to define extra padding columns.
            Individual components are defined with dash mantine components (dmc)
            Total row width is defined as 12 by default.
    """
    return [
        dmc.Grid(
            [
                # the span sum for each row must equal 12
                dmc.Col(fc.get_dropdown_compilation('dmc'),
                        span=10,
                        style={
                            'border': border_grids,
                        },
                        ),
                dmc.Col(span=2, style={'border': border_grids, }),

                # the span sum for each row must equal 12
                dmc.Col(span=2, style={'border': border_grids, }),
                dmc.Col(fc.get_text_chromosome('dmc'), span=2),
                dmc.Col(fc.get_text_inclusion_junction('dmc'), span=2),
                dmc.Col(fc.get_text_exclusion_junction('dmc'), span=2),
                dmc.Col(span=4, style={'border': border_grids, }),

                # the span sum for each row must equal 12
                dmc.Col(fc.get_text_junction('dmc'), span=2, style={'border': border_grids, }),
                dmc.Col(fc.get_input_chrom('dmc'), span=2, style={'border': border_grids, }),
                dmc.Col(fc.get_input_inc_junction('dmc'), span=2, style={'border': border_grids, }),
                dmc.Col(fc.get_input_exc_junction('dmc'), span=2, style={'border': border_grids, }),
                dmc.Col(fc.get_button_add_junction('dmc'), span=2, style={'border': border_grids, }),
                # dmc.Col(span='auto'), # this will fill the row
                dmc.Col(span=2, style={'border': border_grids, }),  # this will fill the row
                dmc.Col(fc.get_button_generate_results('dmc'), span='auto', style={'border': border_grids, }),
            ],
            gutter="sm",  # small gutters

        )
    ]


def get_dmc_grid_example():
    """
            This uses the dmc grid. Rows and columns are not defined with dmc. The column just wrap around
            You  need to define extra padding columns.
            Individual components are defined with dash mantine components (dmc)
            Total row width is defined as 12 by default.
    """
    return [
        dmc.Grid(
            [
                dmc.Col(html.Div("long words here", style=style_debugging), span=3),
                dmc.Col(html.Div("test 2", style=style_debugging), span=3),
                dmc.Col(html.Div("test 3", style=style_debugging), span=3),
                dmc.Col(html.Div("test 4", style=style_debugging), span=3),
                dmc.Col(html.Div("test 5", style=style_debugging), span=3),
                dmc.Col(html.Div("test 6", style=style_debugging), span=3),
                dmc.Col(html.Div("test 7", style=style_debugging), span=3),
            ],
            gutter="xl",
        ),
    ]


def get_dmc_simple_grid():
    """
        This uses the dmc simple grid. You can specify how many columns each row has which can be helpful at times.
        The column just wrap around as in the other grid type in dmc
        You  need to define extra padding columns.
        Individual components are defined with dash mantine components (dmc)
        Total row width is defined as 12 by default.
    """
    return [
        # SimpleGrid is a simple flexbox container where each child is treated as a column
        # 'xlg' doesn't affect it?
        dmc.SimpleGrid(
            cols=1,  # number of columns per row.
            spacing="lg",
            mb='lg',  # adding medium margin to bottom
            children=[
                fc.get_dropdown_compilation('dmc'),
            ],
            style={
                "border": border_grids,
            },
        ),
        dmc.SimpleGrid(
            cols=5,
            spacing='lg',
            mt='lg',
            children=[
                html.Div(),
                fc.get_text_chromosome('dmc'),
                fc.get_text_inclusion_junction('dmc'),
                fc.get_text_exclusion_junction('dmc'),
                html.Div(),
            ],
            style={
                "border": border_grids,
            },
        ),
        dmc.SimpleGrid(
            cols=5,
            spacing='xlg',  # setting this to xlg will make the textbooks closer! not further
            mb='lg',
            children=[
                fc.get_text_junction('dmc'),
                fc.get_input_chrom('dmc'),
                fc.get_input_inc_junction('dmc'),
                fc.get_input_exc_junction('dmc'),
                fc.get_button_add_junction('dmc'),
            ],
            style={
                "border": border_grids,
            },
        ),
        dmc.SimpleGrid(
            cols=1,
            spacing='lg',
            children=[
                fc.get_button_generate_results('dmc')
            ],
            style={
                "border": border_grids,
            },
        )
    ]


def get_card_query_form_and_image():
    """
            Bundled the junction inclusion query form and the image into one card.
            Card borders are set to 0
            Used for debugging with margins and padding currently
    """
    card = dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Title('Form and Image in card', order=2, align='center'),
            ),
            # dmc.Space(h=50),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                children=get_dmc_simple_grid(),
                                style={
                                    "border": border_column,
                                },
                            ),
                        ],
                        className='g-0'  # 0 gutters for this column
                    ),
                    dbc.Col(
                        html.Img(src='assets/junction_query.png',
                                 style={'object-fit': 'contain',
                                        'width': '400px',  # changing the width actually pushes the image to the right??
                                        'height': '220px',
                                        }
                                 ),
                        style={
                            'border': border_column,
                        },
                        width=4,
                        className='g-1',  # small gutters for this column.
                        # this will override row alignment
                        align='center'  # vertical alignment: center start end
                    )
                ],
                justify='center'
            )
        ],
        # withBorder=True,
        # shadow="sm",
        radius="md",
        style={"width": '100%',
               "border": border_card,
               # "border-radius": "10px",
               # "background-color": "#CDCDCD",
               # "box-shadow": "1px 2px 7px 0px grey"
               },
    )
    return card


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
                    html.Div(get_dbc_cols_with_dmc_comp())
                ],
                position="center",  # centering it makes everything fall into place nicely
                mt="md",
                mb="xs",
            ),
        ],
        # withBorder=True,
        # shadow="sm",
        radius="md",
        style={"width": '100%',
               "border": border_card,
               },
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
        style={"width": '100%',
               # 'height': '120%'
               "border": border_card,
               },
    )
    return card


def get_testing_card_dbc_vc_dmc():
    """
         This code is used for debugging all the different grid options and combinations
         for the junction inclusion query. It is very helpful as components move around.
         This will lay out all the components, so you can pick the one that fits best.
    """

    card = dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Title('Junction Inclusion Query', order=1, align='center'),
            ),

            dmc.Space(h=50),
            dmc.Title('DBC Row/Col + dcc comp, width set to 10', order=3),
            html.Div(children=get_dbc_grid_with_dcc_com()),

            dmc.Space(h=50),
            dmc.Title('DBC Row/Col + dmc comp -> in a dmc.Group -> centered ', order=3),
            dmc.Group(
                [
                    html.Div(get_dbc_cols_with_dmc_comp())
                ],
                position="center",  # centering it makes everything fall into place nicely
                mt="md",
                mb="xs",
            ),

            dmc.Space(h=50),
            dmc.Title('DMC grid + dmc comp -> in a dmc.Group -> centered has no effect', order=3),
            dmc.Group(
                [
                    html.Div(get_dmc_grid())
                ],
                # centering dmc.grid does nothing because there is no definition of row, I had to put "dummy"
                # columns, so the right side has empty columns
                position="center",
                mt="md",
                mb="xs",
            ),

            dmc.Space(h=50),
            dmc.Title('DMC simple grid + dmc comp -> in a dmc.Group -> centered', order=3),
            dmc.Group(
                [
                    html.Div(get_dmc_simple_grid())
                ],
                position="center",
                mt="md",
                mb="xs",
            ),
            dmc.Space(h=50),
            dmc.Title('DMC simple grid + dmc comp-> out of a group', order=3),
            html.Div(get_dmc_simple_grid()),

            dmc.Space(h=50),
            dmc.Title('form_dmc_grid_example in a group', order=3),
            dmc.Group(
                [
                    html.Div(get_dmc_grid_example())
                ]
            ),

            dmc.Space(h=50),
            dmc.Title('DMC grid out of the group', order=3),
            dmc.Grid(
                [
                    dmc.Col(html.Div("long words here", style=style_debugging), span=3),
                    dmc.Col(html.Div("2", style=style_debugging), span=3),
                    dmc.Col(html.Div("3", style=style_debugging), span=3),
                    dmc.Col(html.Div("4", style=style_debugging), span=3),
                    dmc.Col(html.Div("5", style=style_debugging), span=3),
                    dmc.Col(html.Div("6", style=style_debugging), span=3),
                    dmc.Col(html.Div("7", style=style_debugging), span=3),
                ],
                gutter="xl",
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"width": '100%'},
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
                    dmc.Col(components.get_switch_log_psi('dmc'), span=3, style={'border': border_grids, }),
                    dmc.Col(span=9, style={'border': border_grids, }),
                    dmc.Col(html.Div(dcc.Graph(id="id-histogram")), span=12, style={'border': border_grids, }),
                ],
                gutter="xs",
            ),
        ],
        withBorder=True,
        shadow="md",
        radius="md",
        style={
            'display': display_style,
            "width": '100%',
            "border": border_card,
            # "border-radius": "10px",
            # "background-color": "#CDCDCD",
            "box-shadow": "1px 2px 7px 0px grey"
        },
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
                        style={'border': border_column},
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
                        style={'border': border_column},
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
        withBorder=True,
        shadow="sm",
        radius="md",
        style={
            'display': display_style,
            "width": '100%',
            "border": border_card,
            # "border-radius": "10px",
            # "background-color": "#CDCDCD",
            "box-shadow": "1px 2px 7px 0px grey"
        },
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
                        style={'border': border_column}
                        # className='ml-auto'
                    ),
                    dbc.Col(
                        [
                            components.get_switch_lock_data_with_table('dbc')
                        ],
                        width=3,
                        align='center',
                        style={'border': border_column},
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
        withBorder=True,
        shadow="md",
        radius="md",
        style={
            'display': display_style,
            "width": '100%',
            "border": border_card,
            # "border-radius": "10px",
            # "background-color": "#CDCDCD",
            "box-shadow": "1px 2px 7px 0px grey"
        },
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
                    style={'border': border_column}),
                dbc.Col(
                    [
                        get_card_image()
                    ],
                    width=4,
                    style={'border': border_column}
                )
            ],
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
        #             style={'border': border_column}),
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
                    style={'border': border_column}
                ),
                dbc.Col(
                    [
                        get_card_histogram()
                    ],
                    width=6,
                    style={'border': border_column}
                )
            ],
            className='g-2',  # no gutters in between the columns
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
                    style={'border': border_column}
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
