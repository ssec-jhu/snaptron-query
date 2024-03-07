"""This is the Junction Inclusion Query Layout."""

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html

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
