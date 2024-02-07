import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
from dash import Dash, html, dcc, Input, Output
from dash.exceptions import PreventUpdate

from snaptron_query.app import graphs
from snaptron_query.app import layout
from snaptron_query.app import global_strings

# Initialize the app
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
bs_cdn = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
app = Dash(__name__,
           external_stylesheets=[dbc.themes.SANDSTONE,
                                 dbc_css,
                                 ])

# this is the main layout of the page with all tabs
app.layout = dbc.Container(
    [
        # app uses a dcc.store to store information needed between components from callbacks

        dcc.Store(id="id-store-info"),
        dcc.Store(id="id-store-jiq-df"),

        # navbar,# Top row with titles and all
        layout.get_navbar_top(),

        # Next row is are the tabs and their content
        dmc.Space(h=30),
        layout.get_tabs(),


        dmc.Space(h=30),
        html.Div(id="id-log-content"),
    ],
    fluid=True,  # this will make the page use full screen width
)


@app.callback(
    Output('id-store-info', 'data'),
    Output('id-store-jiq-df', 'data'),
    Input('id-button-generate-results', 'n_clicks'),
    Input(component_id="id-input-compilation", component_property="value"),
    Input(component_id="id-input-inc-junc", component_property="value"),
    Input(component_id="id-input-exc-junc", component_property="value"),
    Input('id-store-info', 'data'),
    prevent_initial_call=True
)
def on_button_click_gen_results(n_clicks, compilation, inc, exc, datasets):
    #  this function gets called with every input change, not just the button click
    if not datasets:
        datasets = dict(clicks=0, log='')

    old_click = datasets['clicks']
    if n_clicks <= old_click:
        raise PreventUpdate
    else:
        # ----------------------------------------
        #       Work In Progress Here
        # ----------------------------------------
        # Gather the form data and create the URL
        # TODO: hardcode URL for now
        chromosome_number = 19
        host = 'https://snaptron.cs.jhu.edu'
        query_type_string = 'snaptron'  # vs 'genes' for gene expression
        head = f'{host}/{compilation}/{query_type_string}?regions=chr{chromosome_number}' + ':'
        url = f'{head}{exc}{inc}'
        # url = 'https://snaptron.cs.jhu.edu/srav3h/snaptron?regions=chr19:4491836-4493702'
        # TODO: run the query and return result's data frame here
        # putting example data for now
        data = {
            'rail_id': [1, 2, 3, 4, 5],
            'external_id': [10, 20, 30, 40, 50],
            'study': ['AA', 'BB', 'CC', 'DD', 'EE'],
            'inc': [25, 30, 22, 28, 35],
            'exc': [25, 30, 22, 28, 35],
            'total': [25, 30, 22, 28, 35],
            'psi': [15, 26, 34, 5, 17],
        }
        results_df = pd.DataFrame(data)
        # ----------------------------------------

        data_dict = results_df.to_dict(orient='list')
        # keep track of any log needed
        log_msg = f'Click= {n_clicks}-URL={url[0]}'
        datasets['log'] = log_msg
        datasets['clicks'] = n_clicks

    return datasets, data_dict


@app.callback(
    Output('id-ag-grid', 'rowData'),
    Output('id-ag-grid', 'columnDefs'),
    Output('id-card-table', 'style'),
    Input('id-store-jiq-df', 'data'),
    Input('id-card-table', 'style'),
    prevent_initial_call=True
)
def update_table(data_from_store, current_style):
    if not data_from_store:
        raise PreventUpdate

    # convert data from storage to data frame and make sure the psi column is float type
    df = pd.DataFrame(data_from_store)
    df['psi'] = df['psi'].astype('float')
    row_data = df.to_dict("records")

    # Set the columnDefs for the ag-grid
    column_defs = graphs.get_junction_query_column_def()

    # TODO: other components' style needs to be none by default and turned on here
    # set component visibility
    current_style['display'] = 'block'

    # parentheses must be here, dash does not like it without it
    return (row_data, column_defs, current_style)  # grid


@app.callback(
    Output('id-histogram', 'figure'),
    Output('id-box-plot', 'figure'),
    Input('id-ag-grid', 'rowData'),
    Input('id-ag-grid', 'virtualRowData'),
    Input('id-switch-lock-with-table', 'value')
)
def update_charts(row_data_from_table, filtered_row_data_from_table, lock_graph_data_with_table):
    """
        Given the table data as input, it will update the relative graphs
    """
    if not row_data_from_table or not filtered_row_data_from_table:
        raise PreventUpdate

    if lock_graph_data_with_table:
        df = pd.DataFrame(filtered_row_data_from_table)
    else:
        df = pd.DataFrame(row_data_from_table)

    df[global_strings.table_jiq_col_psi] = df[global_strings.table_jiq_col_psi].astype('float')
    histogram = graphs.get_histogram(df)
    box_plot = graphs.get_box_plot(df)
    return histogram, box_plot


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
