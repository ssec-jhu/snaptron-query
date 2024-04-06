import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
from dash import Dash, html, Input, Output, callback_context, no_update
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template

from snaptron_query.app import graphs, layout, global_strings as gs, exceptions, snaptron_client as sc, components
from snaptron_query.app.query_gene_expression import GeneExpressionQueryManager
from snaptron_query.app.query_junction_inclusion import JunctionInclusionQueryManager

# Initialize the app
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
bs_cdn = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
app = Dash(__name__,
           external_stylesheets=[dbc.themes.SANDSTONE, dbc_css])

load_figure_template(gs.dbc_template_name)


def read_srav3h():
    # TODO: read the rest of the meta data files here as they become available
    # read the file and make sure index is set to the rail id for fast lookup
    df = pd.read_csv('data/samples_SRAv3h.tsv', sep='\t',
                     usecols=gs.srav3h_meta_data_required_list,
                     dtype={'sample_description': 'string'}).set_index(gs.snpt_col_rail_id)
    return df.to_dict(orient='index')


# Meta data loaded in global space
dict_srav3h = read_srav3h()

# this is the main layout of the page with all tabs
app.layout = dbc.Container(
    [
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
    Output('id-ag-grid-display-jiq', 'style'),
    Output('id-ag-grid-jiq', 'rowData'),
    Output('id-ag-grid-jiq', 'columnDefs'),
    Output('id-alert-jiq', 'children'),

    Input('id-button-jiq-generate-results', 'n_clicks'),
    Input("id-input-compilation-jiq", "value"),
    Input("id-input-jiq-inc-junc", "value"),
    Input("id-input-jiq-exc-junc", "value"),
    prevent_initial_call=True,
    # Note: this requires the latest Dash 2.16
    running=[(Output("id-button-jiq-generate-results", "disabled"), True, False)]
)
def on_button_click_gen_results(n_clicks, compilation, inclusion_interval, exclusion_interval):
    #  this function gets called with every input change
    if callback_context.triggered_id != 'id-button-jiq-generate-results':
        raise PreventUpdate
    else:
        try:
            alert_message = None
            row_data = None
            column_defs = None
            if compilation and inclusion_interval and exclusion_interval:

                # make sure chromosome numbers match
                # if there is any error in the intervals, an exception will be thrown
                (exc_chr, exc_start, exc_end), (inc_chr, inc_start, inc_end) = (
                    sc.jiq_verify_coordinate_pairs(exclusion_interval, inclusion_interval))

                # RUN the URL and get results back from SNAPTRON
                # make sure you get results back
                df_snpt_results = sc.get_snpt_query_results_df(compilation, exclusion_interval, 'snaptron')
                # df_snpt_results = pd.read_csv('./tests/data/test_srav3h_chr19_4491836_4493702.tsv', sep='\t')

                if df_snpt_results.empty:
                    raise exceptions.EmptyResponse

                # Select the meta data that must be used
                # TODO: add the rest of the meta data as PI provides list
                if compilation == gs.compilation_srav3h:
                    # meta_data_df = df_srav3h
                    meta_data_dict = dict_srav3h
                else:
                    raise PreventUpdate

                # # Set upt the JIQ manager then run the Junction Inclusion Query
                jqm = JunctionInclusionQueryManager(exc_start, exc_end, inc_start, inc_end)
                # results returned are list of dictionaries which makes ag-grid load much faster,
                # Once can convert a dataframe to dict with orient set to records for the ag-grid as well.
                row_data = jqm.run_junction_inclusion_query(df_snpt_results, meta_data_dict)

                # Set the columnDefs for the ag-grid
                column_defs = graphs.get_junction_query_column_def()
            else:
                raise exceptions.MissingUserInputs

        except Exception as e:
            alert_message = exceptions.handle_exception(e)

    if alert_message:
        alert = components.get_alert(alert_message)
        return no_update, no_update, no_update, alert

    return {'display': 'block'}, row_data, column_defs, no_update


@app.callback(
    Output('id-histogram-jiq', 'figure'),
    Output('id-box-plot-jiq', 'figure'),
    Output('id-jiq-box-plot-col', 'width'),
    Output('id-jiq-histogram-col', 'width'),
    Output('id-display-graphs-jiq', 'style'),

    Input('id-ag-grid-jiq', 'rowData'),
    Input('id-ag-grid-jiq', 'virtualRowData'),
    Input('id-switch-jiq-lock-with-table', 'value'),
    Input('id-switch-jiq-log-psi-box-plot', 'value'),
    Input('id-switch-jiq-violin-box-plot', 'value'),
    Input('id-switch-jiq-log-psi-histogram', 'value'),
    Input('id-switch-jiq-log-y-histogram', 'value'),
    prevent_initial_call=True
)
def update_charts_jiq(row_data_from_table, filtered_row_data_from_table, lock_graph_data_with_table,
                      log_psi_values, violin_overlay,
                      histogram_log_psi, histogram_log_y):
    """
        Given the table data as input, it will update the relative graphs
    """
    if not row_data_from_table or not filtered_row_data_from_table:
        raise PreventUpdate

    if lock_graph_data_with_table:
        df = pd.DataFrame(filtered_row_data_from_table)
    else:
        df = pd.DataFrame(row_data_from_table)

    histogram = graphs.get_histogram_jiq(df, histogram_log_psi, histogram_log_y)
    box_plot = graphs.get_box_plot_jiq(df, log_psi_values, violin_overlay)
    col_width = {'size': 6}
    # when the component is hidden, then becomes visible, the original style is lost,
    # so I am putting it back again.
    display_style = {"box-shadow": "1px 2px 7px 0px grey", "border-radius": "10px", }
    return histogram, box_plot, col_width, col_width, display_style


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
    Output('id-ag-grid-display-geq', 'style'),
    Output('id-ag-grid-geq', 'rowData'),
    Output('id-ag-grid-geq', 'columnDefs'),
    Output('id-alert-geq', 'children'),
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
    prevent_initial_call=True,
    # Note: this requires latest Dash 2.16
    running=[(Output("id-button-geq-run-query", "disabled"), True, False)]
)
def on_button_click_gene_expression(n_clicks, compilation, use_coordinates,
                                    query_gene_id, query_gene_coordinates,
                                    normalize_data, norm_gene_id, norm_gene_coordinates):
    #  this function gets called with every input change
    if callback_context.triggered_id != 'id-button-geq-run-query':
        raise PreventUpdate
    else:
        try:
            alert_message = None
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
                    # meta_data_df = df_srav3h
                    meta_data_dict = dict_srav3h
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

                    geq.setup_normalization_data_method(norm_gene_id, df_snpt_results_norm, meta_data_dict)

                row_data = geq.run_gene_expression_query(query_gene_id, df_snpt_results_query, meta_data_dict)

                # ag-grid accepts list of dicts so passing in the data from storage that is saved as list of dict
                # saves times here. store_data = row_data.df.to_dict("records") Set the columnDefs for the ag-grid
                column_defs = graphs.get_gene_expression_query_column_def(normalize_data)
            else:
                raise exceptions.MissingUserInputs

        except Exception as e:
            alert_message = exceptions.handle_exception(e)

    if alert_message:
        alert = components.get_alert(alert_message)
        return no_update, no_update, no_update, alert
    else:
        return {'display': 'block'}, row_data, column_defs, no_update


