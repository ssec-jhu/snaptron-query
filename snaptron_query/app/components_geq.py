import dash_ag_grid as dag
import dash_bootstrap_components as dbc

from snaptron_query.app import components, global_strings as gs


def get_text_gene_id(component_style):
    return components.get_text(component_style, gs.geq_gene_id)


def get_text_gene_coordinates(component_style):
    return components.get_text(component_style, gs.geq_gene_coord)


def get_text_gene_id_norm(component_style):
    return get_text_gene_id(component_style)


def get_text_gene_coordinates_norm(component_style):
    return components.get_text(component_style, gs.geq_gene_coord)


def get_input_gene_id():
    return components.get_input(gs.geq_gene_id_placeholder, 'id-input-gene-id')


def get_input_gene_id_norm():
    return components.get_input(gs.geq_gene_id_norm_placeholder, 'id-input-gene-id-norm', disabled='True')


def get_input_gene_coordinates():
    return components.get_input(gs.geq_gene_coord_placeholder, 'id-input-gene-coord')


def get_input_gene_coordinates_norm():
    return components.get_input(gs.geq_gene_coord_norm_placeholder, 'id-input-gene-coord-norm', disabled='True')


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


def get_switch_lock_data_with_table_geq():
    return components.get_switch_lock_data_with_table('id-switch-lock-with-table-geq', gs.switch_lock)


def get_table_geq():
    table = dag.AgGrid(
        id="id-ag-grid-geq",
        persistence=True,  # https://community.plotly.com/t/how-to-add-persistence-to-dash-ag-grid/74944
        style={'height': 600},
        defaultColDef={"flex": 1,  # snaps the end
                       "sortable": True, "resizable": True, "filter": True,
                       },
        dashGridOptions={'rowSelection': 'multiple',
                         'checkboxSelection': 'True',
                         'isRowSelectable': {"function": "log(params)"},
                         'pagination': True,
                         },
    )
    return table
