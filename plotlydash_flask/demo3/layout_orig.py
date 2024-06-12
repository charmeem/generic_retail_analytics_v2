# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 11:36:04 2024

@author: Muhammad Mubashir Mufti
"""
# --------------------------------------------
# This Is the Main Combined Layout 
#------------------------------------------------

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc 



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
                                    dbc.Col(dbc.NavbarBrand(html.H6("Tools",
                                         className='mt-5'  # margin-top
                                        )))
                                ],
                                align="center",  #Vertical center
                                
                            ),
                            dbc.Row(
                                [
                                    dbc.NavItem(
                                        [
                                            
                                            dbc.NavLink("MP4-Mp3 Convertor", href="/demo3/", external_link=True, style={'paddingRight':'3rem','display':'inline','color':'orange'}),
                                            dbc.NavLink("Home", href="/demo3/", external_link=True, style={'paddingRight':'3rem','display':'inline','color':'orange'}),
                                            dbc.NavLink("Logout", href="/app_3_raw_dash/logout/", external_link=True, style={"display": "inline", "color": "orange"}),
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
            
    dcc.Location(id='url3', refresh=False),
    dcc.Location(id='redirect3', refresh=True),
    dcc.Store(id='login-status3', storage_type='session'),
    html.Div(id='page-content3'),   # main  page callback output
    # dash.page_container,           # The output of our pages will be shown here. ref. 3 in design.txt
    
    html.Div([
       
               dbc.Container(
                   
                   [     
                    dbc.Row(
                        
                                            
                        ),
             
                    dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Input( placeholder="Enter keyword and press Search button", type="search", id="search-input",
                                          style={'width': '60%','margin-right': '1rem'}  ),
                                dbc.Button("Search", id="search-button", className=" contrast-button"),
                                
                            ],
                            className="d-flex justify-content-center",  # Centered input and button
                            
                            )
                        ],
                    
                    ),     
                   ],
                   className= "mx-4 mt-5 mb-3"
                 )
                  
           ])
    
    
    
    
   
    
])