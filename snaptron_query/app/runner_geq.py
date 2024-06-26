import pandas as pd
from dash import no_update

from snaptron_query.app import column_defs as cd
from snaptron_query.app import (
    graphs,
    exceptions,
    global_strings as gs,
    snaptron_client as sc,
)
from snaptron_query.app.query_gene_expression import GeneExpressionQueryManager


def run_query(
    meta_data_dict,
    normalize_data,
    use_coordinates,
    norm_gene_coordinates,
    query_gene_coordinates,
    compilation,
    norm_gene_id,
    query_gene_id,
    histogram_log_x,
    histogram_log_y,
    box_plot_log_x,
    violin_overlay,
):
    """
    :param normalize_data: whether the gene data should be normalized or not
    :param use_coordinates: if coordinates are to be provided
    :param norm_gene_coordinates:  the normalization gene coordinates
    :param query_gene_coordinates: the query gene coordinates
    :param compilation: selected compilation from UI
    :param norm_gene_id: normalization gene ID
    :param query_gene_id: query gene ID
    :param histogram_log_x: log the counts base 2
    :param histogram_log_y: log the Y axis
    :param box_plot_log_x: log the counts bas 2
    :param violin_overlay: show plot in violin mode
    :return:
    """
    # Verify the gene coordinates string, we don't need the return values for this query
    df_snpt_results_query = sc.get_snpt_query_results_df(
        compilation=compilation,
        region=sc.coordinates_to_formatted_string(sc.geq_verify_coordinate(query_gene_coordinates))
        if use_coordinates
        else query_gene_id,
        query_mode="genes",
    )
    if df_snpt_results_query.empty:
        raise exceptions.EmptyResponse

    # Set upt the GEX manager then run the Query
    # Create normalization table if needed
    geq = GeneExpressionQueryManager()
    if normalize_data:
        if use_coordinates:
            sc.geq_verify_coordinate(norm_gene_coordinates)
            df_snpt_results_norm = sc.get_snpt_query_results_df(
                compilation=compilation, region=norm_gene_coordinates, query_mode="genes"
            )
        else:
            df_snpt_results_norm = sc.get_snpt_query_results_df(
                compilation=compilation, region=norm_gene_id, query_mode="genes"
            )
        if df_snpt_results_norm.empty:
            raise exceptions.EmptyResponse

        geq.setup_normalization_data_method(norm_gene_id, df_snpt_results_norm, meta_data_dict)

    row_data = geq.run_gene_expression_query(query_gene_id, df_snpt_results_query, meta_data_dict)

    # ag-grid accepts list of dicts so passing in the data from storage that is saved as list of dict
    # saves times here. store_data = row_data.df.to_dict("records") Set the columnDefs for the ag-grid
    column_defs = cd.get_gene_expression_query_column_def(compilation, normalize_data)

    filter_model = cd.get_geq_table_filter_model(normalize_data)
    if normalize_data:
        # Filter out the -1 factors directly
        data = [row for row in row_data if row[gs.table_geq_col_factor] != -1]
        df = pd.DataFrame(data)
        # df = df[df[gs.table_geq_col_factor] >= 0]

        # Make histogram
        histogram = graphs.get_histogram_geq(df, histogram_log_x, histogram_log_y)
        box_plot = graphs.get_box_plot_gene_expression(df, box_plot_log_x, violin_overlay, normalize_data)

        width_box = width_hist = {"size": 6}
        hist_display = {"display": "Block"}
    else:
        df = pd.DataFrame(row_data)
        histogram = None
        box_plot = graphs.get_box_plot_gene_expression(df, box_plot_log_x, violin_overlay, normalize_data)
        width_box = {"size": 8, "offset": 2}
        width_hist = no_update
        hist_display = {"display": "None"}

    return row_data, column_defs, filter_model, box_plot, histogram, width_box, width_hist, hist_display


if __name__ == "__main__":
    from snaptron_query.app import utils

    dict_srav3h = utils.read_srav3h("/Users/Fatemeh/Desktop/meta_data_2/srav3h_samples.tsv")

    run_query(
        meta_data_dict=dict_srav3h,
        normalize_data=True,
        use_coordinates=None,
        norm_gene_coordinates=None,
        query_gene_coordinates=None,
        compilation="SRAv3h",
        norm_gene_id="EDF1",
        query_gene_id="TARDBP",
        histogram_log_x=True,
        histogram_log_y=False,
        box_plot_log_x=True,
        violin_overlay=False,
    )
