from datetime import datetime

import pandas as pd
from dash import no_update, dcc

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


def export_data_as_csv(option, data, file_name):
    df = pd.DataFrame(data)

    exported_rows = "filteredAndSorted" if option == components.DownloadType.FILTERED.value else "all"
    # timestamp the file
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    # post process the columns to have an underscore in lieu of the spaces
    file = f"{file_name}_{exported_rows}_{timestamp}.csv"

    # send the download to dash
    return dcc.send_data_frame(df.to_csv, file)
