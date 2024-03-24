"""This file includes the graph components used in the queries."""
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from snaptron_query.app import global_strings as gs


def get_histogram_jiq(df):
    """Wrapper for plotly express histogram given a df - for clarity

    fig.update traces using below
    https://plotly.com/python/reference/histogram/
    https://plotly.com/python/histograms/
    """
    fig = px.histogram(df,
                       x=gs.table_jiq_col_psi,
                       nbins=50,
                       )
    fig.update_layout(title=f'<b>{gs.psi_histogram_title}</b>', title_x=0.5)
    fig.update_traces(marker_color='darkblue')
    return fig


def get_box_plot_jiq(df, log_psi_values, violin_overlay):
    """Wrapper for plotly express box plot given a df

    https://plotly.com/python/box-plots/
    https://plotly.com/python-api-reference/generated/plotly.express.box
    https://plotly.com/python/reference/box/
    """
    y_values = gs.table_jiq_col_psi
    range_y_axis = [0, 110]
    if log_psi_values:
        y_values = np.log2(df[y_values + 1])
        range_y_axis = None

    if violin_overlay:
        fig = px.violin(df, y=y_values, hover_data=[gs.snaptron_col_rail_id],
                        labels={gs.snaptron_col_rail_id: gs.plot_label_rail_id},
                        box=True,
                        points='all')  # show all points

        # if you want to add the mean set mean-line_visible=True
        fig.update_traces(jitter=0.1, pointpos=0,
                          line_color='royalblue', marker_color='darkblue')

    else:
        fig = px.box(df, y=y_values, hover_data=[gs.snaptron_col_rail_id],
                     labels={gs.snaptron_col_rail_id: gs.plot_label_rail_id,
                             gs.table_jiq_col_psi: gs.table_jiq_col_psi.upper()},
                     # Request to not snap with table changes.
                     # If provided, overrides auto-scaling on the y-axis in cartesian coordinates.
                     range_y=range_y_axis,
                     points='all')  # show all points

        fig.update_traces(jitter=0.1, pointpos=0, boxmean=True,
                          line_color='royalblue', marker_color='darkblue')

    # update the y-axis title if log switch is on
    if log_psi_values:
        fig.update_yaxes(title_text='Log₂(PSI)')

    fig.update_layout(title=f'<b>{gs.psi_box_plot_title}</b>', title_x=0.5)

    return fig


def get_histogram_geq(df):
    """Wrapper for plotly express histogram given a df - for clarity

    fig.update traces using below
    https://plotly.com/python/reference/histogram/
    https://plotly.com/python/histograms/
    """
    fig = px.histogram(df,
                       x='normalized_count',
                       nbins=50,
                       )
    fig.update_layout(title='Histogram Tittle', title_x=0.5)
    fig.update_traces(marker_color='darkblue')
    return fig


