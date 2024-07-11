import os

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
from dash import Dash, Input, Output, ctx, no_update, State, dcc, ClientsideFunction, Patch
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template

from snaptron_query.app import callback_common as callback, inline_styles as styles, navbars, paths
from snaptron_query.app import (
    graphs,
    layout,
    components,
    utils,
    exceptions,
    global_strings as gs,
    runner_geq,
    runner_jiq,
)

# Initialize the app
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(
    __name__,
    title=gs.web_title,
    external_stylesheets=[dbc.themes.SANDSTONE, dbc_css, dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME],
)

# VERY important line of code for running with gunicorn
# you run the 'server' not the 'app'. VS. you run the 'app' with uvicorn
server = app.server

load_figure_template(gs.dbc_template_name)

# TODO: remove this code for final deployment
# Sanity check for the metadata directory
dir_list = os.listdir(paths.meta_data_directory)
if len(dir_list) == 0:
    print(f"**** WARNING **** Snaptron Meta data files are missing from:{paths.meta_data_directory}")

# Meta data loaded in global space
dict_srav3h = utils.read_srav3h(paths.srav3h_meta)
dict_gtexv2 = utils.read_gtexv2(paths.gtexv2_meta)
dict_tcgav2 = utils.read_tcgav2(paths.tcgav2_meta)
dict_srav1m = utils.read_srav1m(paths.srav1m_meta)


def get_meta_data(compilation):
    if compilation == gs.compilation_srav3h:
        return dict_srav3h
    elif compilation == gs.compilation_gtexv2:
        return dict_gtexv2
    elif compilation == gs.compilation_tcgav2:
        return dict_tcgav2
    elif compilation == gs.compilation_srav1m:
        return dict_srav1m
    else:
        raise PreventUpdate


# this is the main layout of the page with all tabs
app.layout = dbc.Container(
    [
        # navbar, top row with titles and all
        navbars.get_navbar_top(),
        # Next row is are the tabs and their content
        dmc.Space(h=30),
        layout.get_tabs(),
        dmc.Space(h=30),
        navbars.get_navbar_bottom(),
        # a space for log content if any
        dmc.Space(h=30),
        dcc.Store(id="id-store-jiq-junctions"),
    ],
    # TODO: Keep this commented here, need to verify with PI rep to switch to full width or not
    # fluid=True,  # this will make the page use full screen width
)


@app.callback(
    Output("id-ag-grid-display-jiq", "style"),
    Output("id-ag-grid-jiq", "rowData"),
    Output("id-ag-grid-jiq", "columnDefs"),
    Output("id-ag-grid-jiq", "filterModel"),
    Output("id-loading-table-jiq", "children"),
    Output("id-alert-jiq", "children"),
    # figure related outputs
    Output("id-histogram-jiq", "figure"),
    Output("id-box-plot-jiq", "figure"),
    Output("id-jiq-box-plot-col", "width"),
    Output("id-jiq-histogram-col", "width"),
    Output("id-display-graphs-jiq", "style"),
    # ------- INPUTS ------
    Input("id-button-jiq-generate-results", "n_clicks"),
    State("id-input-compilation-jiq", "value"),
    State("id-jiq-input-container", "children"),
    State("id-store-jiq-junctions", "data"),
    # figure related states
    State("id-switch-jiq-log-psi-box-plot", "value"),
    State("id-switch-jiq-violin-box-plot", "value"),
    State("id-switch-jiq-log-psi-histogram", "value"),
    State("id-switch-jiq-log-y-histogram", "value"),
    prevent_initial_call=True,
    running=[(Output("id-button-jiq-generate-results", "disabled"), True, False)],  # requires the latest Dash 2.16
)
def on_button_click_jiq(
    n_clicks, compilation, children, junction_count, box_log_psi, violin_overlay, histogram_log_psi, histogram_log_y
):
    #  this function gets called with every input change
    if ctx.triggered_id != "id-button-jiq-generate-results":
        raise PreventUpdate
    else:
        try:
            alert_message = None
            row_data = None
            column_defs = None
            if not compilation:
                raise exceptions.MissingUserInputs

            if junction_count is None:  # first call
                junction_count = 0

            row_data, column_defs, filter_model, histogram, box_plot, col_width, col_width, display_style = (
                runner_jiq.run_query(
                    meta_data_dict=get_meta_data(compilation),
                    compilation=compilation,
                    children=children,
                    junction_count=junction_count,
                    box_log_psi=box_log_psi,
                    violin_overlay=violin_overlay,
                    histogram_log_psi=histogram_log_psi,
                    histogram_log_y=histogram_log_y,
                )
            )

        except Exception as e:
            alert_message = exceptions.alert_message_from_exception(e)

    if alert_message:
        alert = components.get_alert(alert_message)
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            alert,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
        )

    return (
        {"display": "block"},
        row_data,
        column_defs,
        filter_model,
        {},
        no_update,
        histogram,
        box_plot,
        col_width,
        col_width,
        display_style,
    )


