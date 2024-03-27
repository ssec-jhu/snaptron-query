import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
from dash import Dash, html, dcc, Input, Output, callback_context
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template

from snaptron_query.app import graphs, layout, global_strings as gs, exceptions, snaptron_client as sc
from snaptron_query.app.query_junction_inclusion import JunctionInclusionQueryManager
from snaptron_query.app.query_gene_expression import GeneExpressionQueryManager

# Initialize the app
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
bs_cdn = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
app = Dash(__name__,
           external_stylesheets=[dbc.themes.SANDSTONE, dbc_css])

load_figure_template(gs.dbc_template_name)


def read_srav3h():
    # TODO: read the rest of the meta data files here as they become available
    # read the file and make sure index is set to the rail id for fast lookup
    return pd.read_csv('data/samples_SRAv3h.tsv', sep='\t',
                       usecols=gs.srav3h_meta_data_required_list,
                       dtype={'sample_description': 'string'}).set_index(gs.snpt_col_rail_id)


# Meta data loaded in global space
df_srav3h = read_srav3h()

# this is the main layout of the page with all tabs
app.layout = dbc.Container(
    [
        # app uses a dcc.store to store information needed between components from callbacks

        dcc.Store(id="id-store-info"),
        dcc.Store(id="id-store-info-geq"),
        dcc.Store(id="id-store-jiq-df"),
        dcc.Store(id="id-store-geq-df"),

        # navbar, top row with titles and all
        layout.get_navbar_top(),

        # Next row is are the tabs and their content
        dmc.Space(h=30),
        layout.get_tabs(),

        # a space for log content if any
        dmc.Space(h=30),
        html.Div(id="id-log-content"),
    ],
    # TODO: Keep this commented here, need to verify with PI rep to switch to full width or not
    # fluid=True,  # this will make the page use full screen width
)


@app.callback(
    Output('id-store-info', 'data'),
    Output('id-store-jiq-df', 'data'),
    Input('id-button-jiq-generate-results', 'n_clicks'),
    Input(component_id="id-input-compilation-jiq", component_property="value"),
    Input(component_id="id-input-jiq-inc-junc", component_property="value"),
    Input(component_id="id-input-jiq-exc-junc", component_property="value"),
    Input('id-store-info', 'data'),
    prevent_initial_call=True,
    running=[(Output("id-input-compilation-jiq", "disabled"), True, False)]
)
def on_button_click_gen_results(n_clicks, compilation, inclusion_interval, exclusion_interval, datasets):
    #  this function gets called with every input change, not just the button click
    if not datasets:
        datasets = dict(clicks=0, log='')

    # compare old clicks with the new clicks
    if n_clicks <= datasets.get('clicks', 0):
        raise PreventUpdate
    else:
        try:
            if compilation and inclusion_interval and exclusion_interval:

                # make sure chromosome numbers match
                # if there is any error in the intervals, an exception will be thrown
                (exc_chr, exc_start, exc_end), (inc_chr, inc_start, inc_end) = (
                    sc.jiq_verify_coordinate_pairs(exclusion_interval, inclusion_interval))

                # RUN the URL and get results back from SNAPTRON
                # make sure you get results back
                df_snpt_results = sc.get_snpt_query_results_df(compilation, exclusion_interval, 'snaptron')
                if df_snpt_results.empty:
                    raise exceptions.EmptyResponse

                # Select the meta data that must be used
                # TODO: add the rest of the meta data as PI provides list
                if compilation == gs.compilation_srav3h:
                    df_meta_data = df_srav3h
                else:
                    raise PreventUpdate

                # # Set upt the JIQ manager then run the Junction Inclusion Query
                jqm = JunctionInclusionQueryManager(exc_start, exc_end, inc_start, inc_end)
                results_list_of_dict = jqm.run_junction_inclusion_query(df_snpt_results, df_meta_data)

                # Performance Note: ag-grid will load much faster with a lists of dictionaries, so I am storing
                # it as such. Once can convert a dataframe to dict with orient set to records for the ag-grid as well.
                table_data = results_list_of_dict
            else:
                raise exceptions.MissingUserInputs

        # TODO: setup UI for error messages
        except exceptions.BadURL:
            print("URL was bad")
            raise PreventUpdate
        except exceptions.EmptyResponse:
            print("URL was correct but server returned empty response")
            raise PreventUpdate
        except exceptions.MissingUserInputs or exceptions.BadCoordinates:
            print("Some user input error")
            raise PreventUpdate
        except exceptions.EmptyJunction:
            print("Requested Junction has no sample data")
            raise PreventUpdate
        except Exception as e:
            # Any other exception happens I want it forwarded to the front end for handling
            print(f"Exception: {e}")
            raise PreventUpdate

        # keep track of any log needed
        log_msg = f'Click= {n_clicks}'
        datasets['log'] = log_msg
        datasets['clicks'] = n_clicks

    return datasets, table_data


