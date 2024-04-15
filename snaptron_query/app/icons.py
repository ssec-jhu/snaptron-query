from dash import html
from dash_iconify import DashIconify

md = 20
sm = 16
add_box = html.I(DashIconify(icon="mdi:add-box", height=sm, width=sm))
# add_box = html.I(DashIconify(icon="ic:round-add-box", height=18, width=18))

# download = html.I(className="fa-solid fa-download")
# reset = html.I(className="fa-solid fa-filter-circle-xmark")
# lock_open = html.I(id='id-jiq-unlock', className="fa-solid fa-lock-open", style={'color': 'var(--bs-gray-400)'})
# lock_closed = html.I(id='id-jiq-lock', className="fa-solid fa-lock", style={'color': 'var(--bs-primary)'})
# info = html.I(className="fa-solid fa-circle-info",style={'color': 'var(--bs-secondary)'})

download = html.I(DashIconify(icon="mdi:tray-download", height=md, width=md))
reset = html.I(DashIconify(icon="mdi:filter-remove", height=md, width=md))
lock_open = html.I(DashIconify(icon="fa6-solid:lock-open", height=md, width=md), id='id-jiq-unlock',
                   style={'color': 'var(--bs-gray-400)'})
lock_closed = html.I(DashIconify(icon="fa6-solid:lock", height=md, width=md), id='id-jiq-lock',
                     style={'color': 'var(--bs-primary)'})
info = html.I(DashIconify(icon="fa6-solid:circle-info", height=sm, width=sm),
              style={'color': 'var(--bs-info)'}  # TODO: show PI color and decide to keep or remove from final layout
              )