@app.callback(
    Output("id-histogram-jiq", "figure", allow_duplicate=True),
    Output("id-box-plot-jiq", "figure", allow_duplicate=True),
    # Output("id-loading-graph-jiq", "children"),
    State("id-ag-grid-jiq", "rowData"),
    Input("id-ag-grid-jiq", "virtualRowData"),
    Input("id-switch-jiq-lock-with-table", "value"),
    Input("id-switch-jiq-log-psi-box-plot", "value"),
    Input("id-switch-jiq-violin-box-plot", "value"),
    Input("id-switch-jiq-log-psi-histogram", "value"),
    Input("id-switch-jiq-log-y-histogram", "value"),
    prevent_initial_call=True,
)
def update_charts_jiq(
    row_data_from_table,
    filtered_row_data_from_table,
    lock_graph_data_with_table,
    box_log_psi,
    violin_overlay,
    histogram_log_psi,
    histogram_log_y,
):
    """
    Given the table data as input, it will update the relative graphs
    """
    if not row_data_from_table or not filtered_row_data_from_table:
        raise PreventUpdate

    if lock_graph_data_with_table:
        df = pd.DataFrame(filtered_row_data_from_table)
    else:
        df = pd.DataFrame(row_data_from_table)

    # count how many psi columns we have
    list_of_calculated_junctions = [col for col in df.columns if col.startswith(gs.table_jiq_col_psi)]
    histogram = graphs.get_histogram_jiq(df, histogram_log_psi, histogram_log_y, list_of_calculated_junctions)
    box_plot = graphs.get_box_plot_jiq(df, box_log_psi, violin_overlay, list_of_calculated_junctions)

    return histogram, box_plot  # , {}


@app.callback(
    Output("id-store-jiq-junctions", "data"),
    Input("id-button-jiq-add-more-junctions", "n_clicks"),
    State("id-store-jiq-junctions", "data"),
    # Don't prevent initial call back as this sets the junction count value
)
def on_add_junction_click(n_clicks, junction_counts):
    if junction_counts is None:  # first call
        return 0

    if junction_counts < 5:
        return junction_counts + 1
    else:
        raise PreventUpdate


@app.callback(
    Output("id-row-input-jiq-1", "style"),
    Output("id-row-input-jiq-2", "style"),
    Output("id-row-input-jiq-3", "style"),
    Output("id-row-input-jiq-4", "style"),
    Input("id-button-jiq-add-more-junctions", "n_clicks"),
    Input("id-store-jiq-junctions", "data"),
    prevent_initial_call=True,
)
def update_junction_inputs(n_clicks, junction_counts):
    # changing row style for visibility throws off the whole layout
    # https://community.plotly.com/t/setting-style-causes-layout-issue/60403
    # need to ensure I put back the original 'flex' not just a 'block' display
    if junction_counts == 1:
        style_1 = {"display": "flex"}
        return style_1, no_update, no_update, no_update
    elif junction_counts == 2:
        style_2 = {"display": "flex"}
        return no_update, style_2, no_update, no_update
    elif junction_counts == 3:
        style_3 = {"display": "flex"}
        return no_update, no_update, style_3, no_update
    elif junction_counts == 4:
        style_4 = {"display": "flex"}
        return no_update, no_update, no_update, style_4
    else:
        raise PreventUpdate


@app.callback(
    Output("id-row-query-gene-coordinates", "style"),
    Output("id-row-norm-gene-coordinates", "style"),
    Input("id-checkbox-use-coordinates", "value"),
    prevent_initial_call=True,
)
def enable_coordinate_inputs(use_coordinates):
    if use_coordinates:
        display = {"display": "block"}
    else:
        display = {"display": "none"}

    return display, display


