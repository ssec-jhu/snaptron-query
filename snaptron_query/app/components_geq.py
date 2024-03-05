import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc
from dash_iconify import DashIconify
from snaptron_query.app import global_strings as gs
from snaptron_query.app import components_jiq


def get_text_gene_id(component_style):
    return components_jiq.get_text(component_style, gs.gene_id)


def get_text_gene_coordinates(component_style):
    return components_jiq.get_text(component_style, gs.gene_coord)


def get_text_gene_id_norm(component_style):
    return get_text_gene_id(component_style,disabled='True')


def get_text_gene_coordinates_norm(component_style):
    return components_jiq.get_text(component_style, gs.gene_coord)

def get_input_gene_id():
    return components_jiq.get_input("some place holder for the gene", 'id-input-gene-id')


def get_input_gene_id_norm():
    return components_jiq.get_input("Gene ID placeholder", 'id-input-gene-id-norm',disabled='True')

def get_input_gene_coordinates():
    return components_jiq.get_input("gene coord placeholder", 'id-input-gene-coord')

def get_input_gene_coordinates_norm():
    return components_jiq.get_input("norm gene coord placeholder", 'id-input-gene-coord-norm',disabled='True')

def get_switch_normalize():
    return html.Div([dbc.Checkbox(
            id="id-switch-normalize",
            label="Normalize Counts",
            value=False,
        )],
        style={'float':'right'}
    )

def get_button_geq_results():
    """Wrapper function to retrieve the button component"""
    return dbc.Button(
        gs.button_run,
        n_clicks=0,
        id='id-button-geq-run-query',
        size="md",  # button size
        class_name="btn-primary",
    )
