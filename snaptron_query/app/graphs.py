"""This file includes the graph components used in the queries."""
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from snaptron_query.app import global_strings as gs, utils


def get_histogram_jiq_lists(x_values, log_values, log_psi_values, log_y):
    if log_psi_values:
        x_values = log_values

    fig = px.histogram(x=x_values, log_y=log_y, nbins=25)
    fig.update_layout(title=f'<b>{gs.jiq_plot_title_hist}</b>',
                      title_x=0.5,
                      template=gs.dbc_template_name)
    # fig.update_traces(marker_color='darkblue')

    # update the y-axis title if log switch is on
    if log_psi_values:
        fig.update_xaxes(title_text=gs.jiq_log_psi)
    else:
        fig.update_yaxes(title_text=gs.jiq_psi_plot_axes)

    return fig


def get_histogram_jiq(df, log_psi_values, log_y):
    """Wrapper for plotly express histogram given a df - for clarity

    fig.update traces using below
    https://plotly.com/python/reference/histogram/
    https://plotly.com/python/histograms/
    """
    x_values = gs.table_jiq_col_psi
    if log_psi_values:
        x_values = gs.table_jiq_col_log_2  # utils.log_2_function(df, x_values)

    fig = px.histogram(df, x=x_values, log_y=log_y, nbins=25)
    fig.update_layout(title=f'<b>{gs.jiq_plot_title_hist}</b>',
                      title_x=0.5,
                      template=gs.dbc_template_name)
    # fig.update_traces(marker_color='darkblue')

    # update the y-axis title if log switch is on
    if log_psi_values:
        fig.update_xaxes(title_text=gs.jiq_log_psi)
    else:
        fig.update_yaxes(title_text=gs.jiq_psi_plot_axes)

    return fig


def get_box_plot_jiq_lists(y_values, rail_id_list, log_values, log_psi_values, violin_overlay):
    """Wrapper for plotly express box plot given a df

    https://plotly.com/python/box-plots/
    https://plotly.com/python-api-reference/generated/plotly.express.box
    https://plotly.com/python/reference/box/
    """
    # y_values = gs.table_jiq_col_psi
    range_y_axis = [0, 110]
    if log_psi_values:
        y_values = log_values  # utils.log_2_function_lists(y_values)
        range_y_axis = None

    if violin_overlay:
        fig = px.violin(y=y_values,
                        # hover_data=rail_id_list,
                        # labels={gs.snpt_col_rail_id: gs.plot_label_rail_id},
                        box=True,
                        hover_data={gs.plot_label_rail_id: rail_id_list}
                        # points='all'
                        )  # show all points

        # if you want to add the mean set mean-line_visible=True
        fig.update_traces(jitter=0.01, pointpos=0,
                          # line_color='royalblue', marker_color='darkblue'
                          )

    else:
        fig = px.box(y=y_values, hover_data={gs.plot_label_rail_id: rail_id_list},
                     # labels={gs.table_jiq_col_psi: gs.table_jiq_col_psi.upper()},
                     # Request to not snap with table changes.
                     # If provided, overrides auto-scaling on the y-axis in cartesian coordinates.
                     range_y=range_y_axis,
                     # points='all'
                     )  # show all points

        fig.update_traces(jitter=0.01, pointpos=0, boxmean=True,
                          # line_color='royalblue', marker_color='darkblue'
                          )

    fig.update_layout(title=f'<b>{gs.jiq_plot_title_box}</b>',
                      title_x=0.5,
                      template=gs.dbc_template_name)

    # update the y-axis title if log switch is on
    if log_psi_values:
        fig.update_yaxes(title_text=gs.jiq_log_psi)
    else:
        fig.update_yaxes(title_text=gs.jiq_psi_plot_axes)

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
        y_values = gs.table_jiq_col_log_2  # utils.log_2_function(df, y_values)
        range_y_axis = None

    if violin_overlay:
        fig = px.violin(df, y=y_values, hover_data=[gs.snpt_col_rail_id],
                        labels={gs.snpt_col_rail_id: gs.plot_label_rail_id},
                        box=True,
                        # points='all'
                        )  # show all points

        # if you want to add the mean set mean-line_visible=True
        fig.update_traces(jitter=0.01, pointpos=0,
                          # line_color='royalblue', marker_color='darkblue'
                          )

    else:
        fig = px.box(df, y=y_values, hover_data=[gs.snpt_col_rail_id],
                     labels={gs.snpt_col_rail_id: gs.plot_label_rail_id,
                             gs.table_jiq_col_psi: gs.table_jiq_col_psi.upper()},
                     # Request to not snap with table changes.
                     # If provided, overrides auto-scaling on the y-axis in cartesian coordinates.
                     range_y=range_y_axis,
                     # points='all'
                     )  # show all points

        fig.update_traces(jitter=0.01, pointpos=0, boxmean=True,
                          # line_color='royalblue', marker_color='darkblue'
                          )

    fig.update_layout(title=f'<b>{gs.jiq_plot_title_box}</b>',
                      title_x=0.5,
                      template=gs.dbc_template_name)

    # update the y-axis title if log switch is on
    if log_psi_values:
        fig.update_yaxes(title_text=gs.jiq_log_psi)
    else:
        fig.update_yaxes(title_text=gs.jiq_psi_plot_axes)

    return fig


