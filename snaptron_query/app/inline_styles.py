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
border_grids = f'0px solid {dmc.theme.DEFAULT_COLORS['orange'][4]}'
style_debugging = {
    'border': border_grids,
    # "textAlign": "center",
}
# --------------------


# IMPORTANT!
# will need to do inline styling for tabs, not CSS
# see here: https://github.com/plotly/dash-core-components/issues/327
# specifically I had an issue with the width, the code would not follow CSS but exact code as inline did the job

borderColor = '3px solid var(--bs-success-border-subtle)'  # '3px solid #e36209' orange
tabBackgroundColor = 'var(--bs-light-bg-subtle)'  # '#f9f9f9' , 'var(--bs-light-bg-subtle)'
buttonColor = 'var(--bs-secondary)'  # ,var(--bs-info-border-subtle), '#f9f9f9'

# set this value to 'block' to see the layout without running the query
display_style = 'block'  # none or block for debugging
boundary_style = {
    'display': display_style,
    'width': '100%',
    'border': border_card,
    # 'background-color': '#d8e7ff',
    # 'background-color':'var(--bs-gray-200)',
    # "border-radius": "10px",
    # "background-color": "#CDCDCD",
    'box-shadow': "1px 2px 7px 0px grey"  # 'shadow-sm' does not work here
}

tab_style_vertical = {
    'padding': '10px 20px',
    'borderRadius': '5px 0 0 5px',
    'cursor': 'pointer',
    'marginRight': '1px',
    'width': '130px',  # Fixed width
    'height': '200px',  # Fixed height
    # need all three lines below to bring the content to center vertically
    "display": "flex",  # need this line or the other two below will not work
    "justify-content": "center",
    "align-items": "center",

    # ----------------
    # different
    # ----------------
    # https://community.plotly.com/t/access-background-color-from-dash-bootstrap-templates-inside-dash-callback/63458/5
    # this is a variable in the bootstrap(bs) themes. you can find it in the dev tools on the browser
    'backgroundColor': tabBackgroundColor,
    'color': '#586069',  # text color
    'transition': 'background-color 0.3s, color 0.3s',
    'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
}

tab_selected_style_vertical = {
    # 'padding': '10px 20px',
    'borderRadius': '5px 0 0 5px',  # these are the 4 corners of the tab_horizontal_bootstrap
    'cursor': 'pointer',
    'marginRight': '1px',
    'width': '130px',  # Fixed width
    'height': '200px',  # Fixed height
    # need all three lines below to bring the content to center vertically
    "display": "flex",  # need this line or the other two below will not work
    "justify-content": "center",
    "align-items": "center",

    # ----------------
    # different
    # ----------------
    'backgroundColor': 'white',  # Light navy
    'color': 'black',  # text color
    # # shadow: X and Y offsets relative to the element, blur and spread radius, and color.
    # 'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
    'transition': 'background-color 0.3s, color 0.3s, box-shadow 0.3s',
    'font-weight': "bold",
    # # uncomment this to override the border line
    # 'borderLeft': '3px solid #e36209',
    'borderLeft': borderColor,
}

horizontal_tab = {

    'padding': '10px 20px',
    'borderRadius': '5px 5px 0 0px',
    'cursor': 'pointer',
    'marginBottom': '50px',  # puts some spacing below the tabs
    'height': '70px',  # Fixed height
    # need all three lines below to bring the content to center vertically
    "display": "flex",  # need this line or the other two below will not work
    "justify-content": "center",
    "align-items": "center",

    # ----------------
    # different
    # ----------------
    'backgroundColor': tabBackgroundColor,
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

    # need all three lines below to bring the content to center vertically
    "display": "flex",  # need this line or the other two below will not work
    "justify-content": "center",
    "align-items": "center",

    # uncomment this to override the borderline
    'borderTop': borderColor,

    # ----------------
    # different
    # ----------------
    'backgroundColor': 'white',  # Light navy
    'color': 'black',  # text color
    # shadow: X and Y offsets relative to the element, blur and spread radius, and color.
    # 'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
    'transition': 'background-color 0.3s, color 0.3s, box-shadow 0.3s',
    'font-weight': "bold",
}
