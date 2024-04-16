"""This file provides inline custom styles for some of the dash components"""

# --------------------
#       USE FOR DEBUGGING LAYOUT
# --------------------
# set the 0 to 1 to see the grids for alignment and layout changes
import dash_mantine_components as dmc

border_column = {'border': f'0px solid {dmc.theme.DEFAULT_COLORS["green"][4]}'}
boundary_style = {'box-shadow': "1px 2px 7px 0px grey"}  # 'shadow-sm' does not work here
inactive_lock = {'color': 'var(--bs-gray-400)'}
active_lock = {'color': 'var(--bs-primary)'}
section = {"box-shadow": "1px 2px 7px 0px grey", "border-radius": "10px"}
# Note: Setting the 'display': 'None' creates a delay in the rendering of the plots. They
# render to the screen then shift to their position.
# visibility will keep the space, so when the plots come in, they render fast
section_vis = {'visibility': 'hidden', "height": "70px"}