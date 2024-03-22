"""This file includes the graph components used in the queries."""
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from snaptron_query.app import global_strings as gs
import pandas as pd


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
        y_values = np.log2(df[y_values+1])
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
    y_values = gs.table_geq_col_raw_count
    labels = {gs.snaptron_col_rail_id: gs.plot_label_rail_id,
              gs.table_geq_col_raw_count: gs.plot_label_raw_count}
    hover_data = {gs.snaptron_col_rail_id: gs.plot_label_rail_id}
    box_plot_title = gs.raw_count_box_plot_title

    if normalized:
        box_plot_title = gs.raw_vs_normalized_count_box_plot_title

    if log_values:
        y_values = np.log2(df[y_values]+1)

    # pick the box plot mode
    if violin_overlay:
        fig = px.violin(df, y=y_values, hover_data=hover_data, labels=labels, box=True, points='all')
        # if you want to add the mean set mean-line_visible=True
    else:
        if normalized:
            raw_count = go.Box(y=df['raw_count'],
                               name='Raw Count',
                               hoverinfo='text',
                               text=df['rail_id'],
                               hovertemplate="Rail ID:%{text}<br>Raw Count: %{y}")
            if log_values:
                y_norm = np.log2(df['normalized_count']+1)
            else:
                y_norm = df['normalized_count']

            normalized_count = go.Box(y=y_norm, name='Normalized Count',
                                      hoverinfo='text',
                                      text=df['rail_id'],
                                      hovertemplate="Rail ID:%{text}<br>Normalized Count: %{y}")
            fig = go.Figure(data=[raw_count, normalized_count])

        else:
            fig = px.box(df, y=y_values, hover_data=hover_data, labels=labels)

    # update the y-axis title if log switch is on
    if log_values:
        fig.update_yaxes(title_text='Log₂(Gene Expression Count+1)')
    else:
        fig.update_yaxes(title_text='Gene Expression Count')

    if normalized:
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", xanchor="center",x=0.5, y=1.02))

    fig.update_traces(jitter=0.1, pointpos=0, line_color='royalblue', marker_color='darkblue')
    fig.update_layout(title=f'<b>{box_plot_title}</b>',title_x=0.5)

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
