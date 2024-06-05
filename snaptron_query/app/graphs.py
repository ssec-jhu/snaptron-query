"""This file includes the graph components used in the queries."""

import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from snaptron_query.app import global_strings as gs


def get_common_labels_jiq():
    return {
        gs.snpt_col_rail_id: gs.plot_label_rail_id,
        gs.table_jiq_col_psi: gs.table_jiq_col_psi.upper(),
        gs.table_jiq_col_log_2: gs.jiq_log_psi,
    }


def get_common_labels_geq():
    return {
        gs.snpt_col_rail_id: gs.plot_label_rail_id,
        gs.table_geq_col_raw_count: gs.geq_plot_label_raw_count,
        gs.table_geq_col_norm_count: gs.geq_plot_label_norm_count,
        gs.table_geq_col_log_2_raw: gs.geq_log_count,
        gs.table_geq_col_log_2_norm: gs.geq_log_count,
    }


def fig_common_update_box_plot(fig, title, y_axes_title_text):
    fig.update_layout(
        title=f"<b>{title}</b>",
        title_x=0.5,
        template=gs.dbc_template_name,
        margin=dict(b=0),
        # points='all'
    )
    # line_color='royalblue', marker_color='darkblue'
    fig.update_traces(jitter=0.01, pointpos=0)
    fig.update_yaxes(title_text=y_axes_title_text)
    return fig


def create_box_plot(violin_overlay, df, y_values, range_y_axis, labels):
    hover_data = [gs.snpt_col_rail_id]
    if violin_overlay:
        # to draw all points set point to all
        fig = px.violin(
            df,
            y=y_values,
            hover_data=hover_data,
            labels=labels,
            box=True,
            # points='all'
        )
    else:
        fig = px.box(
            df,
            y=y_values,
            hover_data=hover_data,
            labels=labels,
            # Request to not snap with table changes for JIQ.
            # If provided, overrides auto-scaling on the y-axis in cartesian coordinates.
            range_y=range_y_axis,
            # points='all'
        )  # show all points
        fig.update_traces(boxmean=True)

    return fig


def get_box_plot_jiq(df, log_psi_values, violin_overlay):
    """Wrapper for plotly express box plot given a df

    https://plotly.com/python/box-plots/
    https://plotly.com/python-api-reference/generated/plotly.express.box
    https://plotly.com/python/reference/box/
    """
    # set up the titles and the values for the box plot
    y_values = gs.table_jiq_col_log_2 if log_psi_values else gs.table_jiq_col_psi
    range_y_axis = None if log_psi_values else [0, 110]
    y_axes_title_text = gs.jiq_log_psi if log_psi_values else gs.jiq_psi_plot_axes

    # now create the box plot with these values
    fig = create_box_plot(violin_overlay, df, y_values, range_y_axis, get_common_labels_jiq())

    # apply the common attributes for all box plots
    fig_common_update_box_plot(fig, gs.jiq_plot_title_box, y_axes_title_text)

    return fig


def create_box_plot_gene_expression_normalized(df, log_values, violin_overlay, y_raw, y_normalized):
    # to get the hover templates in graphics pobject working use customdata
    # combination of hoverinfo='text', text=df['rail_id'], hovertemplate="Rail ID:%{text}<br>Raw Count: %{y}"
    # creates an extra box next to the original hover box with the trace title.
    # https://stackoverflow.com/questions/69278251/plotly-including-additional-data-in-hovertemplate
    custom_data = np.stack((df[gs.snpt_col_rail_id], df[gs.table_geq_col_factor]), axis=-1)
    hover_template_pre = f"{gs.plot_label_rail_id}:" + " %{customdata[0]}<br>"
    if log_values:
        hover_template = hover_template_pre + gs.geq_log_count + ": %{y} <br><extra></extra>"
    else:
        hover_template = hover_template_pre + "Count: %{y} <br><extra></extra>"

    raw_plot_params_dict = {
        "y": y_raw,
        "name": gs.geq_plot_label_raw_count,
        "hovertemplate": hover_template,
        "customdata": custom_data,
    }
    norm_plot_params_dict = {
        "y": y_normalized,
        "name": gs.geq_plot_label_norm_count,
        "hovertemplate": hover_template,
        "customdata": custom_data,
    }
    if violin_overlay:
        trace_raw_count = go.Violin(raw_plot_params_dict, box_visible=True)
        trace_normalized_count = go.Violin(norm_plot_params_dict, box_visible=True)
    else:
        trace_raw_count = go.Box(raw_plot_params_dict)
        trace_normalized_count = go.Box(norm_plot_params_dict)

    fig = go.Figure(data=[trace_raw_count, trace_normalized_count])

    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=0.98))

    return fig