@app.callback(
    Output('id-row-graph-geq-box', 'figure'),
    Output('id-row-graph-geq-hist', 'figure'),
    Output('id-geq-box-plot-col', 'width'),
    Output('id-geq-histogram-col', 'width'),
    Output('id-geq-histogram-col', 'style'),
    Output('id-display-graphs-geq', 'style'),

    Input('id-ag-grid-geq', 'rowData'),
    Input('id-ag-grid-geq', 'virtualRowData'),
    Input('id-switch-geq-lock-with-table', 'value'),
    Input('id-switch-geq-log-raw-box-plot', 'value'),
    Input('id-switch-geq-violin-raw-box-plot', 'value'),
    Input("id-switch-geq-normalize", 'value'),
    Input("id-switch-geq-log-count-histogram", 'value'),
    Input("id-switch-geq-log-y-histogram", 'value'),
    prevent_initial_call=True
)
def update_charts_geq(row_data_from_table, filtered_row_data_from_table, lock_graph_data_with_table,
                      log_values, violin_overlay, normalized_data,
                      histogram_log_x, histogram_log_y):
    """
        Given the table data as input, it will update the relative graphs
    """
    if not row_data_from_table or not filtered_row_data_from_table:
        raise PreventUpdate

    # don't update on these switches, their value is only important, not their trigger
    if callback_context.triggered_id == 'id-switch-geq-normalize':
        raise PreventUpdate

    if lock_graph_data_with_table:
        data = filtered_row_data_from_table
    else:
        data = row_data_from_table

    style = {"box-shadow": "1px 2px 7px 0px grey", "border-radius": "10px"}
    if normalized_data:
        # Filter out the -1 factors directly
        data = [row for row in data if row[gs.table_geq_col_factor] != -1]
        df = pd.DataFrame(data)
        # Make histogram
        histogram = graphs.get_histogram_geq(df, histogram_log_x, histogram_log_y)
        box_plot = graphs.get_box_plot_gene_expression(df, log_values, violin_overlay, normalized_data)
        # One option is also to have a html.DIV in the layout and send over the Row as
        # but them you need to also send the styling of the row here
        # child = dbc.Row([ dbc.Col(dcc.Graph the graph you want),dbc.Col(dcc.Graph the other graph)], className="g-0")
        width = {'size': 6}
        hist_display = {'display': 'Block'}
        return box_plot, histogram, width, width, hist_display, style
    else:
        df = pd.DataFrame(data)
        box_plot = graphs.get_box_plot_gene_expression(df, log_values, violin_overlay, normalized_data)
        width = {'size': 8, 'offset': 2}
        hist_display = {'display': 'None'}
        return box_plot, None, width, no_update, hist_display, style


@app.callback(
    Output("id-ag-grid-jiq", "exportDataAsCsv"),
    Output("id-ag-grid-jiq", "csvExportParams"),
    Input("id-button-jiq-download", "n_clicks"),
    prevent_initial_call=True
)
def jiq_export_data_as_csv(n_clicks):
    if callback_context.triggered_id == 'id-button-jiq-download':
        return True, {"fileName": "psi_query_data.csv"}
    else:
        raise PreventUpdate


@app.callback(
    Output("id-ag-grid-geq", "exportDataAsCsv"),
    Output("id-ag-grid-geq", "csvExportParams"),
    Input("id-button-geq-download", "n_clicks"),
    prevent_initial_call=True
)
def geq_export_data_as_csv(n_clicks):
    if callback_context.triggered_id == 'id-button-geq-download':
        return True, {"fileName": "gene_expression_query_data.csv"}
    else:
        raise PreventUpdate


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