@app.callback(
    Output('id-ag-grid-jiq', 'rowData'),
    Output('id-ag-grid-jiq', 'columnDefs'),
    Output('id-card-table', 'style'),
    Input('id-store-jiq-df', 'data'),
    Input('id-card-table', 'style'),
    prevent_initial_call=True
)
def update_table(data_from_store, current_style):
    if not data_from_store:
        raise PreventUpdate

    # ag-grid accepts list of dicts so passing in the data from storage that is saved as list of dict saves times here.
    row_data = data_from_store

    # Set the columnDefs for the ag-grid
    column_defs = graphs.get_junction_query_column_def()

    # TODO: other components' style needs to be none by default and turned on here
    # set component visibility
    current_style['display'] = 'block'

    # parentheses must be here, dash does not like it without it
    return row_data, column_defs, current_style  # grid


@app.callback(
    Output('id-histogram-jiq', 'figure'),
    Output('id-box-plot-jiq', 'figure'),
    Input('id-ag-grid-jiq', 'rowData'),
    Input('id-ag-grid-jiq', 'virtualRowData'),
    Input('id-switch-jiq-lock-with-table', 'value'),
    Input('id-switch-jiq-log-box-plot', 'value'),
    Input('id-switch-jiq-violin-box-plot', 'value'),
    prevent_initial_call=True
)
def update_charts(row_data_from_table, filtered_row_data_from_table, lock_graph_data_with_table,
                  log_psi_values, violin_overlay):
    """
        Given the table data as input, it will update the relative graphs
    """
    if not row_data_from_table or not filtered_row_data_from_table:
        raise PreventUpdate

    if lock_graph_data_with_table:
        df = pd.DataFrame(filtered_row_data_from_table)
    else:
        df = pd.DataFrame(row_data_from_table)

    histogram = graphs.get_histogram_jiq(df)
    box_plot = graphs.get_box_plot_jiq(df, log_psi_values, violin_overlay)
    return histogram, box_plot


@app.callback(
    Output('id-row-query-gene-coordinates', 'style'),
    Output('id-row-norm-gene-coordinates', 'style'),
    Input('id-checkbox-use-coordinates', 'value'),
    prevent_initial_call=True
)
def enable_coordinate_inputs(use_coordinates):
    if use_coordinates:
        display = {'display': 'block'}
    else:
        display = {'display': 'none'}

    return display, display


@app.callback(
    Output('id-input-geq-gene-id-norm', 'disabled'),
    Output('id-input-geq-gene-coord-norm', 'disabled'),
    Input('id-switch-geq-normalize', 'value'),
    prevent_initial_call=True
)
def enable_normalization(normalize_value):
    # if normalize_value is on, then the inputs for the normalization gene should be turned
    # in other words disabled=False
    norm_gene_id_enable = not normalize_value
    norm_gene_coord_enable = not normalize_value
    return norm_gene_id_enable, norm_gene_coord_enable


@app.callback(
    Output('id-store-info-geq', 'data'),
    Output('id-store-geq-df', 'data'),
    Input('id-button-geq-run-query', 'n_clicks'),
    Input("id-input-compilation-geq", "value"),
    Input("id-checkbox-use-coordinates", 'value'),
    # Query Gene Info
    Input("id-input-geq-gene-id", "value"),
    Input("id-input-geq-gene-coord", "value"),
    # Norm Gene Info
    Input("id-switch-geq-normalize", 'value'),
    Input("id-input-geq-gene-id-norm", "value"),
    Input("id-input-geq-gene-coord-norm", "value"),
    Input('id-store-info', 'data'),
    prevent_initial_call=True,
    # TODO: figure this out, why doesn't it turn gray?
    # running=[(Output("id-button-geq-run-query", "disabled"), True, False)]
)
def on_button_click_gene_expression(n_clicks, compilation, use_coordinates,
                                    query_gene_id, query_gene_coordinates,
                                    normalize_data, norm_gene_id, norm_gene_coordinates, datasets):
    #  this function gets called with every input change, not just the button click
    if not datasets:
        datasets = dict(clicks=0, log='')

    # compare old clicks with the new clicks
    # if n_clicks <= datasets.get('clicks', 0):
    input_id = callback_context.triggered_id
    if input_id != 'id-button-geq-run-query':
        raise PreventUpdate
    else:
        try:
            if compilation and query_gene_id:

                # if normalize_data and (not norm_gene_coordinates or not gene_id_norm):
                #     raise PreventUpdate
                if normalize_data and (not norm_gene_id):
                    raise exceptions.MissingUserInputs

                if use_coordinates:
                    if not query_gene_coordinates or (normalize_data and (not norm_gene_coordinates)):
                        raise exceptions.MissingUserInputs

                # Verify the gene coordinates string, we don't need the return values for this query
                if use_coordinates:
                    sc.geq_verify_coordinate(query_gene_coordinates)
                    # RUN the URL and get results back from SNAPTRON
                    df_snpt_results_query = sc.get_snpt_query_results_df(compilation=compilation,
                                                                         region=query_gene_coordinates,
                                                                         query_mode='genes')
                else:
                    # TODO: how do you verify the gene ID
                    df_snpt_results_query = sc.get_snpt_query_results_df(compilation=compilation,
                                                                         region=query_gene_id,
                                                                         query_mode='genes')
                if df_snpt_results_query.empty:
                    raise exceptions.EmptyResponse

                # Select the meta data that must be used
                # TODO: add the rest of the meta data as PI provides list
                if compilation == gs.compilation_srav3h:
                    df_meta_data = df_srav3h
                else:
                    raise PreventUpdate

                # Set upt the GEX manager then run the Query
                # Create normalization table if needed
                geq = GeneExpressionQueryManager()
                if normalize_data:
                    if use_coordinates:
                        sc.geq_verify_coordinate(norm_gene_coordinates)
                        df_snpt_results_norm = sc.get_snpt_query_results_df(compilation=compilation,
                                                                            region=norm_gene_coordinates,
                                                                            query_mode='genes')
                    else:
                        df_snpt_results_norm = sc.get_snpt_query_results_df(compilation=compilation,
                                                                            region=norm_gene_id,
                                                                            query_mode='genes')
                    if df_snpt_results_norm.empty:
                        raise exceptions.EmptyResponse

                    geq.setup_normalization_data_method_2(norm_gene_id, df_snpt_results_norm, df_meta_data)

                table_data = geq.run_gene_expression_query(query_gene_id, df_snpt_results_query, df_meta_data)

            else:
                raise exceptions.MissingUserInputs

        # TODO: setup UI for error messages
        except exceptions.BadURL:
            print("URL was bad")
            raise PreventUpdate
        except exceptions.EmptyResponse:
            print("URL was correct but server returned empty response")
            raise PreventUpdate
        except exceptions.MissingUserInputs or exceptions.BadCoordinates:
            print("Some user input error")
            raise PreventUpdate
        except exceptions.EmptyJunction:
            print("Requested Junction has no sample data")
            raise PreventUpdate
        except Exception as e:
            # Any other exception happens I want it forwarded to the front end for handling
            print(f"Exception: {e}")
            raise PreventUpdate

        # keep track of any log needed
        log_msg = f'Click= {n_clicks}'
        datasets['log'] = log_msg
        datasets['clicks'] = n_clicks

    return datasets, table_data


