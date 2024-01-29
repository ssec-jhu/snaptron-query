import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html

import components_jiq_form as fc
import inline_styles as styles

col_width = 2


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
                        "border": styles.border_column,
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
                        "border": styles.border_column,
                    },
                ),
                dbc.Col(
                    fc.get_text_chromosome('dcc'),
                    width=col_width,
                    style={
                        "border": styles.border_column,
                    },
                ),
                dbc.Col(
                    fc.get_text_inclusion_junction('dcc'),
                    width=col_width,
                    style={
                        "border": styles.border_column,
                    },
                ),
                dbc.Col(
                    fc.get_text_exclusion_junction('dcc'),
                    width=col_width,
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
                    fc.get_text_junction('dcc'),
                    width=col_width,
                    style={
                        "border": styles.border_column,
                    },
                ),
                dbc.Col(
                    fc.get_input_chrom('dcc'),
                    width=col_width,
                    style={
                        "border": styles.border_column,
                    },
                ),
                dbc.Col(
                    fc.get_input_inc_junction('dcc'),
                    width=col_width,
                    style={
                        "border": styles.border_column,
                    },
                ),
                dbc.Col(
                    fc.get_input_exc_junction('dcc'),
                    width=col_width,
                    style={
                        "border": styles.border_column,
                    },
                ),
                dbc.Col(
                    fc.get_button_add_junction('dbc'),
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
                dmc.Col(html.Div("long words here", style=styles.style_debugging), span=3),
                dmc.Col(html.Div("test 2", style=styles.style_debugging), span=3),
                dmc.Col(html.Div("test 3", style=styles.style_debugging), span=3),
                dmc.Col(html.Div("test 4", style=styles.style_debugging), span=3),
                dmc.Col(html.Div("test 5", style=styles.style_debugging), span=3),
                dmc.Col(html.Div("test 6", style=styles.style_debugging), span=3),
                dmc.Col(html.Div("test 7", style=styles.style_debugging), span=3),
            ],
            gutter="xl",
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
                            'border': styles.border_grids,
                        },
                        ),
                dmc.Col(span=2, style={'border': styles.border_grids, }),

                # the span sum for each row must equal 12
                dmc.Col(span=2, style={'border': styles.border_grids, }),
                dmc.Col(fc.get_text_chromosome('dmc'), span=2),
                dmc.Col(fc.get_text_inclusion_junction('dmc'), span=2),
                dmc.Col(fc.get_text_exclusion_junction('dmc'), span=2),
                dmc.Col(span=4, style={'border': styles.border_grids, }),

                # the span sum for each row must equal 12
                dmc.Col(fc.get_text_junction('dmc'), span=2, style={'border': styles.border_grids, }),
                dmc.Col(fc.get_input_chrom('dmc'), span=2, style={'border': styles.border_grids, }),
                dmc.Col(fc.get_input_inc_junction('dmc'), span=2, style={'border': styles.border_grids, }),
                dmc.Col(fc.get_input_exc_junction('dmc'), span=2, style={'border': styles.border_grids, }),
                dmc.Col(fc.get_button_add_junction('dmc'), span=2, style={'border': styles.border_grids, }),
                # dmc.Col(span='auto'), # this will fill the row
                dmc.Col(span=2, style={'border': styles.border_grids, }),  # this will fill the row
                dmc.Col(fc.get_button_generate_results('dmc'), span='auto', style={'border': styles.border_grids, }),
            ],
            gutter="sm",  # small gutters

        )
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
                "border": styles.border_grids,
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
                "border": styles.border_grids,
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
                "border": styles.border_grids,
            },
        ),
        dmc.SimpleGrid(
            cols=1,
            spacing='lg',
            children=[
                fc.get_button_generate_results('dmc')
            ],
            style={
                "border": styles.border_grids,
            },
        )
    ]


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
                    dmc.Col(html.Div("long words here", style=styles.style_debugging), span=3),
                    dmc.Col(html.Div("2", style=styles.style_debugging), span=3),
                    dmc.Col(html.Div("3", style=styles.style_debugging), span=3),
                    dmc.Col(html.Div("4", style=styles.style_debugging), span=3),
                    dmc.Col(html.Div("5", style=styles.style_debugging), span=3),
                    dmc.Col(html.Div("6", style=styles.style_debugging), span=3),
                    dmc.Col(html.Div("7", style=styles.style_debugging), span=3),
                ],
                gutter="xl",
            ),
        ],
        # withBorder=True,
        # shadow="sm",
        radius="md",
        style=styles.boundary_style,
    )
    return card


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
                                    "border": styles.border_column,
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
                            'border': styles.border_column,
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
        style=styles.boundary_style,
    )
    return card
