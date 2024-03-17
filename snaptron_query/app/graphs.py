"""This file includes the graph components used in the queries."""

import plotly.express as px
from snaptron_query.app import global_strings


def get_histogram(df):
    """Wrapper for plotly express histogram given a df - for clarity

    fig.update traces using below
    https://plotly.com/python/reference/histogram/
    https://plotly.com/python/histograms/
    """
    fig = px.histogram(df,
                       x=global_strings.table_jiq_col_psi,
                       nbins=50,
                       )
    fig.update_layout(title=f'<b>{global_strings.histogram_title}</b>', title_x=0.5)
    fig.update_traces(marker_color='darkblue')
    return fig


def get_box_plot(df, log_psi_values, violin_overlay):
    """Wrapper for plotly express box plot given a df

    https://plotly.com/python/box-plots/
    https://plotly.com/python-api-reference/generated/plotly.express.box
    https://plotly.com/python/reference/box/
    """
    import numpy as np
    y_values = global_strings.table_jiq_col_psi
    if log_psi_values:
        y_values = np.log2(df[y_values])

    if violin_overlay:
        fig = px.violin(df, y=y_values, hover_data=[global_strings.snaptron_col_rail_id],
                        labels={global_strings.snaptron_col_rail_id: global_strings.boxplot_label},
                        box=True,
                        points='all')  # show all points

        # if you want to add the mean set meanline_visible=True
        fig.update_traces(jitter=0.1, pointpos=0,
                          line_color='royalblue', marker_color='darkblue')

    else:
        fig = px.box(df, y=y_values, hover_data=[global_strings.snaptron_col_rail_id],
                     labels={global_strings.snaptron_col_rail_id: global_strings.boxplot_label,
                             global_strings.table_jiq_col_psi:global_strings.table_jiq_col_psi.upper()},
                     # Request to not snap with table changes.
                     # If provided, overrides auto-scaling on the y-axis in cartesian coordinates.
                     range_y=[0, 110],
                     points='all')  # show all points

        fig.update_traces(jitter=0.1, pointpos=0, boxmean=True,
                          line_color='royalblue', marker_color='darkblue')


    # update the y axis title if log switch is on
    if log_psi_values:
        fig.update_yaxes(title_text='Log₂(PSI)')

    fig.update_layout(title=f'<b>{global_strings.box_plot_title}</b>', title_x=0.5)

    return fig


def get_box_plot_gene_expression(df, log_values, violin_overlay):
    """Wrapper for plotly express box plot given a df

    https://plotly.com/python/box-plots/
    https://plotly.com/python-api-reference/generated/plotly.express.box
    https://plotly.com/python/reference/box/
    """
    import numpy as np
    y_values = global_strings.table_geq_col_raw_count
    if log_values:
        y_values = np.log2(df[y_values])

    if violin_overlay:
        fig = px.violin(df, y=y_values, hover_data=[global_strings.snaptron_col_rail_id],
                        labels={global_strings.snaptron_col_rail_id: global_strings.boxplot_label},
                        box=True,
                        points='all')  # show all points

        # if you want to add the mean set mean-line_visible=True
        fig.update_traces(jitter=0.2, pointpos=0,
                          line_color='royalblue', marker_color='darkblue')

    else:
        fig = px.box(df, y=y_values, hover_data=[global_strings.snaptron_col_rail_id],
                     labels={global_strings.snaptron_col_rail_id: global_strings.boxplot_label,
                             global_strings.table_jiq_col_psi: global_strings.table_jiq_col_psi.upper()},
                     # Request to not snap with table changes.
                     # If provided, overrides auto-scaling on the y-axis in cartesian coordinates.
                     # range_y=[0, 110],
                     points='all')  # show all points

        fig.update_traces(jitter=0.2, pointpos=0, boxmean=True,
                          line_color='royalblue', marker_color='darkblue')

    # update the y-axis title if log switch is on
    if log_values:
        fig.update_yaxes(title_text='Log₂(PSI)')

    fig.update_layout(title=f'<b>{global_strings.box_plot_title}</b>', title_x=0.5)

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


def get_gene_expression_query_column_def():
    """Wrapper for ag-grid column definitions and their individual style"""

    # TODO: different compilation are going to have different headers
    # this function needs to be dynamic
    return [
        {"field": 'rail_id', "headerName": "Rail ID", "filter": "agNumberColumnFilter"},
        {"field": 'count', "headerName": "Raw Count", "filter": "agNumberColumnFilter", },
        {"field": 'external_id', "headerName": "External ID"},
        {"field": 'study', "headerName": "Study"},
        {"field": 'study_title', "headerName": "Study Title"},
        {"field": 'library_layout', "headerName": "Library"},
        {"field": 'sample_description', "headerName": "Desc"},
        {"field": 'sample_name', "headerName": "Name"},
        {"field": 'sample_title', "headerName": "Title"},

    ]
