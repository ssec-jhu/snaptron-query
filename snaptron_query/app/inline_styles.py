"""
    This file provides inline custom styles for some of the dash components
"""

# --------------------
#       USE FOR DEBUGGING LAYOUT
# --------------------
# set the 0 to 1 to see the grids for alignment and layout changes
import dash_mantine_components as dmc
border_card = f'0px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}'
border_column = f'0px solid {dmc.theme.DEFAULT_COLORS['green'][4]}'

# set this value to 'block' to see the layout without running the query
display_style = 'block'  # none or block for debugging

boundary_style = {
    'display': display_style,
    'width': '100%',
    'border': border_card,
    'box-shadow': "1px 2px 7px 0px grey"  # 'shadow-sm' does not work here
}
# --------------------
# IMPORTANT!
# will need to do inline styling for tabs, not CSS
# see here: https://github.com/plotly/dash-core-components/issues/327
# specifically I had an issue with the width, the code would not follow CSS but exact code as inline did the job
tab_border_color = '3px solid var(--bs-success-border-subtle)'  # '3px solid #e36209' orange
tab_background_color = 'var(--bs-light-bg-subtle)'  # '#f9f9f9' , 'var(--bs-light-bg-subtle)'

horizontal_tab = {

    'padding': '10px 20px',
    'borderRadius': '5px 5px 0 0px',
    'cursor': 'pointer',
    'marginBottom': '50px',  # puts some spacing below the tabs
    'height': '70px',       # Fixed height
    "display": "flex",  # need this line or the other two below will not work
    "justify-content": "center",
    "align-items": "center",
    'backgroundColor': tab_background_color,
    'color': '#586069',  # text color
    'transition': 'background-color 0.3s, color 0.3s',
    'boxShadow': '1 2px 4px rgba(0, 0, 0, 0.1)',
}

horizontal_tab_selected = {
    'padding': '10px 20px',
    'borderRadius': '5px 5px 0 0px',  # these are the 4 corners of the tab_horizontal_bootstrap
    'cursor': 'pointer',
    'marginBottom': '50px',  # puts some spacing below the tabs
    'height': '70px',  # Fixed height
    "display": "flex",  # need this line or the other two below will not work
    "justify-content": "center",
    "align-items": "center",
    'borderTop': tab_border_color, # uncomment this to override the borderline
    'backgroundColor': 'white',  # Light navy
    'color': 'black',  # text color
    'transition': 'background-color 0.3s, color 0.3s, box-shadow 0.3s',
    'font-weight': "bold",
}
