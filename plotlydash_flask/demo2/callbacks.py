# THIS VERSION UTILIZING DCC.STORE THAT HAS LIMITATIONS FOR LARGE DATASET
# HENCE I WILL NOT USE THIS


from dash.dependencies import Input, Output, State
from dash import clientside_callback, dcc, html
import dash_bootstrap_components as dbc
import dash
# from models import User
from flask_login import current_user
from thefuzz import fuzz, process
import psycopg2
from psycopg2 import sql
import pandas as pd
from rapidfuzz import fuzz
from demo2.apps import search               # INclude Search layout on TOP of general layout
from demo2.apps import analytics            # Analytics page of demo2 application
import os
import plotly.express as px
import plotly.graph_objects as go
import re
from dash import dash_table
import dash_ag_grid as dag
import dash_player as player


def register_callbacks(dash_app):
    
    
    #---------------------------------------------------------------------------------
    # Loading data - Using demo3 unrefined to capture all details for search result!!
    # Only for Search and Chained options callbacks!
    # Graph and Table callbacks will use their own data extracted locally
    #--------------------------------------------------------------------------------
    
    # Define base directory (replace with your application's base directory)
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get current file's directory
    
    # Combine path components (assuming dataset folder is one level down)
    filepath = os.path.join(base_dir, "dataset", "media1.csv")
    # filepath = os.path.join(base_dir, "dataset", "demo_4.csv")
    # Read the CSV file
    df = pd.read_csv(filepath)
    
    #------------------------------------------------------------------
    # This callback checks user authentication status on every url change and
    # Stores the user id into Store session 
    #------------------------------------------------------------------
   
    @dash_app.callback(
        # Output('user-status-div', 'children'),  # I donot want to display the link 
        Output('login-status2', 'data'),        #saving the user status in session store
        Input('url2', 'pathname'),
        
        )
    def login_status2(url):
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
    
    #-----------------------------------------------------------------------..........................---
    # Search Component v3
    # Starting with search routines.
    #
    # Callback to fetch data based on keyword
    #
    # - All the components of this call back including Search button component is defined in the layout.py
    #   That triggers input that return table in Output
    # - Loading component associated with button also defined in main callback below 
    #-----------------------------------------------------------------------------------------------------
    
    # Callback to fetch data based on keyword
    @dash_app.callback(
        [Output("data-table", 'children'),       # Table showing Search result i donot want it to print before clientcallback
        Output("search-input",'placeholder'),    # MAking place holder dynamic linked to search type radio button
        Output("alert-container",'children'),    # reminding alert to select Date
        # Output('keyword-store', 'data'),         # Not needed now
        ],        
        [Input("search-button", "n_clicks"),
         Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date'),
         Input('radio_search',"value")           # selecting search type
         ],
        [State("search-input", "value")]
    )
    def fetch_data(n_clicks,start_date,end_date,radios,keyword):
        
        # Check if Dates are selected
        if keyword and not start_date:
            # print("please select the date")
            return "","",dbc.Alert("Please select a date!", color='danger')
        
        
        # Convert string dates to datetime objects
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        #---------------------
        # Dynamic placehoder
        #----------------------
        search_type = radios
        if search_type== 'Single search':
            new_placeholder = f"Enter single keyword like : Allah"
        else:
            new_placeholder = f"Try Entering multiple words with or without , seperation like : Allah,Great"
      
        #---------------------
        # Main Routine
        #---------------------
        if n_clicks and start_date and end_date and keyword:
            try:
                
                #-----------------------------------------------------------
                #
                # Every time search will read from external data base
                # IT IS NOT TIME EFFICIENT 
                # SO I WILL USE THE LOCALLY STORED CSV FILE
                #-----------------------------------------------------------
                
                dfc = df.copy()  # Avoid modifying original DataFrame
                
                # Selected Columns for Table
                dfs = dfc[['Date','Hour','Timestamp','Text','Speakers','image_link','media_link']]
                
                # Selected Columns for Search - we donot want searching on all columns!
                dfss = dfc[['Text','Speakers']]
                
                # Ensure the 'Date' column is in datetime format
                dfs['Date'] = pd.to_datetime(dfs['Date'])
                

                # Filter the DataFrame based on the date range
                date_range_df = dfs[(dfs['Date'] >= start_date) & (dfs['Date'] <= end_date)]
                
                # Removing 00:00:00 time element from date object column
                date_range_df['Date'] = date_range_df['Date'].dt.date
                
                #-----------------------------------------
                # Function for Soft fuzzy based Searching
                #------------------------------------------
                def fuzzy_search(search_terms, date_range_df):
                    """
                    Searches for a term in selected columns of a DataFrame, returning rows with fuzzy matches.
                    Returns:
                        pd.DataFrame: The DataFrame containing only the rows with fuzzy matches.                   
                    """           
                    filtered_rows = date_range_df[dfss.apply(lambda x: any(fuzz.partial_ratio(search_terms.lower(), str(val).lower()) > 80 for val in x.values), axis=1)]
                    return filtered_rows
                
                #----------------------------------------------------
                # Function for comma dilimited based Exact searching
                #----------------------------------------------------
                def combined_search(search_terms, date_range_df):
                    """
                    Searches for exact matches first, then fuzzy matches if no exact matches found.
                    """
                       
                    # Split search terms if comma-separated
                    search_terms = [term.strip().lower() for term in search_terms.split(",")]
                    print(search_terms)
                    # print(search_terms)
                    # Function to check for exact matches in a row
                    def check_exact_match(row):
                        return any(all(term in str(val).lower() for term in search_terms) for val in row.values)
                
                    # Filter for exact matches first
                    exact_matches = date_range_df[dfss.apply(check_exact_match, axis=1)]
                
                    if not exact_matches.empty:
                        return exact_matches
                    else:
                        # If no exact matches, perform fuzzy search
                        return fuzzy_search(search_terms, date_range_df)
                
                
                
                #-----------------------------------------------------------------------------
                # defines a function called fuzzy_search that helps you find rows in a DataFrame
                # where the values in certain columns partially match a given search term.
                #
                # dfss dataframe contains name of the columns to be searched
                #
                # # Fuzzy wuzzy with lemmatization:
                #-----------------------------------------------------------------------------------
                
                # import nltk
                # nltk.download('wordnet')
                # from nltk.stem import WordNetLemmatizer
                
                # def fuzzy_search_with_lemma(search_term, date_range_df):
                #     """
                #     Searches for a term in selected columns of a DataFrame, 
                #     performing lemmatization and returning rows with fuzzy matches.
                #     """
                #     # Initialize the lemmatizer
                #     lemmatizer = WordNetLemmatizer()
                
                #     # Lemmatize the search term
                #     search_term_lemma = lemmatizer.lemmatize(search_term.lower())
                
                #     filtered_rows = date_range_df[dfss.apply(lambda x: any(fuzz.partial_ratio(search_term_lemma, lemmatizer.lemmatize(str(val).lower())) > 80 for val in x.values), axis=1)]
                
                #     return filtered_rows
        
        
                #-------------------------------------------------------
                # Selecting the search method based on the  radio button
                #--------------------------------------------------------          
                if search_type == 'Single search':
                    filtered_df_rows = fuzzy_search(keyword, date_range_df)
                else:
                    filtered_df_rows = combined_search(keyword, date_range_df)
                             
                
                #--------------------------------------------------    
                # This function insert span tags around the search keywords in Text column
                # This is needed in renderer javascripts function
                #
                # Note:
                # Dash table as well as AGGRID inherently does not allow styling
                # inside the html tags due to security reason. Thats the reason
                # that i have to try hard to find THIS SOLUTION eventusaly
                #--------------------------------------------------
                def highlight_text(text, search_terms):
                    """
                    Highlights search terms within cell text (excluding HTML tags for security).
                
                    Args:
                        text (str): Cell text.
                        search_terms (list): List of search terms (lowercase).
                 
                    Returns:
                        str: Cell text with highlighted search terms (wrapped in `<span>` tags).
                    """
                 
                    highlighted_text = text
                    for term in search_terms:
                        # Use a regular expression to find terms without introducing HTML tags
                        # replacement_string = "<span style='background-color: yellow;'>" + "\\1" + "</span>"
                        replacement_string = "<span>" + "\\1" + "</span>"
                        highlighted_text = re.sub(rf"\b({term})\b", replacement_string, highlighted_text, flags=re.IGNORECASE)

                    return highlighted_text
                 
                # Apply highlighting to 'Text' column only
                #
                # .apply() iterative method, when used on a DataFrame column, 
                # systematically goes through each cell of that column, one by one
                
                filtered_df_rows['Text'] = filtered_df_rows['Text'].apply(
                    lambda x: highlight_text(str(x), keyword.split(","))
                )
                
                
                
                #-------------------------------------
                # Constructing Dash AG Grid
                #-------------------------------------              
                
                # Define a list of columns where you want to enable filtering
                filterable_columns = ['Text']  
                
                # -------------------------------------------------------
                # Dynamically create columnDefs with filtering for specified columns
                # 1. MAnaging Javascript renderer for thumbnails
                # 2. Hiding media_link as it is redundane in the table
                # --------------------------------------------------------
                
                # # OLD Code for single renderer only
                # columnDefs = [
                #     {
                #         "field": col, 
                #         "filter": True,
                #         "cellRenderer": "Highlight",  # rendering dashAgGridComponentFunctions.js in assets folder
                     
                #      } if col in filterable_columns else {"field": col} 
                #     for col in filtered_df_rows.columns
                # ]
                
                
                columnDefs = [
                                {
                                    "field": col,
                                    "headerName": col.replace('image_link', 'Media') if col == 'image_link' else col,  # Rename 'image_link' column
                                    "filter": True if col in filterable_columns else False,
                                    "cellRenderer": "ImgThumbnail" if col == 'image_link' or col=='media_link' else "Highlight" if col in filterable_columns else None,
                                    "hide": True if col == 'media_link' else False  # Add hide property
                                } for col in filtered_df_rows.columns
                            ]
                
                
                grid = dag.AgGrid(
                        id="agrid_table",
                        rowData=filtered_df_rows.to_dict('records'),
                        columnDefs= columnDefs,
                        dangerously_allow_code =True,
                        className="ag-theme-alpine-dark",            # Themes
                        # className="ag-theme-quartz-dark",            # Themes
                        # className="ag-theme-balham-dark",            # Themes
                        # columnSize="sizeToFit",
                        # columnSize="autoSize",
                        columnSize="sizeToFit",
                        columnSizeOptions={
                            'defaultMinWidth': 118,
                            'columnLimits': [{'key': 'Text', 'minWidth': 600},
                                             {'key': 'Timestamp', 'minWidth': 155},
                                             {'key': 'Hour', 'minWidth': 118},
                                             {'key': 'Media', 'minWidth': 115}
                                             ],
                        },
                        
                    )
                
                
                # tab.data takes out the props tag of stored table 
                return grid,new_placeholder,""
                
            
            except Exception as e:
                return html.Div(f"An error occurred: {e}")
        
        else:
            return "",new_placeholder,""

        # Initially display loading indicator
        return html.Div("Loading...")
    
    #---------------------------------------------------------------
    # Layouts and Callbacks for Thumbnail Modal image
    # Utilizing dash-player
    # Simple video player didnot work- it was only playing the first video
    #-------------------------------------------------------------------
    
    @dash_app.callback(
        Output("selected_video_url", "value"),
        Output("custom-component-img-modal", "is_open"),
        Input("agrid_table", "cellRendererData"),
        Input("close-modal", "n_clicks"),
        State("selected_video_url", "value"),
    )
    def update_modal(data, n_clicks, selected_video_url):
        ctx = dash.callback_context
        if ctx.triggered:
            triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
            if triggered_id == "close-modal":
                return selected_video_url, False
    
        if data:
            video_url = f"{data['value']['value']}"  # Adjust this URL
            return video_url, True
    
        return selected_video_url, False
    
    @dash_app.callback(
        Output("modal-video-content", "children"),
        Input("selected_video_url", "value"),
        )
    def update_video_content(selected_video_url):
        if selected_video_url:
            return html.Div(
                
                [
                    player.DashPlayer(
                        id='video-player',
                        url=selected_video_url, 
                        controls=True,
                        playing=True,
                        volume=0.9,
                        seekTo=6000,                       
                        style={"width": "100%","height":'auto'}
                    )
                ],
                
            )
        return None
    
    # @dash_app.callback(
    #     Output('confirm-dialog', 'displayed'),
    #     Input("close-modal", "n_clicks"),
    #     )
    # def display_confirm(click):
    #     if click:
    #         return True
    #     return False

    
    # @dash_app.callback(
    #     Output('video-player', 'playing'),
    #     [Input('confirm-dialog', 'submit_n_clicks')]
    # )
    # def update_player_status(sclick):
    #     # print("playing",playing)
    #     print("sclick",sclick)
    #     if sclick:
    #         print("parooooooo")
    #         return False;
            
    #     else:
    #         return 'Player is paused or not ready'
    
    # #---------------------------------------------------------------
    # # Callbacks for Thumbnail Modal image
    # # Working BUT ONLY first Video connectionReset after that 
    # #-------------------------------------------------------------------
    # @dash_app.callback(
    #     Output("selected_video_url", "value"),
    #     Output("custom-component-img-modal", "is_open"),
    #     Input("agrid_table", "cellRendererData"),
    #     Input("close-modal", "n_clicks"),
    #     State("selected_video_url", "value"),
    # )
    # def update_modal(data, n_clicks, selected_video_url):
    #     ctx = dash.callback_context
    #     if ctx.triggered:
    #         triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    #         if triggered_id == "close-modal":
    #             return selected_video_url, False
    
    #     if data:
    #         video_url = f"{data['value']['value']}"  # Adjust this URL
    #         return video_url, True
    
    #     return selected_video_url, False
    
    # @dash_app.callback(
    #     Output("modal-video-content", "children"),
    #     Input("selected_video_url", "value"),
    # )
    # def update_video_content(selected_video_url):
    #     if selected_video_url:
    #         return html.Div(
    #             [
    #                 html.Video(
    #                     id="video-player", 
    #                     src=selected_video_url, 
    #                     controls=True, 
    #                     style={"width": "100%", "height": "400px"}
    #                 )
    #             ]
    #         )
    #     return None

    
    #---------------------------------------------------------------
    # Callbacks for ANALYTIC page
    #-------------------------------------------------------------------
    # Chained Callback functions (update charts and table based on filters)
    #-------------------------------------------------------------
           
    # CALLBACK TO SET Hour SEGMENT OPTIONS
    @dash_app.callback(
        Output('segment-filter', 'options'),
        Input('date-filter','value')
        )
    def set_segment_options(choosen_date):
            
        # Selecting segments from  choosen date
        dff = df[df.Date == choosen_date]
        segments = list(dff['Hour'].unique())
        return [{'label': s, 'value': s} for s in segments]
    
    
    # CALLBACK TO SET TOPIC OPTIONS
    @dash_app.callback(
        Output('topic-filter', 'options'),
        Input('date-filter','value')
        )
    def set_topic_options(choosen_date):
        
        # Selecting segments from  choosen date
        dff = df[df.Date == choosen_date]
        topics = list(dff['Program'].unique())
        return [{'label': t, 'value': t} for t in topics]
   
 
    
    #---------------------------------------------------
    # Callback for Graphs
    #--------------------------------------------------
    # Graph 1: This gives Speakers overview for  
    #          all Topics within selected Hour and Date.
    #--------------------------------------------------
    @dash_app.callback(
        Output('display-map1', 'figure'),
        Input('date-filter', 'value'),
        Input('segment-filter', 'value'),
        
            )
    def update_graph(selected_date, selected_segment):
        
        # We have built a grouped df for the graph pupsoses
        # e.g. demo3_speaker_grouped.csv
        #
        # Combine path components (assuming dataset folder is one level down)
        filepath_speaker = os.path.join(base_dir, "dataset", "demo3_grouped1.csv")
        # Read the CSV file
        df = pd.read_csv(filepath_speaker)
        
        
        if selected_segment is None:  # Check for None explicitly
            return dash.no_update
        
        elif len(selected_segment) == 0:  # Check for empty sequence if not None           
            return dash.no_update
        
        else:                             # Filter the required columns
            dff = df[(df['Date']==selected_date) 
                              & (df.Hour==selected_segment)
                              ]
          
        fig = px.sunburst(dff,
                           color=dff['Speakers'],
                          values='Duration',
                          path=['Date','Hour','Program','Speakers'],
                          height=500,
                          width = 500,
                         # color_discrete_sequence= graph_color
                        )   
        return fig
    
    #--------------------------------------------------
    # Graph 2: This gives Speakers overview for  
    #          selected Topic within selected Hour and Date.
    #--------------------------------------------------
    @dash_app.callback(
        Output('display-map2', 'figure'),
        Input('date-filter', 'value'),
        Input('segment-filter', 'value'),
        Input('topic-filter', 'value'),
            )
    def update_graph(selected_date, selected_segment,selected_topic):
        
        # We have built a grouped df for the graph pupsoses
        # e.g. demo3_speaker_grouped.csv
        #
        # Combine path components (assuming dataset folder is one level down)
        filepath_speaker = os.path.join(base_dir, "dataset", "demo3_grouped1.csv")
        # Read the CSV file
        df = pd.read_csv(filepath_speaker)
               
        if selected_segment is None:  # Check for None explicitly
            return dash.no_update
        elif len(selected_segment) == 0:  # Check for empty sequence if not None           
            return dash.no_update
        else:                             # Filter the required columns
            dff = df[(df['Date']==selected_date) & (df.Hour==selected_segment)& (df.Program==selected_topic)
                              ]
           
        fig = px.sunburst(dff,
                           color=dff['Speakers'],
                          values='Duration',
                          path=['Date','Hour','Program','Speakers'],
                          height=500,
                          width = 500,
                         # color_discrete_sequence= graph_color
                        )
        
        return fig
    #--------------------------------------------------
    # Callback for MAIN TABLE
    #--------------------------------------------------
    # Genarates table from main Dataframe
    #--------------------------------------------------
    @dash_app.callback(
        Output('display-map3', 'figure'),
        Input('date-filter', 'value'),
        Input('segment-filter', 'value'),
        Input('topic-filter', 'value'),
            )
    def update_graph(selected_date, selected_segment,selected_topic):
        
        # We have built a grouped df for the graph pupsoses
        # e.g. demo3_speaker_grouped.csv
        #
        # Combine path components (assuming dataset folder is one level down)
        filepath_speaker = os.path.join(base_dir, "dataset", "media1.csv")
        # Read the CSV file
        df = pd.read_csv(filepath_speaker)
        
        # Selected Columns
        dfs = df[['id','Date','Hour','Timestamp','Text','Program','Speakers','media_link']]
        
        
        if selected_segment is None:  # Check for None explicitly
            return dash.no_update
        elif len(selected_segment) == 0:  # Check for empty sequence if not None           
            return dash.no_update
        else:                             # Filter the required columns
            dff = dfs[(dfs['Date']==selected_date) & (dfs.Hour==selected_segment)& (dfs.Program==selected_topic)]
            
        fig = go.Figure(data=[go.Table(
                header=dict(values=list(dff.columns),
                            fill_color='paleturquoise',
                            align='left'),
                cells=dict(values=[dff.id,dff.Date,dff.Hour, dff.Timestamp, dff.Text, dff.Program, dff.Speakers, dff.media_link],
                           fill_color='lavender',
                           align='left'))
            ])
        
        fig.update_layout(height=1000)
        
        return fig

    #--------------------------------------------------------
    # Main Call back that display the landing page of Dash App
    # As well as code to control authentication
    #-----------------------------------------------------------
    @dash_app.callback(
    Output('page-content2', 'children'),
    Output('redirect2', 'pathname'),
    Input('url2', 'pathname'),
    )
    def display_page(pathname):
        
        
        # When dash.no_update is returned for an output, it signifies to Dash 
        # that you don't want to update that specific component. 
        # It's a way to avoid unnecessary re-renders.
        redirect_path = dash.no_update
    
        #Redirection to another page [ Analytics ] defined in layout.py
        if pathname=='/demo2/analytics':
            view = analytics.layout                   # Calling analytic page file layout
        
        # Authentication for landing page
        if pathname == '/demo2/':
            if current_user.is_authenticated:
                view = search.layout                   # Calling search page file layout
                
            else:
                redirect_path = '/login'
    
        return view, redirect_path

    