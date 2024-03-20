import dash_ag_grid as dag
import dash_bootstrap_components as dbc

from snaptron_query.app import global_strings as gs


def get_switch_normalize():
    return dbc.Switch(
        id='id-switch-geq-normalize',
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
