import pandas as pd

from snaptron_query.app import column_defs as cd, utils
from snaptron_query.app import (
    graphs,
    exceptions,
    global_strings as gs,
    snaptron_client as sc,
)
from snaptron_query.app.query_junction_inclusion import JunctionInclusionQueryManager, JiqReturnType


def run_query(
    meta_data_dict,
    compilation,
    children,
    junction_count,
    box_log_psi,
    violin_overlay,
    histogram_log_psi,
    histogram_log_y,
):
    # count is indexed at 0
    inc_junctions, exc_junctions = utils.get_element_id_and_value(children, junction_count)
    if len(inc_junctions) == 0 or len(exc_junctions) == 0:
        raise exceptions.MissingUserInputs

    # verify all the coordinates, if there is any error in the intervals, an exception will be thrown
    junction_lists = []
    for j in range(len(exc_junctions)):
        junction_coordinates = sc.jiq_verify_coordinate_pairs(exc_junctions[j], inc_junctions[j])
        junction_lists.append(junction_coordinates)

    # gather the snaptron results form the exclusion junctions
    df_snpt_results_dict = sc.gather_snpt_query_results_into_dict(
        compilation=compilation, junction_lists=junction_lists
    )
    # Select the metadata that must be used
    # meta_data_dict = get_meta_data(compilation)

    # results returned are list of dictionaries which makes ag-grid load much faster,
    # One can convert a dataframe to dict with orient set to records for the ag-grid as well.
    row_data = JunctionInclusionQueryManager().run_junction_inclusion_query(
        meta_data_dict=meta_data_dict,
        df_snpt_results_dict=df_snpt_results_dict,
        junctions_list=junction_lists,
        return_type=JiqReturnType.LIST,
    )

    # Set the columnDefs for the ag-grid
    column_defs = cd.get_junction_query_column_def(compilation, len(junction_lists))

    # set the preset column filters requested
    filter_model = cd.get_jiq_table_filter_model(len(junction_lists))

    # Gather figure related items
    # TODO: these numbers must be combined with the filter model function
    df = pd.DataFrame(row_data)
    if len(junction_lists) == 1:
        df = df[(df[gs.table_jiq_col_psi] >= 5) & (df[gs.table_jiq_col_total] >= 15)]
    else:
        df = df[df[gs.table_jiq_col_avg_psi] >= 5]

    # count how many psi columns we have
    list_of_calculated_junctions = [col for col in df.columns if col.startswith(gs.table_jiq_col_psi)]
    histogram = graphs.get_histogram_jiq(df, histogram_log_psi, histogram_log_y, list_of_calculated_junctions)
    box_plot = graphs.get_box_plot_jiq(df, box_log_psi, violin_overlay, list_of_calculated_junctions)

    col_width = {"size": 6}
    # when the component is hidden, then becomes visible, the original style is lost,
    # so I am putting it back again.
    display_style = {
        "box-shadow": "1px 2px 7px 0px grey",
        "border-radius": "10px",
    }

    return row_data, column_defs, filter_model, histogram, box_plot, col_width, col_width, display_style
