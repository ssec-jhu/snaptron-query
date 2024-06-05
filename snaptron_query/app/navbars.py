import dash_bootstrap_components as dbc
from dash import html

from snaptron_query.app import components

logos = {
    "neurosci": "assets/logo_neurosci_reversed.svg",
    "ssec": "assets/SSEC-logoHorizontal white_cropped.png",
    "jmed": "assets/medicine.logo.vertical.blue.svg",
    "idies": "assets/IDIES-inhouse-logo_Vertical_navy.svg",
    "schmidt": "assets/schmidt-futures.png",
    "nih": "assets/NIH_Master_Logo_Vertical_2Color.png",
    "nsf": "assets/NSF_Official_logo_High_Res_1200ppi.png",
}


def get_navbar_top():
    """This is the component at the top of the page."""
    return html.Div(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col([html.Img(src=logos["neurosci"], width="100%")], width=3, align="center"),
                        dbc.Col([html.P("SnapMine")], align="center"),
                        dbc.Col([html.Img(src=logos["ssec"], width="100%")], width=3, align="center"),
                    ],
                    class_name="g-2 d-flex justify-content-between",
                ),
            ],
            fluid=True,
            class_name="display-4",
        ),
        style={"box-shadow": "0 5px 5px -5px #333"},
        className="bg-primary bg-gradient text-light py-4 text-center fs-1 fw-light border-bottom",  # Div
    )


def get_navbar_bottom():
    return html.Div(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                components.get_text("Built using "),
                                html.A(
                                    components.get_text("Snaptron"),
                                    href="https://snaptron.cs.jhu.edu/",
                                    className="study-link-color",
                                ),
                                components.get_text(" and "),
                                html.A(
                                    components.get_text("Recount3"),
                                    href="https://rna.recount.bio/",
                                    className="study-link-color",
                                ),
                            ],
                            width=3,
                            align="center",
                        ),
                        dbc.Col([components.get_text("Please Cite: <paper link/name>")], width=3, align="center"),
                        dbc.Col([components.get_text("Contacts")], width=2, align="center"),
                    ],
                    class_name="dbc g-0 d-flex justify-content-center mt-1",
                ),
                dbc.Row(
                    [
                        dbc.Col([html.Img(src=logos["jmed"])], width=2, class_name="logos-size"),
                        dbc.Col([html.Img(src=logos["idies"])], width=2, class_name="logos-size"),
                        dbc.Col([html.Img(src=logos["schmidt"], width="45%")], width=2, align="center"),
                        dbc.Col([html.Img(src=logos["nih"], width="35%")], width=2, align="center"),
                        dbc.Col([html.Img(src=logos["nsf"], width="35%")], width=2, align="center"),
                    ],
                    class_name="g-0 d-flex justify-content-center",
                ),
            ],
            fluid=True,
        ),
        style={"box-shadow": "0 5px 5px -5px #333"},
        # className="bg-primary bg-gradient text-light text-center fs-6 fw-light border-top",
        className="bg-light bg-gradient text-primary text-center fs-6 fw-light border-top",
    )