def get_histogram_geq_lists(x_values, log_count_values, log_y):
    """Wrapper for plotly express histogram given a df - for clarity

    fig.update traces using below
    https://plotly.com/python/reference/histogram/
    https://plotly.com/python/histograms/
    """
    # labels = {gs.snpt_col_rail_id: gs.plot_label_rail_id,
    #           gs.table_geq_col_norm_count: gs.geq_plot_label_norm_count}

    # x_values = gs.table_geq_col_norm_count

    if log_count_values:  # log2 the values
        x_values = utils.log_2_function_lists(x_values)

    fig = px.histogram(x=x_values, log_y=log_y, nbins=50)

    fig.update_layout(title=f'<b>{gs.geq_plot_title_hist}</b>',
                      title_x=0.5,
                      template=gs.dbc_template_name)
    # fig.update_traces(marker_color='darkblue')

    if log_count_values:
        fig.update_xaxes(title_text=gs.geq_log_count)
    else:
        fig.update_xaxes(title_text=gs.geq_plot_label_norm_count)

    return fig


def get_histogram_geq(df, log_count_values, log_y):
    """Wrapper for plotly express histogram given a df - for clarity

    fig.update traces using below
    https://plotly.com/python/reference/histogram/
    https://plotly.com/python/histograms/
    """
    labels = {gs.snpt_col_rail_id: gs.plot_label_rail_id,
              gs.table_geq_col_norm_count: gs.geq_plot_label_norm_count}

    x_values = gs.table_geq_col_norm_count

    if log_count_values:  # log2 the values
        x_values = utils.log_2_function(df, gs.table_geq_col_norm_count)

    fig = px.histogram(df, x=x_values, labels=labels, log_y=log_y, nbins=50)

    fig.update_layout(title=f'<b>{gs.geq_plot_title_hist}</b>',
                      title_x=0.5,
                      template=gs.dbc_template_name)
    # fig.update_traces(marker_color='darkblue')

    if log_count_values:
        fig.update_xaxes(title_text=gs.geq_log_count)
    else:
        fig.update_xaxes(title_text=gs.geq_plot_label_norm_count)

    return fig


