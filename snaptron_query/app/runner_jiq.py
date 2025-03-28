import pandas as pd

from snaptron_query.app import column_defs as cd, utils
from snaptron_query.app import (
    graphs,
    exceptions,
    global_strings as gs,
    snaptron_client as sc,
    inline_styles as styles,
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
        compilation=compilation,
        return_type=JiqReturnType.LIST,
    )

    # Set the columnDefs for the ag-grid
    column_defs = cd.get_junction_query_column_def(compilation, len(junction_lists))

    # set the preset column filters requested
    filter_model = cd.get_jiq_table_filter_model(len(junction_lists))

    # Gather figure related items
    # make sure you also update get_jiq_table_filter_model with changes here
    df = pd.DataFrame(row_data)
    if len(junction_lists) == 1:
        df = df[
            (df[gs.table_jiq_col_psi] >= gs.const_filter_psi) & (df[gs.table_jiq_col_total] >= gs.const_filter_total)
        ]
    else:
        # we need to filter all total_i for all the junctions
        df = df[df[gs.table_jiq_col_avg_psi] >= gs.const_filter_psi]
        for i in range(1, len(junction_lists) + 1):
            total_col = f"{gs.table_jiq_col_total}_{i}"
            df = df[(df[total_col] >= gs.const_filter_total)]

    # count how many psi columns we have
    list_of_calculated_junctions = [col for col in df.columns if col.startswith(gs.table_jiq_col_psi)]
    histogram = graphs.get_histogram_jiq(df, histogram_log_psi, histogram_log_y, list_of_calculated_junctions)
    box_plot = graphs.get_box_plot_jiq(df, box_log_psi, violin_overlay, list_of_calculated_junctions)

    # Create split graph
    box_plot_split_display = styles.display_none
    if len(inc_junctions) == 1:
        if compilation in {gs.compilation_gtexv2, gs.compilation_tcgav2}:
            split_column = "SMTS" if compilation == gs.compilation_gtexv2 else "gdc_cases.project.primary_site"
            unique_categories = df[split_column].nunique()
            box_plot_split = graphs.get_box_plot_jiq(
                df,
                box_log_psi,
                violin_overlay,
                list_of_calculated_junctions,
                split=split_column,
                n_col_graph=unique_categories,
            )
            box_plot_split_display = styles.display_block
        else:
            box_plot_split = None
    else:
        box_plot_split = None

    col_width = {"size": 6}
    # when the component is hidden, then becomes visible, the original style is lost,
    # so I am putting it back again.
    display_style = {
        "box-shadow": "1px 2px 7px 0px grey",
        "border-radius": "10px",
    }

    return (
        row_data,
        column_defs,
        filter_model,
        histogram,
        box_plot,
        box_plot_split,
        box_plot_split_display,
        col_width,
        col_width,
        display_style,
    )