def get_box_plot_gene_expression(df, log_values, violin_overlay, normalized=False):
    """Wrapper for plotly express box plot given a df

    https://plotly.com/python/box-plots/
    https://plotly.com/python-api-reference/generated/plotly.express.box
    https://plotly.com/python/reference/box/
    """
    global y_normalized
    if normalized:
        y_raw = df[gs.table_geq_col_raw_count]
        y_normalized = df[gs.table_geq_col_norm_count]
        box_plot_title = gs.geq_plot_title_raw_vs_normalized_count
        if log_values:
            y_raw = np.log2(df[gs.table_geq_col_raw_count] + 1)
            y_normalized = np.log2(df[gs.table_geq_col_norm_count] + 1)
    else:
        y_raw = df[gs.table_geq_col_raw_count]
        box_plot_title = gs.geq_plot_title_raw_count_box_plot
        if log_values:
            y_raw = np.log2(df[gs.table_geq_col_raw_count] + 1)

    if normalized:
        # to get the hover templates in graphics pobject working use customdata
        # combination of hoverinfo='text', text=df['rail_id'], hovertemplate="Rail ID:%{text}<br>Raw Count: %{y}"
        # creates an extra box next to the original hover box with the trace title.
        # https://stackoverflow.com/questions/69278251/plotly-including-additional-data-in-hovertemplate
        custom_data = np.stack((df['rail_id'], df['factor']), axis=-1)
        if log_values:
            hover_template = 'Rail ID: %{customdata[0]}<br>Log(count+1): %{y} <br><extra></extra>'
        else:
            hover_template = 'Rail ID: %{customdata[0]}<br>Count: %{y} <br><extra></extra>'
            # 'factor:  %{customdata[1]}<br>' + #TODO: does PI want factor info as well

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
            trace_normalized_count = go.Violin(norm_plot_params_dict,box_visible=True)
        else:
            trace_raw_count = go.Box(raw_plot_params_dict)
            trace_normalized_count = go.Box(norm_plot_params_dict)

        fig = go.Figure(data=[trace_raw_count, trace_normalized_count])

    else:  # not normalized data then use plotly express
        hover_data = [gs.snaptron_col_rail_id]
        labels = {gs.snaptron_col_rail_id: gs.plot_label_rail_id,
                  gs. table_geq_col_raw_count: gs.geq_plot_label_raw_count}

        # Note:plotly express doesn't like the values sent in as a dictionary like the graphics object
        if violin_overlay:
            # to draw all points set point to all
            fig = px.violin(df, y=y_raw, hover_data=hover_data, labels=labels, box=True)
        else:
            # with plotly express, provide the df, so it can extract the labels and hover data
            fig = px.box(df, y=y_raw, hover_data=hover_data, labels=labels)

    # update the y-axis title if log switch is on
    if log_values:
        fig.update_yaxes(title_text='Log₂(Gene Expression Count+1)')
    else:
        fig.update_yaxes(title_text='Gene Expression Count')

    fig.update_traces(jitter=0, pointpos=0, line_color='royalblue', marker_color='darkblue')
    fig.update_layout(title=f'<b>{box_plot_title}</b>', title_x=0.5)

    # update the legend location for the normalized case so it doesn't take space in
    # between the box plots and the histogram
    if normalized:
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=1.02))

    return fig


def get_junction_query_column_def():
    """Wrapper for ag-grid column definitions and their individual style"""

    # TODO: different compilation are going to have different headers
    # this function needs to be dynamic
    return [
        {"field": 'rail_id', "headerName": "Rail ID", "filter": "agNumberColumnFilter", },
        {"field": 'external_id', "headerName": "External ID"},
        {"field": 'study', "headerName": "Study"},
        {"field": 'study_title', "headerName": "Study Title"},
        {"field": 'library_layout', "headerName": "Library"},
        {"field": 'sample_description', "headerName": "Desc"},
        {"field": 'sample_name', "headerName": "Name"},
        {"field": 'sample_title', "headerName": "Title"},
        {"field": 'inc', "headerName": "Inclusion Count", "filter": "agNumberColumnFilter", },
        {"field": 'exc', "headerName": "Exclusion Count", "filter": "agNumberColumnFilter", },
        {"field": 'total', "headerName": "Total Count", "filter": "agNumberColumnFilter", },
        {"field": 'psi', "headerName": "PSI", "filter": "agNumberColumnFilter", 'initialSort': 'desc'},
    ]


def get_gene_expression_query_column_def(normalized):
    """Wrapper for ag-grid column definitions and their individual style"""

    # TODO: different compilation are going to have different headers
    # this function needs to be dynamic
    column_def = [{"field": 'rail_id', "headerName": "Rail ID", "filter": "agNumberColumnFilter"},
                  {"field": 'external_id', "headerName": "External ID"},
                  {"field": 'raw_count', "headerName": "Raw Count", "filter": "agNumberColumnFilter"}]

    if normalized:
        norm_data = [{"field": 'factor', "headerName": "Factor", "filter": "agNumberColumnFilter"},
                     {"field": 'normalized_count', "headerName": "Normalized Count", "filter": "agNumberColumnFilter"}]
        column_def.extend(norm_data)

    # append the meta data
    meta_data = [{"field": 'study', "headerName": "Study"},
                 {"field": 'study_title', "headerName": "Study Title"},
                 {"field": 'library_layout', "headerName": "Library"},
                 {"field": 'sample_description', "headerName": "Desc"},
                 {"field": 'sample_name', "headerName": "Name"},
                 {"field": 'sample_title', "headerName": "Title"}]

    column_def.extend(meta_data)

    return column_def
