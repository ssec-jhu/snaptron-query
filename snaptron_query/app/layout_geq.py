"""This is the Junction Inclusion Query Layout."""

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc
from dash_iconify import DashIconify
from snaptron_query.app import components_geq as components
from snaptron_query.app import global_strings as gs
from snaptron_query.app import inline_styles as styles


def get_geq_form():
    """Wrapper function for the Gene Expression Query components."""
    return [
        # ROW 2 has the titles of the text boxes
        dbc.Row(
            [
                dbc.Col(
                    components.get_text_gene_id('dmc'),
                    width=2,
                    style={"border": styles.border_column},
                    align='center',
                ),
                dbc.Col(
                    components.get_input_gene_id(),
                    width=3,
                    style={"border": styles.border_column},
                    align='center',
                ),
                dbc.Col(
                    components.get_switch_normalize(),
                    #width=2,
                    style={"border": styles.border_column},
                    className="mx-3 mt-3",
                ),
                dbc.Col(
                    components.get_text_gene_id('dmc'),
                    width=2,
                    style={"border": styles.border_column},
                    #align='center',
                ),
                dbc.Col(
                    components.get_input_gene_id_norm(),
                    width=3,
                    style={"border": styles.border_column},
                    align='center',
                ),

            ],
            className="g-1 form-control-sm",
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    components.get_text_gene_coordinates('dmc'),
                    width=2,
                    style={"border": styles.border_column},
                    align='center',
                ),
                dbc.Col(
                    components.get_input_gene_coordinates(),
                    width=3,
                    style={"border": styles.border_column},
                    align='center',
                ),
                dbc.Col(
                    style={"border": styles.border_column},
                    align='center',
                ),
                dbc.Col(
                    components.get_text_gene_coordinates('dmc'),
                    width=2,
                    style={"border": styles.border_column},
                    align='center',
                ),
                dbc.Col(
                    components.get_input_gene_coordinates_norm(),
                    width=3,
                    style={"border": styles.border_column},
                    align='center',
                ),
            ],
            className="g-1 form-control-sm",
            align="center",
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

def get_geq_form2():
    """Wrapper function for the Gene Expression Query components."""
    return [
        # ROW 2 has the titles of the text boxes
        dbc.Row(
            [
                dbc.Col(
                    width=2,
                    style={"border": styles.border_column},
                    align='center',
                ),
                dbc.Col(
                    components.get_text_gene_id('dmc'),
                    width=3,
                    style={"border": styles.border_column},
                    align='center',
                ),
                dbc.Col(
                    components.get_text_gene_coordinates('dmc'),
                    width=3,
                    style={"border": styles.border_column},
                    align='center',
                ),
            ],
            className="g-1 form-control-sm",
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dmc.Text("Enter gene information:", weight=500, size="sm"),
                    width=2,
                    style={"border": styles.border_column},
                    align='center',
                ),
                dbc.Col(
                    components.get_input_gene_id(),
                    width=3,
                    style={"border": styles.border_column},
                    align='center',
                ),
                dbc.Col(
                    components.get_input_gene_coordinates(),
                    width=3,
                    style={"border": styles.border_column},
                    align='center',
                ),
                dbc.Col(
                    html.Div([dbc.Checkbox(
                        id="id-switch-normalize",
                        label="Normalize Counts",
                        value=False,
                    )]),
                    width=2,
                    style={"border": styles.border_column},
                    align='center',
                )
            ],
            className="g-1 form-control-sm",
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    #dmc.Text("Enter gene information:", weight=500, size="sm"),
                    width=2,
                    style={"border": styles.border_column},
                    align='center',
                ),
                dbc.Col(
                    components.get_input_gene_id_norm(),
                    width=3,
                    style={"border": styles.border_column},
                    align='center',
                ),
                dbc.Col(
                    components.get_input_gene_coordinates_norm(),
                    width=3,
                    style={"border": styles.border_column},
                    align='center',
                ),
            ],
            className="g-1 form-control-sm",
            align="center",
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
def get_accordian_geq():
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dmc.Space(h=20),  # this will create a space with the tab above it
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div(get_geq_form())
                                ],
                                #width=8
                            ),
                        ],
                        justify="start",
                    ),
                ],
                title=gs.geq_form_title,
            ),

            dbc.AccordionItem(
                [
                    dmc.Space(h=20),  # this will create a space with the tab above it
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div(get_geq_form2())
                                ],
                                # width=8
                            ),
                        ],
                        justify="start",
                    ),
                ],
                title=gs.geq_form_title,
            ),
        ]
    )


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
        ],
    )
    return layout