def get_box_plot_gene_expression_lists(y_raw, y_normalized, rail_id_list, factor_list,
                                       log_values, violin_overlay, normalized=False):
    """Wrapper for plotly express box plot given a df

    https://plotly.com/python/box-plots/
    https://plotly.com/python-api-reference/generated/plotly.express.box
    https://plotly.com/python/reference/box/
    """
    if normalized:
        # y_raw = df[gs.table_geq_col_raw_count]
        # y_normalized = df[gs.table_geq_col_norm_count]
        box_plot_title = gs.geq_plot_title_box_norm
        if log_values:
            y_raw = utils.log_2_function_lists(y_raw)
            y_normalized = utils.log_2_function_lists(y_normalized)
    else:
        # y_raw = df[gs.table_geq_col_raw_count]
        box_plot_title = gs.geq_plot_title_box_raw
        if log_values:
            y_raw = utils.log_2_function_lists(y_raw)

    if normalized:
        # to get the hover templates in graphics pobject working use customdata
        # combination of hoverinfo='text', text=df['rail_id'], hovertemplate="Rail ID:%{text}<br>Raw Count: %{y}"
        # creates an extra box next to the original hover box with the trace title.
        # https://stackoverflow.com/questions/69278251/plotly-including-additional-data-in-hovertemplate
        custom_data = np.stack((rail_id_list, factor_list), axis=-1)
        if log_values:
            hover_template = 'Rail ID: %{customdata[0]}<br>Log(count+1): %{y} <br><extra></extra>'
        else:
            hover_template = 'Rail ID: %{customdata[0]}<br>Count: %{y} <br><extra></extra>'

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
        hover_data = rail_id_list
        labels = {gs.snpt_col_rail_id: gs.plot_label_rail_id,
                  gs.table_geq_col_raw_count: gs.geq_plot_label_raw_count}

        # Note:plotly express doesn't like the values sent in as a dictionary like the graphics object
        if violin_overlay:
            # to draw all points set point to all
            fig = px.violin(y=y_raw, hover_data=hover_data, labels=labels, box=True)
        else:
            # with plotly express, provide the df, so it can extract the labels and hover data
            fig = px.box(y=y_raw, hover_data=hover_data, labels=labels)

    # update the y-axis title if log switch is on
    if log_values:
        fig.update_yaxes(title_text=gs.geq_box_plot_y_axes_log)
    else:
        fig.update_yaxes(title_text=gs.geq_box_plot_y_axes)

    # fig.update_traces(jitter=0, pointpos=0, line_color='royalblue', marker_color='darkblue')
    fig.update_traces(jitter=0.01, pointpos=0)
    fig.update_layout(title=f'<b>{box_plot_title}</b>',
                      title_x=0.5,
                      template=gs.dbc_template_name,
                      # graphics object have different margins than plotly express
                      # so this box plot needs to bring the margin down a bit
                      margin=dict(t=55))

    # update the legend location for the normalized case, so it doesn't take space in
    # between the box plots and the histogram
    if normalized:
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=0.98))

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
            y_raw = utils.log_2_function(df, gs.table_geq_col_raw_count)
            y_normalized = utils.log_2_function(df, gs.table_geq_col_norm_count)
    else:
        y_raw = df[gs.table_geq_col_raw_count]
        box_plot_title = gs.geq_plot_title_box_raw
        if log_values:
            y_raw = utils.log_2_function(df, gs.table_geq_col_raw_count)

    if normalized:
        # to get the hover templates in graphics pobject working use customdata
        # combination of hoverinfo='text', text=df['rail_id'], hovertemplate="Rail ID:%{text}<br>Raw Count: %{y}"
        # creates an extra box next to the original hover box with the trace title.
        # https://stackoverflow.com/questions/69278251/plotly-including-additional-data-in-hovertemplate
        custom_data = np.stack((df[gs.snpt_col_rail_id], df[gs.table_geq_col_factor]), axis=-1)
        if log_values:
            hover_template = 'Rail ID: %{customdata[0]}<br>Log(count+1): %{y} <br><extra></extra>'
        else:
            hover_template = 'Rail ID: %{customdata[0]}<br>Count: %{y} <br><extra></extra>'

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
        labels = {gs.snpt_col_rail_id: gs.plot_label_rail_id,
                  gs.table_geq_col_raw_count: gs.geq_plot_label_raw_count}

        # Note:plotly express doesn't like the values sent in as a dictionary like the graphics object
        if violin_overlay:
            # to draw all points set point to all
            fig = px.violin(df, y=y_raw, hover_data=hover_data, labels=labels, box=True)
        else:
            # with plotly express, provide the df, so it can extract the labels and hover data
            fig = px.box(df, y=y_raw, hover_data=hover_data, labels=labels)

    # update the y-axis title if log switch is on
    if log_values:
        fig.update_yaxes(title_text=gs.geq_box_plot_y_axes_log)
    else:
        fig.update_yaxes(title_text=gs.geq_box_plot_y_axes)

    # fig.update_traces(jitter=0, pointpos=0, line_color='royalblue', marker_color='darkblue')
    fig.update_traces(jitter=0.01, pointpos=0)
    fig.update_layout(title=f'<b>{box_plot_title}</b>',
                      title_x=0.5,
                      template=gs.dbc_template_name,
                      # graphics object have different margins than plotly express
                      # so this box plot needs to bring the margin down a bit
                      margin=dict(t=55))

    # update the legend location for the normalized case, so it doesn't take space in
    # between the box plots and the histogram
    if normalized:
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=0.98))

    return fig


