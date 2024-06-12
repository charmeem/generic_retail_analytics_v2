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
                        # html.A(            #Html A link enclosing logo
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Img(
                                        # src=dash_app.get_asset_url('piesis_logo.jpg'),
                                         src="assets/piesis_logo.jpg",
                                        alt='Logo',
                                        height='80px')),
                                    dbc.Col(dbc.NavbarBrand(html.H6(" Searchable video Archive",
                                         className='mt-5'  # margin-top
                                        )))
                                ],
                                align="center",  #Vertical center
                                
                            ),
                            dbc.Row(
                                [
                                    dbc.NavItem(
                                        [
                                            dbc.NavLink(
                                                dbc.Button("Analytics", type="button", id="analytics-button", className="contrast-button mt-4"),
                                                href="/demo2/analytics",
                                                style={"display": "inline"},
                                            ),
                                            dbc.NavLink("Home", href="/demo2/", external_link=True, style={'paddingRight':'3rem','display':'inline','color':'orange'}),
                                            dbc.NavLink("Logout", href="/app_2_raw_dash/logout/", external_link=True, style={"display": "inline", "color": "orange"}),
                                        ],
                                        className="mt-1",
                                    )
                                ],
                                justify="between",  # Align items horizontally between start and end of container
                            ),

                            
                        ],
                        fluid=True  # Stretching the contents within containe to full page
                    ),
                    className="m-2 mb-5"
                   ),
      
            
            
            
            # Loading spinner icon
            
    
      
    dcc.Location(id='url2', refresh=False),
    dcc.Location(id='redirect2', refresh=True),
    dcc.Store(id='login-status2', storage_type='session'),
    html.Div(id='page-content2'),   # main Search page callback output
    dash.page_container,           # The output of our pages will be shown here. ref. 3 in design.txt
    
    
    
    
   
    
])

# print("LAYOUT2",layout)