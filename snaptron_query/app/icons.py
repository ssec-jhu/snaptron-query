from dash import html
from dash_iconify import DashIconify

add_box = html.I(DashIconify(icon="ic:round-add-box"))
download = html.I(className="fa-solid fa-download")
lock_open = html.I(id='id-jiq-unlock', className="fa-solid fa-lock-open", style={'color': 'var(--bs-gray-400)'})
lock_closed = html.I(id='id-jiq-lock', className="fa-solid fa-lock", style={'color': 'var(--bs-primary)'})
point_up = html.I(className="fa-regular fa-hand-point-up")
point_down = html.I(className="fa-regular fa-hand-point-down")
info = html.I(className="fa-solid fa-circle-info")