def get_col_meta_a():
    return [
        {"field": gs.snpt_col_rail_id, "headerName": "Rail ID", 'width': 100, "pinned": "left",
         "filterParams": {"buttons": ["reset"]}},
        {"field": gs.snpt_col_external_id, "headerName": "External ID", 'width': 125,
         "filterParams": {"buttons": ["reset"]}},
        {"field": 'study', "headerName": "Study", 'width': 120, "cellRenderer": "StudyLink",
         "filterParams": {"buttons": ["reset"]}},
    ]


def get_col_meta_b():
    return [
        {"field": 'study_title', "headerName": "Study Title", 'width': 350, "filterParams": {"buttons": ["reset"]},
         'autoHeight': True,  # must have this here, it is not a style option
         'cellClass': 'cell-wrap-dash-ag-grid'
         },
        {"field": 'sample_name', "headerName": "Sample Name", 'width': 150 + 20, "filterParams": {"buttons": ["reset"]},
         "tooltipField": 'sample_name'},
        {"field": 'sample_title', "headerName": "Sample Title", 'width': 150, "filterParams": {"buttons": ["reset"]},
         "tooltipField": 'sample_title'},
        {"field": 'library_layout', "headerName": "Library", 'width': 100, "filterParams": {"buttons": ["reset"]}},
        {"field": 'sample_description', "headerName": "Sample Description", 'width': 200,
         "filterParams": {"buttons": ["reset"]},
         "tooltipField": "sample_description"},
    ]


def get_col_jiq():
    return [
        {"field": gs.table_jiq_col_inc, "headerName": "Inc", "filter": "agNumberColumnFilter", 'width': 100,
         "filterParams": {"buttons": ["reset"]}, },
        {"field": gs.table_jiq_col_exc, "headerName": "Exc", "filter": "agNumberColumnFilter", 'width': 100,
         "filterParams": {"buttons": ["reset"]}, },
        {"field": gs.table_jiq_col_total, "headerName": "Total", "filter": "agNumberColumnFilter", 'width': 120,
         "filterParams": {"buttons": ["reset"]},
         # Performance Note: adding header tooltips creates a horizontal scroll performance issue!
         # "headerTooltip": "Inclusion Count + Exclusion Count"
         },
        {"field": gs.table_jiq_col_psi, "headerName": "PSI", "filter": "agNumberColumnFilter", 'initialSort': 'desc',
         'width': 120, "filterParams": {"buttons": ["reset"]}},
        {"field": gs.table_jiq_col_log_2, "headerName": gs.jiq_log_psi, "filter": "agNumberColumnFilter",
         'width': 120, "filterParams": {"buttons": ["reset"]}}
    ]


def get_junction_query_column_def():
    """Wrapper for ag-grid column definitions and their individual style"""

    # TODO: different compilation are going to have different headers
    return get_col_meta_a() + get_col_jiq() + get_col_meta_b()


def get_gene_expression_query_column_def(normalized=False):
    """Wrapper for ag-grid column definitions and their individual style"""

    column_def = get_col_meta_a()
    if normalized:
        column_def += [
            {"field": gs.table_geq_col_raw_count, "headerName": "Raw Count", "filter": "agNumberColumnFilter",
             'width': 130, "filterParams": {"buttons": ["reset"]}, },
            {"field": gs.table_geq_col_factor, "headerName": "Factor", "filter": "agNumberColumnFilter",
             'width': 130, "filterParams": {"buttons": ["reset"]}, },
            {"field": gs.table_geq_col_norm_count, "headerName": "Normalized Count", "filter": "agNumberColumnFilter",
             'width': 170, "filterParams": {"buttons": ["reset"]}, 'initialSort': 'desc'}
        ]
    else:
        column_def += [
            {"field": gs.table_geq_col_raw_count, "headerName": "Raw Count", "filter": "agNumberColumnFilter",
             'width': 130, "filterParams": {"buttons": ["reset"]},
             'initialSort': 'desc'}
        ]

    column_def += get_col_meta_b()

    return column_def
