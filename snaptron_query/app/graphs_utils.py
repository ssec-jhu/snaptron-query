import pandas as pd

from snaptron_query.app import global_strings as gs


def get_common_colors():
    # colorblind colors: https://davidmathlogic.com/colorblind/  -> select "tol"
    return [
        "#332288",  # blue/purple
        "#882255",  # red/pink
        "#117733",  # green
        "#88CCEE",  # light blue
        "#DDCC77",  # yellow,
    ]


def get_common_labels_jiq():
    mapping = {
        gs.snpt_col_rail_id: gs.plot_label_rail_id,
        gs.table_jiq_col_psi: gs.table_jiq_col_psi.upper(),
        gs.table_jiq_col_log_2: gs.jiq_log_psi,
    }
    mapping.update({f"psi_{i}": f"PSI_{i}" for i in range(1, 6)})
    mapping.update({f"log2_{i}": f"Log_{i}" for i in range(1, 6)})
    return mapping


def get_common_labels_geq():
    # The keys of this dict should correspond to column names, and the values should correspond to the desired label.
    return {
        gs.snpt_col_rail_id: gs.plot_label_rail_id,
        gs.table_geq_col_raw_count: gs.geq_plot_label_raw_count,
        gs.table_geq_col_norm_count: gs.geq_plot_label_norm_count,
        gs.table_geq_col_log_2_raw: gs.geq_plot_label_raw_count,  # TODO: use log or not, it will affect hover data
        gs.table_geq_col_log_2_norm: gs.geq_plot_label_norm_count,  # don't put the word "Log"
    }


def convert_data_to_long_format_jiq(df, log_psi_values, list_of_calculated_junctions):
    # we use df melt to overlay all the data into one histogram.
    # use the log column or the psi columns pending switch value
    df_melt_values = (
        [col for col in df.columns if col.startswith(gs.table_jiq_col_log_2)]
        if log_psi_values
        else list_of_calculated_junctions
    )
    df_melt = pd.melt(df, id_vars=[gs.snpt_col_rail_id], value_vars=df_melt_values)

    # this easy mapping fixes hover data and trace names all-in-one instead of fixing
    # each one manually after the figure is created because the traces follow the df variables
    df_melt["variable"] = df_melt["variable"].map(get_common_labels_jiq())

    return df_melt


def convert_data_to_long_format_geq(df, log_values):
    # we use df melt to overlay all the data into one histogram.
    df_melt_values = (
        [gs.table_geq_col_log_2_raw, gs.table_geq_col_log_2_norm]
        if log_values
        else [gs.table_geq_col_raw_count, gs.table_geq_col_norm_count]
    )
    df_melt = pd.melt(df, id_vars=[gs.snpt_col_rail_id], value_vars=df_melt_values)

    # this easy mapping fixes hover data and trace names all-in-one instead of fixing
    # each one manually after the figure is created because the traces follow the df variables
    df_melt["variable"] = df_melt["variable"].map(get_common_labels_geq())

    return df_melt
