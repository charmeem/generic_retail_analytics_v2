import pandas as pd
import numpy as np
import dash
from dash import dcc, html, dash_table, callback_context, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL, ALLSMALLER 
from dash import register_page
import os
import pathlib
import dash_config                        # Config file
import re


register_page(__name__,order=2,name='View Reports',path='/table')

#-----------------------------------------------------------
# Preparing to load selected report into dataframe variable
#-----------------------------------------------------------
PATH = pathlib.Path(__file__).parent                             # get relative data folder
LEVELS_PATH = PATH.joinpath('../logs/' + dash_config.fold).resolve()  # path to the levels subfolders

def get_log_folders():
    
    #  Creating list of heir subfolders created in the 'logs' folder
    heirlist=os.listdir(LEVELS_PATH)
    
    # Finding common elements between two arrays! 
    # Selecting the single level heirarchy subfolders as 'man','bra'
    # converting dictionary values to list and then array before doing intersect1d
    
    single_level_abb = np.intersect1d(np.array(list(dash_config.heirarchies.values())),heirlist)
    
    # Converting abbreviated list into full name list with the help of dictionary values 
    single_level_full = []
    for n in single_level_abb:
        for key,value in dash_config.heirarchies.items():
            if value==n:
                single_level_full.append(key)
    
    return single_level_full            
            
#---------------------------------------------------------
#     Fetch lists of FACTS for a given heirarchy level
#---------------------------------------------------------
def get_facts(level):
    
    # Level convert full name to abbr. using dictionary stored in dash_config.py
    for key,value in dash_config.heirarchies.items():
        if key==level:               # Check if level is full name like 'Brand'
            level = value            # convert it to the abbreviated names stoed in values
        
    # Create path variable to the levels subfolders 
    FACTS_PATH = PATH.joinpath('../logs/' + dash_config.fold + '/' + level).resolve()     

    # Creating list of all the fact reports stored in respective level subfolder
    factslist=os.listdir(FACTS_PATH)
    
    # Creating new list of kpi_list_with_us after removing .csv from the facts names
    kpi_list_with_us=[]
    for f in factslist:                                 #Looping throungh the files
        pattern=re.compile(r'([a-zA-Z_]+)(\.csv)')      #Creating a pattern by dividing it into sub groups, check video of regex in video folder
        kpi=pattern.sub(r'\1',f)                        # Select the part of substring that contains name of kpi
        kpi_list_with_us.append(kpi)                                # Filling the empty list

    # Removing '_' before using it in dropdown selectors
    kpi_list_without_us=[]
    for fk in kpi_list_with_us:
            kpi_list_without_us.append(fk.replace('_',' '))

    return kpi_list_with_us, kpi_list_without_us

style1 = {'marginLeft':'37%'}
style2 = {'marginLeft':'1%'}

# Creating jumbotron like style Component
jumbotron = html.Div(
                dbc.Container(
                    [
                        html.H1('Retail Audit KPI Report Viewer', className="display-3"),
                        html.H4(
                            " Here you can view Retail related KPI's reports for different levels ",
                            className="lead",
                        ),
                        html.Hr(className="mt-2 mb-5"),
                                              
                    ],
                    fluid=True,
                    className="py-3 text-center",
                ),
                className="p-3 mb-5 bg-light rounded-3",
            )

# Layout

layout=  dbc.Container(
            [
                jumbotron,
                
                dbc.Button("Select Level", id='level_button',style={'display':'none'}), # Button only to be used as dummy in callback below
                
                dbc.Row([                   
                    dbc.Col(
                        id='ldd',
                        # html.Div(id='ldd'),
                        # width=3,
                        ),
                    dbc.Col(
                        id='kpidd',
                        # html.Div(id='kpidd'),
                        width=3,
                        ),    
                    ],
                    justify="center",
                    className='mb-5'
                    ),
                
                html.Div(id='table',children=[]),
                html.Br(),
                html.Br(),
            ],
            # fluid=True,
            # className = "d-flex justify-content-center"
            
    
        )

