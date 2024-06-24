# --------------------------------------------
# This Is the Layout  for 
#
# - Search Page
#
#------------------------------------------------

"""
Created on Mon Mar 25 10:20:19 2024

@author: Muhammad Mubashir Mufti

This is one of the application within multipage Dash application embedded in Flask framework.

This filecovers the Search page within application 'demo2' that deals with Media Analysis

There was 'demo1' that deals with Retail industry analytics

'demo2' is not using Page Function of Dash's Multipage recommended way

Reason is it is not working within multi app paradigm of Flask framework

So on application 'demo1' can use page functionality at a time, As far as i tried and found.

IMPORTANT: THIS FILE ONLY CONTAINS LAYOUT!!!!!!!
           ALL CALLBACKS ARE INCLUDED IN THE COMBINED FILE 'callbacks.py'

"""

from dash import dcc, html, callback
import dash_bootstrap_components as dbc
import dash
import pandas as pd
import os
from datetime import date
from dash import dash_table   
    
layout = html.Div([
    
            dbc.Container(
                
               [     
                  dbc.Row(
                  [
                      dbc.Col(
                          [ 
                             dcc.DatePickerRange(
                                 id ="date-picker-range",
                                 # minimum_nights=5,
                                 # clearable=True,
                                  with_portal=True,
                                 # start_date=date(2023, 6, 21),
                                 min_date_allowed=date(2023, 1, 5),
                                 max_date_allowed=date(2040, 9, 19),
                                  initial_visible_month=date(2024,1,1),
                                  
                                 ), 
                              ],md=6),
                      # dbc.Col(
                      #     [ 
                             
                      #        dcc.Dropdown(
                      #            id='segment-filter',
                      #            options=[],
                      #            value=None  # Initially show all dates
                      #            ) 
                      #         ],md=4),
                   ]),
                  dbc.Row(
                      dbc.Col(
                          html.Div(id='alert-container'),md=3
                          ),
                      ),
                  
                ]),

            

         dbc.Container(
             
            [       
                    dbc.Row(
                        
                         dcc.RadioItems(['Single search', 'Multiple match'], 'Single search',id = "radio_search", inline=True,style={'margin-left': '15rem'})
                                         
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
                    # fluid=True,
                    # className="py-3 text-center",
                    # className="py-3 mb-5 rounded-3 jumbotron-blue text-center d-flex justify-content-center align-items-center",
                    # style={'margin-left':'8rem', 'margin-right':'8rem','margin-top':'4rem'},
                    className= "mx-4 mt-5 mb-3"
                ),
         dbc.Container(
             
            [ 
                dbc.Row(
                [
                    dbc.Col(
                        dcc.Loading(
                            id="loading-output",
                            type="default",
                            children=[
                                html.Div(id="data-table"),
                                # dcc.Markdown(html.Div(id="data-table")),
                                
                            #     # dash_table.DataTable(id="table"),
                            # #     # html.Div(id="table")
                                ],
                            
                            
                        ),
                        # md=10,                       
                    ),
                ],
                ),   
                    ]
            ),
        
        # dcc.Input(id='update-trigger', type='text', value='initial', style={'display': 'none'}),
        # html.Div(id="highlight-trigger", style={"display": "none"}),
        # html.Script(src=app.get_asset_url("dashAgGridComponentFunctions.js")),   # faulty syntax 
        # dcc.Loading(dcc.Store(id="data-table"), fullscreen=True, type="dot"),
        # dcc.Markdown(dangerously_allow_html=True, children='''This should be <mark style="background-color:blue" children="highlighted" />'''),
        # dcc.Markdown(id='data-table',dangerously_allow_html=True, children='''html.Div(id="data-table"),'''),
        # html.Div(id="dummy"),
        # DataTable to display the DataFrame
        # dash_table.DataTable(id='data-table'), 
        # dcc.Store(id="data-table"),
        # html.Div(id='data-table',style={'display': 'none'}),
        # html.Div(id='data-table',dangerously_allow_html=True),
        dcc.Store(id='keyword-store', storage_type='session'), # for storing keyword to be accessed by Javascript 
       # html.Div(id='table-container'),  # Container for the DataTable
       # dcc.Link(href='https://code.jquery.com/jquery-3.6.3.min.js'),  # Replace with your jQuery version
       # html.Div(id='js-container', style={'display': 'none'}),  # Container for JavaScript
       
       dcc.Input(id="selected_video_url", type="hidden", value=""), 
       dbc.Modal(
           [
               dbc.ModalHeader(dbc.ModalTitle("Video Player")),
               dbc.ModalBody(id="modal-video-content"),
               dbc.ModalFooter(
                   dbc.Button("Close", id="close-modal", className="ml-auto")
               ),
           ],
           id="custom-component-img-modal",
           is_open=False,
           # style={"width": "100%", "height": "600px"} 
       ),
       # dcc.ConfirmDialog(
       #     id='confirm-dialog',
       #     message='Are you sure you want to close the modal?',
       #     # displayed=False,
       # ),
    ],
                
  ),