# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 11:30:53 2024

@author: Muhammad Mubashir
"""
import dash
from dash.dependencies import Input, Output, State
from dash import clientside_callback, dcc, html
import pandas as pd
import os
from demo3.apps import mp3conv   # Adding page specific layout on top of main layout
from flask_login import current_user

def register_callbacks(dash_app):
    
    #------------------------------------------------------------------
    # This callback checks user authentication status on every url change and
    # Stores the user id into Store session 
    #------------------------------------------------------------------
   
    @dash_app.callback(
        # Output('user-status-div', 'children'),  # I donot want to display the link 
        Output('login-status3', 'data'),        #saving the user status in session store
        Input('url3', 'pathname'),
        
        )
    def login_status3(url):
        ''' callback to display login/logout link in the header '''
        
        if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated \
                and url != '/logout':  # If the URL is /logout, then the user is about to be logged out anyways
            
            return ( 
                # dcc.Link('logout', href='/logout'),
                current_user.get_id())
        else:
            return (
                # dcc.Link('login', href='/login'),
                'loggedout' )       
  
#------------------------------------------------------------
# Main Callback
# Input:MP4
#------------------------------------------------------------
    @dash_app.callback(
        Output('', ''),        #saving the user status in session store
        Input('convert-button', 'n_clicks'),
        State('base_folder','value')
        
        )
    def convertor(click,folder):
        print(folder)
        


        