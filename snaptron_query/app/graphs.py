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


def get_box_plot(df):
    """Wrapper for plotly express box plot given a df

    https://plotly.com/python/box-plots/
    https://plotly.com/python-api-reference/generated/plotly.express.box
    https://plotly.com/python/reference/box/
    """
    fig = px.box(df,
                 y=global_strings.table_jiq_col_psi,
                 hover_data=[global_strings.snaptron_col_rail_id],
                 labels={global_strings.snaptron_col_rail_id: global_strings.boxplot_label},
                 # Request to not snap with table changes.
                 # If provided, overrides auto-scaling on the y-axis in cartesian coordinates.
                 range_y=[0, 110]
                 )

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
