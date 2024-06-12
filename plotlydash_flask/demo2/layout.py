# --------------------------------------------
# This Is the Combined Layout Common for both
# - Search 
# - Analytic pages
#------------------------------------------------


import dash
from dash import dcc, html
import dash_bootstrap_components as dbc 
#------------------------------
# Styling the Clicked Button
#------------------------------

# layout = html.Div([
#                 dcc.Location(id='url', refresh=True),
#                 html.Div(id='page-content'),
#                 dash.page_container
                
#                 ])

layout = html.Div([
            
            dbc.Navbar(
                dbc.Container(
                    [
                        html.A(  # HTML A link enclosing logo
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Img(
                                            src="assets/piesis_logo.jpg",
                                            alt='Logo',
                                            height = "120rem",
                                            className="rounded-circle"  # Add rounded image
                                        ),
                                        width=4,  # Adjust column width for logo
                                        # className="d-flex justify-content-end"  # Align logo to the right
                                    ),
                                    dbc.Col(
                                        dbc.NavbarBrand(
                                            html.H6(
                                                "Taxtualize - Video Search Engine",
                                                className='mt-5',  # margin-top
                                                style={'color': 'white','paddingLeft': '1rem'}
                                            )
                                        ),
                                        width=6  # Adjust column width for brand name
                                    )
                                ],
                                align="center",  # Vertical center
                            ),
                            className="navbar-brand"  # Add navbar-brand class
                        ),
                        dbc.Row(
                            [
                                dbc.NavItem(
                                    [
                                        dbc.NavLink(
                                            "Analytics",
                                            href="/demo2/analytics",
                                            external_link=True,
                                            style={'paddingRight': '3rem', 'display': 'inline', 'color': 'white'}
                                        ),
                                        dbc.NavLink(
                                            "Home",
                                            href="/demo2/",
                                            external_link=True,
                                            style={'paddingRight': '3rem', 'display': 'inline', 'color': 'white'}
                                        ),
                                        dbc.NavLink(
                                            "Logout",
                                            href="/app_2_raw_dash/logout/",
                                            external_link=True,
                                            style={"display": "inline", "color": "white"}
                                        ),
                                    ],
                                    className="mt-1",
                                )
                            ],
                            justify="between",  # Align items horizontally between start and end of container
                        ),
                    ],
                    fluid=True  # Stretching the contents within containe to full page
                ),
                color="primary",  # Set navbar background color
                dark=True  # Set navbar text color to white
            ),
    
      
    dcc.Location(id='url2', refresh=False),
    dcc.Location(id='redirect2', refresh=True),
    dcc.Store(id='login-status2', storage_type='session'),
    html.Div(id='page-content2'),   # main Search page callback output
    dash.page_container,           # The output of our pages will be shown here. ref. 3 in design.txt
    
    
    
    
   
    
])

# print("LAYOUT2",layout)