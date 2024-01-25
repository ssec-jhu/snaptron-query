"""
    This file provides inline custom styles for some of the dash components
"""

# will need to do inline styling for tabs not CSS
# see here: https://github.com/plotly/dash-core-components/issues/327
# specifically I had an issue with the width, the CSS would not follow the code

borderColor = '3px solid var(--bs-info-border-subtle)'  # '3px solid #e36209' orange

tabBackgroundColor = 'var(--bs-secondary-bg)'  # '#f9f9f9'
# tabBackgroundColor = 'var(--bs-light-bg-subtle)'

# buttonColor = 'var(--bs-info-border-subtle)'   #'#f9f9f9'
buttonColor = tabBackgroundColor  # 'var(--bs-primary)'

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
    'padding': '10px 20px',
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