# Generating level dropdown
@callback(
    Output('ldd','children'),
    Output('ldd','width'),             #Want to change ldd col width from 3 to 10
    Input('level_button','n_clicks')   # Button only to be used as dummy
    )
def level_dropdown(click):
    
    # Calling function, this must be included in the callback function    
    single_level_full = get_log_folders()
    
    # Check if array is not empty
    if single_level_full:       
        ldd = html.Div([
                dcc.Dropdown(
                    id="leveldd",
                    options=[{'label':h,'value':h} for h in single_level_full],
                    # value=single_level_full[0],      # selecting first element of the above list as initial value
                    placeholder="Select level",
                    clearable=False,
                                      
                 )
              ],             
            )
        return [ldd, '3']    
    else:
        ldd = html.H2('KPI report folders are empty please generate KPI reports first!',className=' text-center text-info')            
        return [ldd,'10']

# Generating FACTS Drop list dynamicaly based on Heirarchy level selection
@callback(
    Output('kpidd','children'),
    # Output('kpi_store','data'),
    Input('leveldd','value')
    )

def kpi_dropdown(level):
    
    # Call external function to get kpi list with and without UnderScore
    if level:
        kpi_list_with_us, kpi_list_without_us = get_facts(level)
        
        kpi_dd = html.Div(
                    [
                    # html.Label("Select kpi"),
                    dcc.Dropdown(
                        id="kpi",
                        options=[{'label':k,'value':k} for k in kpi_list_without_us],
                        # value=kpi_list_without_us[0],      # selecting first element of the above list as initial value
                        placeholder="Select KPI",
                        clearable=False,
                        
                         )],
                    )
        return  kpi_dd


# Creating Dash Table
@callback(
    Output('table','children'),
    Input('kpi','value'),
    Input('leveldd','value'),
    )
def table_view(fact,level):
    
    if level:        
        # Level convert full name to abbr. using dictionary stored in config.py
        for key,value in dash_config.heirarchies.items():
            if key==level:               # Check if level is full name like 'Brand'
                level_abb = value            # convert it to the abbreviated names stoed in values
        
        # Create path variable to the levels subfolders 
        FACTS_PATH = PATH.joinpath('../logs/' + dash_config.fold + '/' + level_abb).resolve() 
        
    # replacing space with underscore
    if fact:
        fact_us=fact.replace(' ','_')
        
        # Read CSV files based on above selection
        df = pd.read_csv(FACTS_PATH.joinpath(fact_us + ".csv"))
        
        # DASH TABLE
        my_table = dash_table.DataTable(
                            id='not_same_as_table',   #WARNING !! DOnt keep this id same as in LAYOUT ID fro table !!
                            columns=[{"name": i, "id": i} for i in df.columns],
                            data=df.to_dict('records'),
                            # editable=True,              # allow editing of data inside all cells
                            filter_action="native",     # allow filtering of data by user ('native') or not ('none')
                            sort_action="native",       # enables data to be sorted per-column by user or not ('none')
                            sort_mode="single",         # sort across 'multi' or 'single' columns
                            # column_selectable="multi",  # allow users to select 'multi' or 'single' columns
                            # row_selectable="multi",     # allow users to select 'multi' or 'single' rows
                            # row_deletable=True,         # choose if user can delete a row (True) or not (False)
                            # selected_columns=[],        # ids of columns that user selects
                            # selected_rows=[],           # indices of rows that user selects
                            page_action="native",       # all data is passed to the table up-front or not ('none')
                            page_current=0,             # page number that user is on
                            page_size=26,                # number of rows visible per page
                            style_cell={                # ensure adequate header width when text is shorter than cell's text
                                'minWidth': 95, 'maxWidth': 95, 'width': 95
                            },
                            style_data={                # overflow cells' content into multiple lines
                                'whiteSpace': 'normal',
                                'height': 'auto'
                            }
                        ),
        
        return my_table
    