from dash import html
from dash_iconify import DashIconify

md = 20
sm = 16
add_box = html.I(DashIconify(icon="mdi:add-box", height=sm, width=sm))  # "ic:round-add-box"
download = html.I(DashIconify(icon="mdi:tray-download", height=md, width=md))
reset = html.I(DashIconify(icon="mdi:filter-remove", height=md, width=md))
info = html.I(DashIconify(icon="fa6-solid:circle-info", height=sm, width=sm), style={'color': 'var(--bs-info)'})


def get_lock_open(icon_id):
    return html.I(DashIconify(icon="fa6-solid:lock-open", height=md, width=md),
                  id=icon_id, style={'color': 'var(--bs-gray-400)'})


def get_lock_closed(icon_id):
    return html.I(DashIconify(icon="fa6-solid:lock", height=md, width=md),
                  id=icon_id, style={'color': 'var(--bs-primary)'})
