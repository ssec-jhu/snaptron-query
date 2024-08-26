"""This file includes the graph components used in the queries."""

import plotly.express as px

from snaptron_query.app import global_strings as gs, graphs_utils


# ----------------------------------
#       BOX PLOT
# ----------------------------------


def fig_common_update_box_plot(fig, plot_title, y_axes_title):
    fig.update_layout(
        title=f"<b>{plot_title}</b>",
        title_x=0.5,
        # template=gs.dbc_template_name, # TODO: use template or colorblind colors
        margin=dict(b=0),
    )
    # line_color='royalblue', marker_color='darkblue'
    fig.update_traces(jitter=0.01, pointpos=0)
    fig.update_yaxes(title_text=y_axes_title)
    return fig


def create_box_plot(violin_overlay, df, y_values, range_y_axis, labels, mode=None, color=None):
    if df.empty:
        hover_data = None
        y_values = None
    else:
        hover_data = [gs.snpt_col_rail_id]

    if violin_overlay:
        # to draw all points set point to all
        fig = px.violin(
            df,
            y=y_values,
            hover_data=hover_data,
            labels=labels,
            color=color,
            violinmode=mode,
            # points="all",
            color_discrete_sequence=graphs_utils.get_common_colors(),
            box=True,
        )
    else:
        fig = px.box(
            df,
            y=y_values,
            hover_data=hover_data,
            labels=labels,
            color=color,
            boxmode=mode,
            # points="all",
            color_discrete_sequence=graphs_utils.get_common_colors(),
            # Request to not snap with table changes for JIQ.
            # If provided, overrides auto-scaling on the y-axis in cartesian coordinates.
            range_y=range_y_axis,
        )

        fig.update_traces(boxmean=True)

    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=0.98))

    return fig


def get_box_plot_jiq(df, log_psi_values, violin_overlay, list_of_calculated_junctions):
    """Wrapper for plotly express box plot given a df

    https://plotly.com/python/box-plots/
    https://plotly.com/python-api-reference/generated/plotly.express.box
    https://plotly.com/python/reference/box/
    """
    # set up the titles and the values for the box plot
    y_values = gs.table_jiq_col_log_2 if log_psi_values else gs.table_jiq_col_psi
    color = None
    mode = None
    if len(list_of_calculated_junctions) > 1:
        df = graphs_utils.convert_data_to_long_format_jiq(df, log_psi_values, list_of_calculated_junctions)
        y_values = "value"
        color = "variable"
        mode = "group"

    fig = create_box_plot(
        violin_overlay=violin_overlay,
        df=df,
        y_values=y_values,
        range_y_axis=None if log_psi_values else [0, 110],
        labels=graphs_utils.get_common_labels_jiq(),
        color=color,
        mode=mode,  # TODO: mode="overlay"?
    )

    # apply the common attributes for all box plots
    fig_common_update_box_plot(
        fig=fig,
        plot_title=gs.jiq_plot_title_box,
        y_axes_title=gs.jiq_log_psi if log_psi_values else gs.jiq_psi_plot_axes,
    )

    return fig


def get_box_plot_gene_expression(df, log_values, violin_overlay, normalized=False):
    """Wrapper for plotly express box plot given a df

    https://plotly.com/python/box-plots/
    https://plotly.com/python-api-reference/generated/plotly.express.box
    https://plotly.com/python/reference/box/
    """
    if normalized:
        # use df melt to convert to long format
        df = graphs_utils.convert_data_to_long_format_geq(df, log_values)
        y = "value"
        color = "variable"
        mode = "group"
    else:
        y = df[gs.table_geq_col_log_2_raw] if log_values else df[gs.table_geq_col_raw_count]
        color = None
        mode = None

    fig = create_box_plot(
        violin_overlay=violin_overlay,
        df=df,
        y_values=y,
        range_y_axis=None,
        labels=graphs_utils.get_common_labels_geq(),
        color=color,
        mode=mode,
    )

    fig_common_update_box_plot(
        fig=fig,
        plot_title=gs.geq_plot_title_box_norm if normalized else gs.geq_plot_title_box_raw,
        y_axes_title=gs.geq_box_plot_y_axes_log if log_values else gs.geq_box_plot_y_axes,
    )

    return fig


# ----------------------------------
#           HISTOGRAM
# ----------------------------------


def fig_common_update_histogram(fig, title, x_axes_title):
    fig.update_layout(
        title=f"<b>{title}</b>",
        title_x=0.5,
        # template=gs.dbc_template_name, # TODO: use template or colorblind colors
        margin=dict(b=0),
    )

    fig.update_xaxes(title_text=x_axes_title)
    # fig.update_traces(marker_color='darkblue')

    return fig


def create_histogram(df, x_values, log_y, labels, bins, plot_title, x_axes_title, color=None):
    if df.empty:
        x_values = None

    fig = px.histogram(
        df,
        x=x_values,
        log_y=log_y,
        labels=labels,
        nbins=bins,
        color=color,
        color_discrete_sequence=graphs_utils.get_common_colors(),
    )

    fig_common_update_histogram(fig, plot_title, x_axes_title)
    return fig


def get_histogram_jiq(df, log_psi_values, log_y, list_of_calculated_junctions):
    """Wrapper for plotly express histogram given a df - for clarity

    fig.update traces using below
    https://plotly.com/python/reference/histogram/
    https://plotly.com/python/histograms/
    """
    x = gs.table_jiq_col_log_2 if log_psi_values else gs.table_jiq_col_psi
    color = None
    if len(list_of_calculated_junctions) > 1:
        # melt the data frame
        df = graphs_utils.convert_data_to_long_format_jiq(df, log_psi_values, list_of_calculated_junctions)
        x = "value"
        color = "variable"

    fig = create_histogram(
        df=df,
        x_values=x,
        log_y=log_y,
        labels=graphs_utils.get_common_labels_jiq(),
        bins=25,
        plot_title=gs.jiq_plot_title_hist,
        x_axes_title=gs.jiq_log_psi if log_psi_values else gs.jiq_psi_plot_axes,
        color=color,
    )

    if len(list_of_calculated_junctions) != 1:
        fig.update_layout(barmode="overlay")
        fig.update_traces(opacity=0.5)  # can't see the blending of some colors with higher opacity
    return fig


def get_histogram_geq(df, log_count_values, log_y):
    """Wrapper for plotly express histogram given a df - for clarity

    fig.update traces using below
    https://plotly.com/python/reference/histogram/
    https://plotly.com/python/histograms/
    """
    return create_histogram(
        df=df,
        x_values=gs.table_geq_col_log_2_norm if log_count_values else gs.table_geq_col_norm_count,
        log_y=log_y,
        labels=graphs_utils.get_common_labels_geq(),
        bins=50,
        plot_title=gs.geq_plot_title_hist,
        x_axes_title=gs.geq_log_count if log_count_values else gs.geq_plot_label_norm_count,
    )