@app.callback(
    Output("id-input-geq-gene-id-norm", "disabled"),
    Output("id-input-geq-gene-coord-norm", "disabled"),
    Input("id-switch-geq-normalize", "value"),
    prevent_initial_call=True,
)
def enable_normalization(normalize_value):
    # if normalize_value is on, then the inputs for the normalization gene should be turned
    # in other words disabled=False
    norm_gene_id_enable = not normalize_value
    norm_gene_coord_enable = not normalize_value
    return norm_gene_id_enable, norm_gene_coord_enable


@app.callback(
    Output("id-ag-grid-display-geq", "style"),
    Output("id-ag-grid-geq", "rowData"),
    Output("id-ag-grid-geq", "columnDefs"),
    Output("id-ag-grid-geq", "filterModel"),
    Output("id-loading-table-geq", "children"),
    Output("id-alert-geq", "children"),
    # figure related outputs
    Output("id-geq-box-plot", "figure"),
    Output("id-geq-histogram", "figure"),
    # Output("id-store-geq-box", "data"),
    # Output("id-store-geq-hist", "data"),
    Output("id-geq-box-plot-col", "width"),
    Output("id-geq-histogram-col", "width"),
    Output("id-geq-histogram-col", "style"),
    Output("id-display-graphs-geq", "style"),
    # ----- Inputs -----
    Input("id-button-geq-run-query", "n_clicks"),
    State("id-input-compilation-geq", "value"),
    State("id-checkbox-use-coordinates", "value"),
    State("id-input-geq-gene-id", "value"),  # Query Gene Info
    State("id-input-geq-gene-coord", "value"),
    State("id-switch-geq-normalize", "value"),  # Norm Gene Info
    State("id-input-geq-gene-id-norm", "value"),
    State("id-input-geq-gene-coord-norm", "value"),
    # figure related states
    State("id-switch-geq-log-raw-box-plot", "value"),
    State("id-switch-geq-violin-raw-box-plot", "value"),
    # State("id-switch-geq-normalize", "value"),
    State("id-switch-geq-log-count-histogram", "value"),
    State("id-switch-geq-log-y-histogram", "value"),
    prevent_initial_call=True,
    running=[(Output("id-button-geq-run-query", "disabled"), True, False)],  # requires latest Dash 2.16
)
def on_button_click_geq(
    n_clicks,
    compilation,
    use_coordinates,
    query_gene_id,
    query_gene_coordinates,
    normalize_data,
    norm_gene_id,
    norm_gene_coordinates,
    box_plot_log_x,
    violin_overlay,
    histogram_log_x,
    histogram_log_y,
):
    #  this function gets called with every input change
    if ctx.triggered_id != "id-button-geq-run-query":
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

                # RUN THE GEX QUERY with the UI inputs
                (row_data, column_defs, filter_model, box_plot, histogram, width_box, width_hist, hist_display) = (
                    runner_geq.run_query(
                        # Select the metadata that must be used
                        meta_data_dict=get_meta_data(compilation),
                        normalize_data=normalize_data,
                        use_coordinates=use_coordinates,
                        norm_gene_coordinates=norm_gene_coordinates,
                        query_gene_coordinates=query_gene_coordinates,
                        compilation=compilation,
                        norm_gene_id=norm_gene_id,
                        query_gene_id=query_gene_id,
                        histogram_log_x=histogram_log_x,
                        histogram_log_y=histogram_log_y,
                        box_plot_log_x=box_plot_log_x,
                        violin_overlay=violin_overlay,
                    )
                )

            else:
                raise exceptions.MissingUserInputs
        except Exception as e:
            alert_message = exceptions.alert_message_from_exception(e)

    if alert_message:
        alert = components.get_alert(alert_message)
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            alert,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
        )
    else:
        return (
            {"display": "block"},
            row_data,
            column_defs,
            filter_model,
            {},
            no_update,  # alert
            box_plot,
            histogram,
            width_box,
            width_hist,
            hist_display,
            styles.section,
        )


