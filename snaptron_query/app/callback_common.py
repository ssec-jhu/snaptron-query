from dash import no_update

from snaptron_query.app import global_strings as gs, inline_styles as st


def on_box_plot_click(click_data, filter_model):
    if not click_data:
        return no_update

    rail_id = click_data["points"][0]["customdata"][0]
    filter_model[gs.snpt_col_rail_id] = {'filterType': 'number', 'type': 'equals', 'filter': rail_id}
    return filter_model


def on_reset_table(click_data):
    if not click_data:
        return no_update

    filter_model = dict()
    return filter_model


def on_lock_switch(lock):
    if lock:
        return st.inactive_lock, st.active_lock
    else:
        return st.active_lock, st.inactive_lock


def export_data_as_csv(n_clicks, option, file_name):
    if option == 2:
        exported_rows = 'filteredAndSorted'
    else:
        exported_rows = 'all'

    # https://ag-grid.com/javascript-data-grid/csv-export/#reference-CsvExportParams-exportedRows
    return True, {"fileName": f'{file_name}_{exported_rows}.csv', "exportedRows": exported_rows}
