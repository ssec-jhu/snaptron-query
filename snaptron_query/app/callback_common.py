from datetime import datetime
from dash import no_update

from snaptron_query.app import global_strings as gs, inline_styles as st, components


def on_box_plot_click(click_data, filter_model):
    if not click_data:
        return no_update

    filter_model[gs.snpt_col_rail_id] = {
        "filterType": "number",
        "type": "equals",
        "filter": click_data["points"][0]["customdata"][0],
    }
    return filter_model


def on_reset_table(click_data):
    if not click_data:
        return no_update

    return {}


def on_lock_switch(lock):
    if lock:
        return st.inactive_lock, st.active_lock
    else:
        return st.active_lock, st.inactive_lock


def export_data_as_csv(option, file_name):
    if option == components.DownloadType.FILTERED.value:
        exported_rows = "filteredAndSorted"
    else:
        exported_rows = "all"

    # timestamp the file
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    # https://ag-grid.com/javascript-data-grid/csv-export/#reference-CsvExportParams-exportedRows
    return True, {"fileName": f"{file_name}_{exported_rows}_{timestamp}.csv", "exportedRows": exported_rows}