# this was slower than the client side callback
# @app.callback(
#     Output("id-geq-histogram", "figure", allow_duplicate=True),
#     Input("id-switch-geq-log-y-histogram", "value"),
#     prevent_initial_call=True,
# )
# def update_geq_histogram_log_y(log_y):
#     patched_fig = Patch()
#     if log_y:
#         patched_fig.layout.yaxis['type'] = 'log'
#
#     return patched_fig


app.clientside_callback(
    ClientsideFunction(namespace="geq_clientside", function_name="update_histogram_log_y"),
    Output("id-geq-histogram", "figure", allow_duplicate=True),
    Input("id-switch-geq-log-y-histogram", "value"),
    State("id-geq-histogram", "figure"),
    prevent_initial_call=True,
)

app.clientside_callback(
    ClientsideFunction(namespace="geq_clientside", function_name="update_histogram_data"),
    Output("id-geq-histogram", "figure", allow_duplicate=True),
    Input("id-switch-geq-log-count-histogram", "value"),
    Input("id-switch-geq-lock-with-table", "value"),
    Input("id-ag-grid-geq", "virtualRowData"),
    State("id-ag-grid-geq", "rowData"),
    State("id-geq-histogram", "figure"),
    prevent_initial_call=True,
)

app.clientside_callback(
    ClientsideFunction(namespace="geq_clientside", function_name="update_box_plot_violin"),
    Output("id-geq-box-plot", "figure", allow_duplicate=True),
    Input("id-switch-geq-violin-raw-box-plot", "value"),
    Input("id-switch-geq-show-points", "value"),
    State("id-geq-box-plot", "figure"),
    prevent_initial_call=True,
)


# app.clientside_callback(
#     ClientsideFunction(namespace='geq_clientside',
#                        function_name='update_box_plot_data'),
#     Output("id-geq-box-plot", "figure", allow_duplicate=True),
#     Input("id-switch-geq-log-raw-box-plot", 'value'),
#     Input('id-switch-geq-lock-with-table', 'value'),
#     Input('id-ag-grid-geq', 'virtualRowData'),
#     State('id-ag-grid-geq', 'rowData'),
#     State("id-geq-box-plot", "figure"),
#     prevent_initial_call=True
# )


@app.callback(
    Output("id-geq-box-plot", "figure", allow_duplicate=True),
    Input("id-switch-geq-log-raw-box-plot", "value"),
    Input("id-switch-geq-lock-with-table", "value"),
    State("id-switch-geq-normalize", "value"),
    Input("id-ag-grid-geq", "virtualRowData"),
    # State('id-ag-grid-geq', 'rowData'),
    prevent_initial_call=True,
)
def update_box_plot_data(log_x, lock_with_table, normalized_count, virtual_row_data):
    if virtual_row_data and lock_with_table:
        patched_fig = Patch()

        # TODO: does this need to apply if normalized, or is this taken care of in the filter model?
        # data = [row for row in data if row[gs.table_geq_col_factor] != -1]
        df = pd.DataFrame(virtual_row_data)

        # handle general items
        rail_id_list_of_lists = df[gs.snpt_col_rail_id].apply(lambda x: [x]).tolist()
        patched_fig.data[0]["customdata"] = rail_id_list_of_lists
        patched_fig.data[0].y = df[gs.table_geq_col_log_2_raw] if log_x else df[gs.table_geq_col_raw_count]
        patched_fig.layout.yaxis.title = (gs.geq_box_plot_y_axes_log if log_x else gs.geq_box_plot_y_axes,)

        if normalized_count:
            patched_fig.data[1]["customdata"] = rail_id_list_of_lists
            patched_fig.data[1].y = df[gs.table_geq_col_log_2_norm] if log_x else df[gs.table_geq_col_norm_count]

        return patched_fig
    else:
        raise PreventUpdate


