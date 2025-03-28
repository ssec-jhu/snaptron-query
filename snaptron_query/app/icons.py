from dash import html
from dash_iconify import DashIconify

MEDIUM = 20
SMALL = 16
add_box = html.I(DashIconify(icon="mdi:add-box", height=SMALL, width=SMALL))  # "ic:round-add-box"
del_box = html.I(DashIconify(icon="mdi:minus-box", height=SMALL, width=SMALL))
download = html.I(DashIconify(icon="mdi:tray-download", height=MEDIUM, width=MEDIUM))
reset = html.I(DashIconify(icon="mdi:filter-remove", height=MEDIUM, width=MEDIUM))
info = html.I(DashIconify(icon="fa6-solid:circle-info", height=SMALL, width=SMALL), style={"color": "var(--bs-info)"})
caution = html.I(
    DashIconify(icon="fa6-solid:triangle-exclamation", height=SMALL, width=SMALL), style={"color": "var(--bs-warning)"}
)


def get_lock_opened(icon_id):
    return html.I(
        DashIconify(icon="fa6-solid:lock-open", height=MEDIUM, width=MEDIUM),
        id=icon_id,
        style={"color": "var(--bs-gray-400)"},
    )


def get_lock_closed(icon_id):
    return html.I(
        DashIconify(icon="fa6-solid:lock", height=MEDIUM, width=MEDIUM),
        id=icon_id,
        style={"color": "var(--bs-primary)"},
    )
