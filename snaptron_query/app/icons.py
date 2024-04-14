from dash import html
from dash_iconify import DashIconify

w = 22
add_box = html.I(DashIconify(icon="ic:round-add-box", height=18, width=18))
# download = html.I(className="fa-solid fa-download")
# reset = html.I(className="fa-solid fa-filter-circle-xmark")
# lock_open = html.I(id='id-jiq-unlock', className="fa-solid fa-lock-open", style={'color': 'var(--bs-gray-400)'})
# lock_closed = html.I(id='id-jiq-lock', className="fa-solid fa-lock", style={'color': 'var(--bs-primary)'})
# info = html.I(className="fa-solid fa-circle-info")
download = html.I(DashIconify(icon="flowbite:download-outline", height=w, width=w))
reset = html.I(DashIconify(icon="mdi:filter-remove", height=w, width=w))
lock_open = html.I(DashIconify(icon="fa6-solid:lock-open", height=w, width=w), id='id-jiq-unlock',
                   style={'color': 'var(--bs-gray-400)'})
lock_closed = html.I(DashIconify(icon="fa6-solid:lock", height=w, width=w), id='id-jiq-lock',
                     style={'color': 'var(--bs-primary)'})
info = html.I(DashIconify(icon="bi:info-circle-fill", height=16, width=16), style={'color': 'var(--bs-info)'})
