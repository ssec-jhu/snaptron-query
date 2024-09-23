import dash_bootstrap_components as dbc
from dash import html

from snaptron_query.app import components, global_strings as gs

logos = {
    "neurosci": "assets/Neurosci_reversed.svg",
    "ssec": "assets/SSEC_horizontal_white_cropped.png",
    "jmed": "assets/JHM_horizontal_white.svg",
    "idies": "assets/IDIES_JHU_Horizontal_white_500.svg",
    "nih": "assets/NIH_symbol_white.png",
    "nsf": "assets/NSF_Official_High_Res_1200ppi.png",
}


def get_navbar_top():
    """This is the component at the top of the page."""
    return html.Div(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col([html.Img(src=logos["neurosci"], width="100%")], width=3, align="center"),
                        dbc.Col([html.P(gs.web_title)], align="center"),
                        dbc.Col([html.Img(src=logos["ssec"], width="90%")], width=3, align="center"),
                    ],
                    class_name="g-2 d-flex justify-content-between",
                ),
            ],
            fluid=True,
            class_name="display-4",
        ),
        style={"box-shadow": "0 5px 5px -5px #333"},
        className="bg-primary text-light py-4 text-center fs-1 fw-light border-bottom",  # Div
    )


def get_navbar_bottom():
    return html.Div(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col([html.Img(src=logos["nsf"], height="60px")], width=1, align="center"),
                        dbc.Col(html.Img(src=logos["jmed"], height="100px"), width=2, align="center"),
                        dbc.Col(
                            dbc.NavbarBrand(
                                children=[
                                    dbc.Row(
                                        dbc.Col(
                                            [
                                                components.get_text(gs.built_using[0]),
                                                html.A(
                                                    components.get_text(gs.built_using[1]),
                                                    href=gs.url_snaptron,
                                                    className="text-light",
                                                    target="_blank",
                                                    rel="noopener noreferrer",
                                                ),
                                                components.get_text(gs.built_using[2]),
                                                html.A(
                                                    components.get_text(gs.built_using[3]),
                                                    href=gs.url_recount,
                                                    className="text-light",
                                                    target="_blank",
                                                    rel="noopener noreferrer",
                                                ),
                                            ],
                                            align="center",
                                        )
                                    ),
                                    dbc.Row(
                                        dbc.Col(
                                            [
                                                components.get_text(gs.cite),
                                                html.A(
                                                    components.get_text(gs.paper_text),
                                                    href=gs.url_paper,
                                                    className="text-light",
                                                    target="_blank",
                                                    rel="noopener noreferrer",
                                                ),
                                            ],
                                            align="center",
                                        )
                                    ),
                                    dbc.Row(children=[components.get_text(gs.contacts)]),
                                ]
                            ),
                            className="mx-auto text-light",
                            width="auto",
                            style={"text-align": "center"},
                        ),
                        dbc.Col(html.Img(src=logos["idies"], height="80px"), width=2, align="center"),
                        dbc.Col([html.Img(src=logos["nih"], height="30px")], width=1, align="center"),
                    ],
                    align="center",
                    justify="between",
                    class_name="g-0 d-flex justify-content-center",
                )
            ],
            fluid=True,
        ),
        style={"box-shadow": "0 5px 5px -5px #333"},
        # className="bg-primary bg-gradient text-light text-center fs-6 fw-light border-top",
        className="bg-primary text-primary text-center fs-6 fw-light border-top",
    )