@app.callback(
    Output('id-ag-grid-geq', 'rowData'),
    Output('id-ag-grid-geq', 'columnDefs'),
    Output('id-card-table-geq', 'style'),
    Input('id-store-geq-df', 'data'),
    Input('id-card-table-geq', 'style'),
    Input("id-switch-geq-normalize", 'value'),
    prevent_initial_call=True
)
def update_table_geq(data_from_store, current_style, normalized_gex):
    if not data_from_store:
        raise PreventUpdate

    # ag-grid accepts list of dicts so passing in the data from storage that is saved as list of dict saves times here.
    row_data = data_from_store

    # Set the columnDefs for the ag-grid
    column_defs = graphs.get_gene_expression_query_column_def(normalized_gex)

    # TODO: other components' style needs to be none by default and turned on here
    # set component visibility
    current_style['display'] = 'block'

    # parentheses must be here, dash does not like it without it
    return row_data, column_defs, current_style  # grid


@app.callback(
    Output('id-row-graph-geq', 'children'),
    Input('id-ag-grid-geq', 'rowData'),
    Input('id-ag-grid-geq', 'virtualRowData'),
    Input('id-switch-geq-lock-with-table', 'value'),
    Input('id-switch-geq-log-raw-box-plot', 'value'),
    Input('id-switch-geq-violin-raw-box-plot', 'value'),
    Input("id-switch-geq-normalize", 'value'),
    prevent_initial_call=True
)
def update_charts_geq(row_data_from_table, filtered_row_data_from_table, lock_graph_data_with_table,
                      log_values, violin_overlay, normalized_data):
    """
        Given the table data as input, it will update the relative graphs
    """
    if not row_data_from_table or not filtered_row_data_from_table:
        raise PreventUpdate

    if lock_graph_data_with_table:
        df = pd.DataFrame(filtered_row_data_from_table)
    else:
        df = pd.DataFrame(row_data_from_table)

    if normalized_data:
        df = df.loc[df[gs.table_geq_col_factor] != -1]
    if normalized_data:
        histogram = graphs.get_histogram_geq(df)
    else:
        histogram = None

    box_plot = graphs.get_box_plot_gene_expression(df, log_values, violin_overlay, normalized_data)

    if normalized_data:
        # One option is also to have a html.DIV in the layout and send over the Row as
        # but them you need to also send the styling of the row here
        # child = dbc.Row([ dbc.Col(dcc.Graph the graph you want),dbc.Col(dcc.Graph the other graph)], className="g-0")
        row_child = [dbc.Col(dcc.Graph(figure=box_plot), width=6), dbc.Col(dcc.Graph(figure=histogram), width=6)]
    else:
        row_child = [dbc.Col(dcc.Graph(figure=box_plot), width=12)]

    # return dcc.Graph(figure=box_plot), dcc.Graph(figure=histogram), child
    return row_child


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
