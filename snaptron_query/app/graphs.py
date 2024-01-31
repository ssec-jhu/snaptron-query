"""
    This file includes the graph components used in the queries.
    Functions are wrappers around px chart components.
"""

import plotly.express as px
import global_strings


def get_histogram(df):
    """
        Wrapper for plotly express histogram given a df
        Wrapping in a function for clarity

        fig.update traces using below
        https://plotly.com/python/reference/histogram/
        https://plotly.com/python/histograms/
    """
    fig = px.histogram(df,
                       x=global_strings.table_jiq_col_psi,
                       nbins=50,
                       # title='Histogram of PSI',
                       # labels={'rail_id': 'Rail ID'},
                       # log_y=log_scale,  # represent bars with log scale
                       # color_discrete_sequence=['yellow']  # color of histogram bars
                       # color='darkblue',
                       # histnorm='percent' or probability density
                       )

    fig.update_layout(title=f'<b>{global_strings.histogram_title}</b>', title_x=0.5)
    fig.update_traces(marker_color='darkblue')
    return fig


def get_box_plot(df):
    """
        Wrapper for plotly express box plot given a df
        Wrapping in a function for clarity

        https://plotly.com/python/box-plots/
        https://plotly.com/python-api-reference/generated/plotly.express.box
        https://plotly.com/python/reference/box/
    """
    fig = px.box(df,
                 y=global_strings.table_jiq_col_psi,
                 hover_data=[global_strings.snaptron_col_rail_id],
                 # hover_name='Rail ID',
                 labels={global_strings.snaptron_col_rail_id: global_strings.boxplot_label},
                 # color='psi',
                 # Request to not snap with table changes.
                 # If provided, overrides auto-scaling on the y-axis in cartesian coordinates.
                 range_y=[0, 110],
                 # boxmode='overlay', # 'group' or 'overlay'
                 # points='all',  # 'outliers' (default), 'suspectedoutliers', 'all', or False
                 # title="Box plot of PSI",
                 )

    # fig.update_traces(quartilemethod="exclusive")  # or "inclusive", or "linear" by default
    # fig.update_traces(pointpos=-1.8)
    # fig.update_traces(boxpoints='all')#Type:( "all" | "outliers" (defualt) | "suspectedoutliers" | False )
    # fig.update_traces(jitter=0.3)# add some jitter for a better separation between points
    fig.update_traces(marker_color='darkblue', line_color='royalblue')
    fig.update_layout(title=f'<b>{global_strings.box_plot_title}</b>', title_x=0.5)
    # fig.update_layout(margin = dict(l=10, r=10, t=5, b=5),paper_bgcolor="LightSteelBlue")

    return fig


def get_junction_query_column_def():
    """
        Wrapper for ag-grid column definitions and their indivisual style
        Wrapping in a function for clarity
    """

    # TODO: add filter params reset to the psi column, confirm with PI
    column_defs = [
        {"field": 'rail_id', "headerName": "Rail ID", "filter": "agNumberColumnFilter", },
        {"field": 'external_id', "headerName": "External ID"},
        {"field": 'study', "headerName": "Study"},
        {"field": 'inc', "headerName": "Inclusion Count", "filter": "agNumberColumnFilter", },
        {"field": 'exc', "headerName": "Exclusion Count", "filter": "agNumberColumnFilter", },
        {"field": 'total', "headerName": "Total Count", "filter": "agNumberColumnFilter", },
        {"field": 'psi', "headerName": "PSI", "filter": "agNumberColumnFilter", 'initialSort': 'desc'},
    ]
    return column_defs
