import dash_bootstrap_components as dbc

from snaptron_query.app import global_strings as gs, components as c_component


def get_text_gene_id(component_style):
    return c_component.get_text(component_style, gs.geq_gene_id)


def get_text_gene_coordinates(component_style):
    return c_component.get_text(component_style, gs.geq_gene_coord)


def get_text_gene_id_norm(component_style):
    return get_text_gene_id(component_style)


def get_text_gene_coordinates_norm(component_style):
    return c_component.get_text(component_style, gs.geq_gene_coord)


def get_input_gene_id():
    return c_component.get_input("some place holder for the gene", 'id-input-gene-id')


def get_input_gene_id_norm():
    return c_component.get_input("Gene ID placeholder", 'id-input-gene-id-norm', disabled='True')


def get_input_gene_coordinates():
    return c_component.get_input("gene coord placeholder", 'id-input-gene-coord')


def get_input_gene_coordinates_norm():
    return c_component.get_input("norm gene coord placeholder", 'id-input-gene-coord-norm', disabled='True')


def get_switch_normalize():
    return dbc.Switch(
        id='id-switch-normalize',
        label=gs.geq_normalized,
        className='text-success'
    )


def get_button_geq_results():
    """Wrapper function to retrieve the button component"""
    return dbc.Button(
        gs.geq_button_run,
        n_clicks=0,
        id='id-button-geq-run-query',
        size="md",  # button size
        class_name="btn-primary",
    )