def get_box_plot_gene_expression(df, log_values, violin_overlay, normalized=False):
    """Wrapper for plotly express box plot given a df

    https://plotly.com/python/box-plots/
    https://plotly.com/python-api-reference/generated/plotly.express.box
    https://plotly.com/python/reference/box/
    """
    # set up the data being used for the box plot
    y_raw = df[gs.table_geq_col_log_2_raw] if log_values else df[gs.table_geq_col_raw_count]
    box_plot_title = gs.geq_plot_title_box_norm if normalized else gs.geq_plot_title_box_raw
    y_axes_title_text = gs.geq_box_plot_y_axes_log if log_values else gs.geq_box_plot_y_axes

    # now create the graphs, normalized will use the graphics object due to its complexity
    if normalized:
        y_normalized = df[gs.table_geq_col_log_2_norm] if log_values else df[gs.table_geq_col_norm_count]
        fig = create_box_plot_gene_expression_normalized(df, log_values, violin_overlay, y_raw, y_normalized)
    else:
        # not normalized data then use plotly express
        fig = create_box_plot(
            violin_overlay,
            df,
            y_raw,
            range_y_axis=None,  # gene expression has no boundaries
            labels=get_common_labels_geq(),
        )

    fig_common_update_box_plot(fig, box_plot_title, y_axes_title_text)
    fig.update_layout(margin=dict(t=55))

    return fig


def fig_common_update_histogram(fig, title, y_title_text):
    fig.update_layout(title=f"<b>{title}</b>", title_x=0.5, template=gs.dbc_template_name, margin=dict(b=0))

    fig.update_xaxes(title_text=y_title_text)
    # fig.update_traces(marker_color='darkblue')

    return fig


def create_histogram(df, x_values, log_y, labels, bins, plot_title, y_title):
    fig = px.histogram(df, x=x_values, log_y=log_y, labels=labels, nbins=bins)
    fig_common_update_histogram(fig, plot_title, y_title)
    return fig


def get_histogram_jiq(df, log_psi_values, log_y):
    """Wrapper for plotly express histogram given a df - for clarity

    fig.update traces using below
    https://plotly.com/python/reference/histogram/
    https://plotly.com/python/histograms/
    """
    x_values = gs.table_jiq_col_log_2 if log_psi_values else gs.table_jiq_col_psi
    y_title_text = gs.jiq_log_psi if log_psi_values else gs.jiq_psi_plot_axes

    return create_histogram(df, x_values, log_y, get_common_labels_jiq(), 25, gs.jiq_plot_title_hist, y_title_text)


def get_histogram_geq(df, log_count_values, log_y):
    """Wrapper for plotly express histogram given a df - for clarity

    fig.update traces using below
    https://plotly.com/python/reference/histogram/
    https://plotly.com/python/histograms/
    """
    x_values = gs.table_geq_col_log_2_norm if log_count_values else gs.table_geq_col_norm_count
    y_title_text = gs.geq_log_count if log_count_values else gs.geq_plot_label_norm_count

    return create_histogram(df, x_values, log_y, get_common_labels_geq(), 50, gs.geq_plot_title_hist, y_title_text)
