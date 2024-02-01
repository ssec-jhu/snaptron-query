import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
from dash import Dash, html, dcc, Input, Output
from dash.exceptions import PreventUpdate

import graphs
import layout
from query_junction_inclusion import JunctionInclusionQueryManager as jiq_mgr
from snaptron_client import SnaptronClientManager

# Initialize the app
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
bs_cdn = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
app = Dash(__name__,
           suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.SANDSTONE,
                                 dbc_css,
                                 # bs_cdn,
                                 # dbc.icons.BOOTSTRAP
                                 ])

# this is the main layout of the page with all tabs
app.layout = dbc.Container(
    [
        # app uses a dcc.store to store information needed between components from callbacks
        # this is stored in the user's browser session
        # data must be in some JSON format
        dcc.Store(id="id-store-info", storage_type='memory'),
        # dcc.Store(id="id-store-info2", storage_type='memory'),
        dcc.Store(id="id-store-jiq-df", storage_type='memory'),

        # navbar,# Top row with titles and all
        layout.jumbotron,

        # Next row is are the tabs and their content
        dmc.Space(h=30),
        layout.tab_horizontal_bootstrap,
        # other options
        # layout.tab_horizontal_styled,
        # layout.tab_vertical_styled,
        # layout_jiq.junction_inclusion_query_layout,

        dmc.Space(h=30),
        html.Div(id="id-log-content",
                 # style={'display:none'}
                 ),
    ],
    # fluid=True, # this will make the page use full screen width
    # className='container-fluid'
)


@app.callback(
    Output('id-store-info', 'data'),
    Output('id-store-jiq-df', 'data'),
    Input('id-button-generate-results', 'n_clicks'),
    Input(component_id="id-input-compilation", component_property="value"),
    Input(component_id="id-input-inc-junc", component_property="value"),
    Input(component_id="id-input-exc-junc", component_property="value"),
    Input('id-store-info', 'data'),
    # allow_duplicate=True,
    prevent_initial_call=True
)
def on_button_click_gen_results(n_clicks, compilation, inc, exc, datasets):
    # TODO this function gets called with every input change, not just the button click,
    #  need to narrow to just the button click

    # if n_clicks is None:
    #     #return no_update
    #     raise PreventUpdate

    if not datasets:
        datasets = dict(clicks=0, log='')
        # data_dict = dict()

    old_click = datasets['clicks']
    if n_clicks <= old_click:
        raise PreventUpdate
    else:
        # Gather the form data and create the URL
        # TODO: hardcode URL for now
        chromosome_number =19
        host = 'https://snaptron.cs.jhu.edu'
        query_type_string = 'snaptron'  # vs 'genes' for gene expression
        head = f'{host}/{compilation}/{query_type_string}?regions=chr{chromosome_number}' + ':'
        url = f'{head}{exc}'
        url = 'https://snaptron.cs.jhu.edu/srav3h/snaptron?regions=chr19:4491836-4493702'

        (inclusion_start, inclusion_end) = inc.split('-')
        (exclusion_start, exclusion_end) = exc.split('-')

        # RUN the URL and get results back from SNAPTRON
        sqm = SnaptronClientManager(url)
        df = sqm.get_query_results_dataframe()

        # Process the results returned and run the Junction Inclusion Query
        jqm = jiq_mgr(int(exclusion_start),
                      int(exclusion_end),
                      int(inclusion_start),
                      int(inclusion_end))

        results_df = jqm.run_junction_inclusion_query(df)

        # prepare to put into session storage
        data_dict = results_df.to_dict(orient='list')

        # keep track of any log needed
        nl = '\n'
        log_msg = f'Button clicked {n_clicks} times.{nl} URL={url[0]}.'
        datasets['log'] = log_msg
        datasets['clicks'] = n_clicks  # update the clicks info for reducing callbacks

    return datasets, data_dict


@app.callback(
    # Output('id-table', 'children'),
    Output('id-ag-grid', 'rowData'),
    Output('id-ag-grid', 'columnDefs'),
    Output('id-card-table', 'style'),
    Input('id-store-jiq-df', 'data'),
    Input('id-card-table', 'style'),
    # allow_duplicate=True,
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

    # parentheses must be here
    return (row_data, column_defs, current_style)  # grid


@app.callback(
    Output('id-histogram', 'figure'),
    Output('id-log-content', 'children'),
    Output('id-box-plot', 'figure'),

    Input('id-ag-grid', 'rowData'),
    Input('id-ag-grid', 'virtualRowData'),
    Input('id-switch-lock-with-table', 'value')
)
def update_charts(row_data_from_table, filtered_row_data_from_table, lock_graph_data_with_table):
    if not row_data_from_table or not filtered_row_data_from_table:
        raise PreventUpdate

    if lock_graph_data_with_table:
        df = pd.DataFrame(filtered_row_data_from_table)
    else:
        df = pd.DataFrame(row_data_from_table)

    df['psi'] = df['psi'].astype('float')
    histogram = graphs.get_histogram(df)
    box_plot = graphs.get_box_plot(df)
    log = f'testing'
    return histogram, log, box_plot


# @app.callback(
#     Output('log-content', 'children'),
#     Input('id-store', 'data'),
#     # allow_duplicate=True,
#     prevent_initial_call=True
# )
# def update_log(data):
#     if data:
#         # datasets = json.loads(data)
#         return data.get('log', '')


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
