"""This file includes the graph components used in the queries."""
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from snaptron_query.app import global_strings as gs


def get_common_labels_jiq():
    return {gs.snpt_col_rail_id: gs.plot_label_rail_id,
            gs.table_jiq_col_psi: gs.table_jiq_col_psi.upper(),
            gs.table_jiq_col_log_2: gs.jiq_log_psi}


def get_common_labels_geq():
    return {gs.snpt_col_rail_id: gs.plot_label_rail_id,
            gs.table_geq_col_raw_count: gs.geq_plot_label_raw_count,
            gs.table_geq_col_norm_count: gs.geq_plot_label_norm_count,
            gs.table_geq_col_log_2_raw: gs.geq_log_count,
            gs.table_geq_col_log_2_norm: gs.geq_log_count}


def fig_common_update_box_plot_plot(fig, title, y_axes_title_text):
    fig.update_layout(title=f'<b>{title}</b>',
                      title_x=0.5,
                      template=gs.dbc_template_name,
                      margin=dict(b=0),
                      # points='all'
                      )
    # line_color='royalblue', marker_color='darkblue'
    fig.update_traces(jitter=0.01, pointpos=0)
    fig.update_yaxes(title_text=y_axes_title_text)
    return fig


def get_box_plot_jiq(df, log_psi_values, violin_overlay):
    """Wrapper for plotly express box plot given a df

    https://plotly.com/python/box-plots/
    https://plotly.com/python-api-reference/generated/plotly.express.box
    https://plotly.com/python/reference/box/
    """
    y_values = gs.table_jiq_col_psi
    range_y_axis = [0, 110]
    y_axes_title_text = gs.jiq_psi_plot_axes
    if log_psi_values:
        y_values = gs.table_jiq_col_log_2  # utils.log_2_function(df, y_values)
        range_y_axis = None
        y_axes_title_text = gs.jiq_log_psi

    if violin_overlay:
        fig = px.violin(df, y=y_values, hover_data=[gs.snpt_col_rail_id], labels=get_common_labels_jiq(),
                        box=True,
                        # points='all'
                        )  # show all points
    else:
        fig = px.box(df, y=y_values, hover_data=[gs.snpt_col_rail_id], labels=get_common_labels_jiq(),
                     # Request to not snap with table changes.
                     # If provided, overrides auto-scaling on the y-axis in cartesian coordinates.
                     range_y=range_y_axis,
                     # points='all'
                     )  # show all points
        fig.update_traces(boxmean=True)

    # apply the common attributes
    fig_common_update_box_plot_plot(fig, gs.jiq_plot_title_box, y_axes_title_text)

    return fig


