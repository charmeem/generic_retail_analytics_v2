
"""
Created on Mon Mar 25 10:20:19 2024

@author: Muhammad Mubashir Mufti

This is one of the application within multipage Dash application embedded in Flask framework.

This filecovers the Analytic page within application 'demo2' that deals with Media Analysis

There was 'demo1' that deals with Retail industry analytics

'demo2' is not using Page Function of Dash's Multipage recommended way

Reason is it is not working within multi app paradigm of Flask framework

So on application 'demo1' can use page functionality at a time, As far as i tried and found.

IMPORTANT: THIS FILE ONLY CONTAINS LAYOUT!!!!!!!
           ALL CALLBACKS ARE INCLUDED IN THE COMBINED FILE 'callbacks.py'

"""

# from dash.dependencies import Input, Output, State
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
import dash
import pandas as pd
import os


# Define base directory (replace with your application's base directory)
base_dir = os.path.dirname(os.path.abspath(__file__))  # Get current file's directory

# Combine path components (assuming dataset folder is one level down)
filepath = os.path.join(base_dir, "../dataset", "media1.csv")

# Read the CSV file
df = pd.read_csv(filepath)


# Available options for filters (extract from DataFrame)
dates = list(df['Date'].unique())
# segments = list(df['Hour'].unique())
# programes = list(df['Program_Type'].unique())
# topics = list(df['Topic'].unique())
# channels = list(df['TV'].unique())


# Sample data (replace with your actual data source)
data = {
    "Talkshows" : 3150,
    "Headlines" : 120,
    "News" : 1030 }

# Function to format time in a user-friendly way
def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    time_string = ""
    if hours > 0:
        time_string += f"{hours}h "
    if minutes > 0:
        time_string += f"{minutes}m "
    time_string += f"{seconds}s"
    return time_string

#----------------------
# Layout components
#---------------------
layout =  html.Div([ 
            html.H1(' Data Analytics ', className="display-3 mt-5"),
            
            dbc.Container([
                
                dbc.Row(
                    [
                        dbc.Col(
                            [
                            # Dropdown #1
                            html.Label("Date:", style={'fontSize':20, 'textAlign':'center'}),
                            dcc.Dropdown(
                                id='date-filter',
                                options=[{'label': d, 'value': d} for d in dates],
                                value=None,  # Initially show all speakers
                                clearable=False,
                                className='dropdown',  # Class for basic styling
                            )], md=4),
                        dbc.Col(
                            [
                            # Dropdown #2
                            html.Label("Segment:", style={'fontSize':20, 'textAlign':'center'}),
                            dcc.Dropdown(
                                id='segment-filter',
                                options=[],
                                value=None  # Initially show alltime segments
                                )], md=4),
                        dbc.Col(
                            [
                            # Dropdown #3
                            html.Label("Program:", style={'fontSize':20, 'textAlign':'center'}),
                            dcc.Dropdown(
                                id='topic-filter',
                                options=[],
                                value=None  # Initially show all dates
                                )], md=4),
                    ]
                ),
            
            ]),
        
    
    # Stats Section Layout
        # html.Div(
        #     [
        #         html.H5("Summary"),
        #         *[
        #             html.Div(
        #                 [
        #                     html.Span(category, className="stat-label"),
        #                     html.Span(
        #                         f"{format_time(data[category])}",
        #                         className="stat-value",  # New class for styling
        #                     ),
        #                 ],
        #                 className="stat-item",
        #             )
        #             for category in data.keys()
        #         ],
        #     ],
        #     className="stats-container",
        # ),
        
        
        # Graph Section
        dbc.Container([
            html.H3(' Graphs: ', className="display-3 "),
            dbc.Row(
            [
                dbc.Col(
                    # Graph1: This gives Speakers overview for all Topics within selected Hour and Date.
                    dcc.Graph(id='display-map1', figure={}), md=6),
                dbc.Col(
                    # Graph 2: This gives Speakers overview for selected Topic within selected Hour and Date.
                    dcc.Graph(id='display-map2', figure={}), md=6),
                
            ]
            ),
        
        html.H3(' Table: ', className="display-3 "),    
        # MAIN Table
        dcc.Graph(id='display-map3', figure={}),
        
        
        ])      
        ],
        className='dropdown-container',  # Class for html div positioning
        
            )
    







# #---------------------------------------------------------------
# # Chained Callback functions (update charts and table based on filters)
# #-------------------------------------------------------------

# @callback(
#     Output('segment-filter', 'options'),
#     Input('date-filter','value')
#     )
# def set_segment_options(choosen_date):
#     print("",choosen_date)
#     dff = df[df.Date == choosen_date]
#     segments = list(dff['Hour'].unique())
#     return [{'label': s, 'value': s} for s in segments]
    