# @app.callback(
#     Output("id-geq-box-plot", "figure", allow_duplicate=True),
#     # Output("id-geq-histogram", "figure", allow_duplicate=True),
#     # Output("id-loading-graph-geq", "children"),
#
#     State("id-ag-grid-geq", "rowData"),
#     Input("id-ag-grid-geq", "virtualRowData"),
#     Input("id-switch-geq-lock-with-table", "value"),
#     Input("id-switch-geq-log-raw-box-plot", "value"),  # TODO: need to put this in client side callback as well
#     State("id-switch-geq-violin-raw-box-plot", "value"),
#     State("id-switch-geq-normalize", "value"),
#     prevent_initial_call=True,
# )
# def update_charts_geq(
#         row_data_from_table,
#         filtered_row_data_from_table,
#         lock_graph_data_with_table,
#         box_plot_log_x,
#         violin_overlay,
#         normalized_data,
# ):
#     """
#     Given the table data as input, it will update the relative graphs
#     """
#     raise PreventUpdate
#
#     if not row_data_from_table or not filtered_row_data_from_table:
#         raise PreventUpdate
#
#     if lock_graph_data_with_table:
#         data = filtered_row_data_from_table
#     else:
#         data = row_data_from_table
#
#     if normalized_data:
#         # Filter out the -1 factors directly
#         data = [row for row in data if row[gs.table_geq_col_factor] != -1]
#         df = pd.DataFrame(data)
#         # Make graphs
#         box_plot = graphs.get_box_plot_gene_expression(df, box_plot_log_x, violin_overlay, normalized_data)
#
#     else:
#         df = pd.DataFrame(data)
#         box_plot = graphs.get_box_plot_gene_expression(df, box_plot_log_x, violin_overlay, normalized_data)
#
#     return box_plot


@app.callback(
    Output("id-ag-grid-jiq", "exportDataAsCsv"),
    Output("id-ag-grid-jiq", "csvExportParams"),
    Input("id-button-jiq-download", "n_clicks"),
    State("id-jiq-download-options", "value"),
    prevent_initial_call=True,
    running=[(Output("id-button-jiq-download", "disabled"), True, False)],  # requires the latest Dash 2.16
)
def export_data_as_csv_jiq(n_clicks, option):
    return callback.export_data_as_csv(option, "psi_query_data")


@app.callback(
    Output("id-ag-grid-geq", "exportDataAsCsv"),
    Output("id-ag-grid-geq", "csvExportParams"),
    Input("id-button-geq-download", "n_clicks"),
    State("id-geq-download-options", "value"),
    prevent_initial_call=True,
    running=[(Output("id-button-geq-download", "disabled"), True, False)],  # requires the latest Dash 2.16
)
def export_data_as_csv_geq(n_clicks, option):
    return callback.export_data_as_csv(option, "gene_expression_query_data")


@app.callback(
    Output("id-ag-grid-jiq", "filterModel", allow_duplicate=True),
    Input("id-box-plot-jiq", "clickData"),
    State("id-ag-grid-jiq", "filterModel"),
    prevent_initial_call=True,
)
def on_box_plot_click_jiq(click_data, filter_model):
    return callback.on_box_plot_click(click_data, filter_model)


@app.callback(
    Output("id-ag-grid-geq", "filterModel", allow_duplicate=True),
    Input("id-geq-box-plot", "clickData"),
    State("id-ag-grid-geq", "filterModel"),
    prevent_initial_call=True,
)
def on_box_plot_click_geq(click_data, filter_model):
    return callback.on_box_plot_click(click_data, filter_model)


@app.callback(
    Output("id-ag-grid-jiq", "filterModel", allow_duplicate=True),
    Input("id-button-jiq-reset", "n_clicks"),
    prevent_initial_call=True,
)
def on_reset_table_jiq(click_data):
    return callback.on_reset_table(click_data)


@app.callback(
    Output("id-ag-grid-geq", "filterModel", allow_duplicate=True),
    Input("id-button-geq-reset", "n_clicks"),
    prevent_initial_call=True,
)
def on_reset_table_geq(click_data):
    return callback.on_reset_table(click_data)


@app.callback(
    Output("id-jiq-unlock", "style"),
    Output("id-jiq-lock", "style"),
    Input("id-switch-jiq-lock-with-table", "value"),
    prevent_initial_call=True,
)
def on_lock_switch_jiq(lock):
    return callback.on_lock_switch(lock)


@app.callback(
    Output("id-geq-unlock", "style"),
    Output("id-geq-lock", "style"),
    Input("id-switch-geq-lock-with-table", "value"),
    prevent_initial_call=True,
)
def on_lock_switch_geq(lock):
    return callback.on_lock_switch(lock)


# Run the app
if __name__ == "__main__":
    app.run()