def get_box_plot_gene_expression(df, log_values, violin_overlay, normalized=False):
    """Wrapper for plotly express box plot given a df

    https://plotly.com/python/box-plots/
    https://plotly.com/python-api-reference/generated/plotly.express.box
    https://plotly.com/python/reference/box/
    """
    if normalized:
        y_raw = df[gs.table_geq_col_raw_count]
        y_normalized = df[gs.table_geq_col_norm_count]
        box_plot_title = gs.geq_plot_title_box_norm
        if log_values:
            y_raw = df[gs.table_geq_col_log_2_raw]
            y_normalized = df[gs.table_geq_col_log_2_norm]
    else:
        y_raw = df[gs.table_geq_col_raw_count]
        box_plot_title = gs.geq_plot_title_box_raw
        if log_values:
            y_raw = df[gs.table_geq_col_log_2_raw]

    if log_values:
        y_axes_title_text = gs.geq_box_plot_y_axes_log
    else:
        y_axes_title_text = gs.geq_box_plot_y_axes

    if normalized:
        # to get the hover templates in graphics pobject working use customdata
        # combination of hoverinfo='text', text=df['rail_id'], hovertemplate="Rail ID:%{text}<br>Raw Count: %{y}"
        # creates an extra box next to the original hover box with the trace title.
        # https://stackoverflow.com/questions/69278251/plotly-including-additional-data-in-hovertemplate
        custom_data = np.stack((df[gs.snpt_col_rail_id], df[gs.table_geq_col_factor]), axis=-1)
        hover_template_pre = f'{gs.plot_label_rail_id}:' + ' %{customdata[0]}<br>'
        if log_values:
            hover_template = hover_template_pre + gs.geq_log_count + ': %{y} <br><extra></extra>'
        else:
            hover_template = hover_template_pre + 'Count: %{y} <br><extra></extra>'

        raw_plot_params_dict = {'y': y_raw,
                                'name': gs.geq_plot_label_raw_count,
                                'hovertemplate': hover_template,
                                'customdata': custom_data}
        norm_plot_params_dict = {'y': y_normalized,
                                 'name': gs.geq_plot_label_norm_count,
                                 'hovertemplate': hover_template,
                                 'customdata': custom_data}
        if violin_overlay:
            trace_raw_count = go.Violin(raw_plot_params_dict, box_visible=True)
            trace_normalized_count = go.Violin(norm_plot_params_dict, box_visible=True)
        else:
            trace_raw_count = go.Box(raw_plot_params_dict)
            trace_normalized_count = go.Box(norm_plot_params_dict)

        fig = go.Figure(data=[trace_raw_count, trace_normalized_count])

    else:  # not normalized data then use plotly express
        hover_data = [gs.snpt_col_rail_id]

        # Note:plotly express doesn't like the values sent in as a dictionary like the graphics object
        if violin_overlay:
            # to draw all points set point to all
            fig = px.violin(df, y=y_raw, hover_data=hover_data, labels=get_common_labels_geq(), box=True)
        else:
            # with plotly express, provide the df, so it can extract the labels and hover data
            fig = px.box(df, y=y_raw, hover_data=hover_data, labels=get_common_labels_geq())

    # update the y-axis title if log switch is on

    fig_common_update_box_plot_plot(fig, box_plot_title, y_axes_title_text)
    fig.update_layout(margin=dict(t=55))

    # update the legend location for the normalized case, so it doesn't take space in
    # between the box plots and the histogram
    if normalized:
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=0.98))

    return fig


def fig_common_update_histogram(fig, title, y_title_text):
    fig.update_layout(title=f'<b>{title}</b>',
                      title_x=0.5,
                      template=gs.dbc_template_name,
                      margin=dict(b=0))

    fig.update_xaxes(title_text=y_title_text)
    # fig.update_traces(marker_color='darkblue')

    return fig


def get_histogram_jiq(df, log_psi_values, log_y):
    """Wrapper for plotly express histogram given a df - for clarity

    fig.update traces using below
    https://plotly.com/python/reference/histogram/
    https://plotly.com/python/histograms/
    """
    x_values = gs.table_jiq_col_psi
    y_title_text = gs.jiq_psi_plot_axes
    if log_psi_values:
        x_values = gs.table_jiq_col_log_2  # utils.log_2_function(df, x_values)
        y_title_text = gs.jiq_log_psi

    fig = px.histogram(df, x=x_values, log_y=log_y, labels=get_common_labels_jiq(), nbins=25)

    fig_common_update_histogram(fig, gs.jiq_plot_title_hist, y_title_text)

    return fig


def get_histogram_geq(df, log_count_values, log_y):
    """Wrapper for plotly express histogram given a df - for clarity

    fig.update traces using below
    https://plotly.com/python/reference/histogram/
    https://plotly.com/python/histograms/
    """
    x_values = gs.table_geq_col_norm_count
    y_title_text = gs.geq_plot_label_norm_count
    if log_count_values:  # log2 the values
        x_values = gs.table_geq_col_log_2_norm
        y_title_text = gs.geq_log_count

    fig = px.histogram(df, x=x_values, log_y=log_y, labels=get_common_labels_geq(), nbins=50)

    fig_common_update_histogram(fig, gs.geq_plot_title_hist, y_title_text)

    return fig
