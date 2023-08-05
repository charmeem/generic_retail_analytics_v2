import plotly.express as px
import pandas as pd
import numpy as np
from dash import dcc
# import dash_core_components as dcc   #deprecated
from dash import html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL
import os
import plotly.graph_objects as go
# from plotly.colors import n_colors
import re
import pathlib
# from app import app
from dash import register_page
import sys


#--------------------------------------------------------------------------------------
#             IMPORTANT CONCEPT
#
# pathlib.PATH(__file).parent = PATH where the current file is located
# sys.path = Set of paths related to this project
# sys.path.append() adds one more path into this set of paths.
#
# Now Whn we import our local modules the system will search that module into paths mentioned in sys.path
# in this way we donot need to specify the absolute path of each of the folders of the modules !!
#
#  EXAMPLE is following 'import dash_config' command
#-----------------------------------------------------------------------------------
PATH = pathlib.Path(__file__).parent
# adding a new path into the PATH sets of variable
sys.path.append('plotlydash_flask/demo1/')

import dash_config

#----------------------------------------------------------
#       MAIN PAge- generates Graphs dash board
#----------------------------------------------------------

# Registering this page into Dash
register_page(__name__,order=1,name='Business Graphs',path='/plot')

# get relative data folder
PATH = pathlib.Path(__file__).parent
# print('PATH',PATH)
# DATA_PATH = PATH.joinpath("../dataset/graphs").resolve()
LEVELS_PATH = PATH.joinpath('../logs/' + dash_config.fold).resolve()  # path to the levels subfolders


#---------------------------------------------------------------------------------------------------
#   Main Functions - Python code
#
#   Fetch stored report files based on the FACTS Input selected from dropdown list in call back below
#   Inputs:
#          kpi, geographical region, product heierarchies, path to the facts files.
#   Outputs:
#           Fact Data frame, Some other data frames 
#----------------------------------------------------------------------------------------------------

def reports_df(kpi,heichy,FACTS_PATH):
    
    ### Single HEIRARCHY Handling  - See heirarchy.csv file in data/csd folder
    #3 Size
    #4  Brand
    #5  Vendor
    #6  Flavor   
    # Note single heirarchies used particulary in Numeric handling and similiar reports
    
    # FACT/KPI
    # Examples:
    #   kpi = "Volume_Share"
    #   kpi = "Value_Share"
    
    # MBD
    # Exapmles:
    # geog = "Total"
    # geog = "NATIONAL RURAL"
    # geog = "NATIONAL URBAN"
    # geog = "LAHORE FRANCHISE"
  
    
    
    # Read CSV files based on above selection
    # Select the relevent csv log files generaterd by AR reporting tool
    
    df_reports = pd.read_csv(FACTS_PATH.joinpath(kpi + ".csv") ,header=[0,1])
    

    ### Renaming  levels of 1st column
    df_reports = df_reports.rename({'Unnamed: 0_level_0': heichy}, axis='columns', level=0)
    df_reports = df_reports.rename({'Month': ''}, axis='columns', level=1)
    
    # Convert heirarchies column to index to facilitae future sorting
    df_reports = df_reports.set_index(heichy)
    
    return df_reports

def other_tables(kpi,geog,heichy,FACTS_PATH):
    
    df_reports = reports_df(kpi,heichy,FACTS_PATH)
    
    # Extracting Waves from multiindex columns
    wavelist = [x[1] for x in df_reports.columns]  #second element of all the first tuple,as rest are repetition
    wavelist = list(set(wavelist))                 # Filter out unique items from this list, Convert set type to list                   
    wavelist.sort()

    # Only select Geography and one Wave at a time and save it in a dictionary
    df={}
    for w in wavelist:
        df["df" + str(w)]= df_reports[geog,w].sort_values(ascending=False)

    # Performing left join operation on the elements of this dictionary
    # Initialy it is done for upto 9 months
    if len(wavelist) == 1:
        merg2 = list(df.values())[0].to_frame()
    elif len(wavelist) == 2:
        merg2 = pd.merge(list(df.values())[0].to_frame(),list(df.values())[1].to_frame(),how='left',left_index=True,right_index=True)
    elif len(wavelist) == 3:
        merg2 = (pd.merge(list(df.values())[0].to_frame(),list(df.values())[1].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[2].to_frame(),how='left',left_index=True,right_index=True))
    elif len(wavelist) == 4:
        merg2 = (pd.merge(list(df.values())[0].to_frame(),list(df.values())[1].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[2].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[3].to_frame(),how='left',left_index=True,right_index=True)) 
    elif len(wavelist) == 5:
        merg2 = (pd.merge(list(df.values())[0].to_frame(),list(df.values())[1].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[2].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[3].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[4].to_frame(),how='left',left_index=True,right_index=True))
    elif len(wavelist) == 6:
        merg2 = (pd.merge(list(df.values())[0].to_frame(),list(df.values())[1].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[2].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[3].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[4].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[5].to_frame(),how='left',left_index=True,right_index=True))    
    elif len(wavelist) == 7:
        merg2 = (pd.merge(list(df.values())[0].to_frame(),list(df.values())[1].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[2].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[3].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[4].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[5].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[6].to_frame(),how='left',left_index=True,right_index=True)) 
    elif len(wavelist) == 8:
        merg2 = (pd.merge(list(df.values())[0].to_frame(),list(df.values())[1].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[2].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[3].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[4].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[5].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[6].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[7].to_frame(),how='left',left_index=True,right_index=True)) 
    elif len(wavelist) == 9:
        merg2 = (pd.merge(list(df.values())[0].to_frame(),list(df.values())[1].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[2].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[3].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[4].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[5].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[6].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[7].to_frame(),how='left',left_index=True,right_index=True)
              .merge(list(df.values())[8].to_frame(),how='left',left_index=True,right_index=True))      



    # merg1 = pd.merge(list(df.values())[0].to_frame(),list(df.values())[1].to_frame(),how='left',left_index=True,right_index=True)
    # merg2 = pd.merge(merg1,list(df.values())[2].to_frame(),how='left',left_index=True,right_index=True)



    ### Removing Category rows from the table
    # col0 = merg2.columns[0]      # Select first column
    # merg2 = merg2[~merg2[col0].str.contains('Category')]    #Select all the rows except one thatt contains string=Category
    merg2 = merg2[~merg2.index.str.contains('Category')] 

    # Take Top 10 Rows
    # merg2t10 = merg2.head(10)

    # NOw only select rows of the table with values upto some threshold say 'th'
    # For rest of the rows get their sum as a row named 'Others' and concat with above 
    th = 0.4

    col1tup1 = merg2.columns[0]  # checking for threshold for the first column
    merg2trunc = merg2[merg2[col1tup1]>th]

    # Get rest of the rows to create 'others' Row as its sum
    merg2rest = merg2[merg2[col1tup1]<th]
    
    # Create dataframe with a Sum Row named 'Others'
    merg2rest.loc['Others',:]=merg2rest.sum(axis=0)
    
    # Get that last row as a dataframe object
    merg2others = merg2rest.iloc[-1:]
    
    # Concat that 'Others' row with the previous dataframe
    final = pd.concat([merg2trunc,merg2others])

    ### Remove first level to covert it to single level- this is needed for dash_table below
    final1 = final.droplevel(0,axis=1)
    final1 = final1.reset_index()
    
    # removing () from first column
    final1[heichy]=final1[heichy].str.replace(heichy[0:2],'',regex=True).str.replace('(','',regex=True).str.replace(')','',regex=True)
    
    # Rounding the wave columns- the column two onwards
    #Decimal rounding
    d=3
    final1.iloc[:,1:]=final1.iloc[:,1:].applymap(lambda x:round(x,d))
    
    # Dropping Heirarchy column to align table with plottly legend
    # final2 = final1.drop(heichy,axis=1)

    ### Convert multilevel columns into mutiple rows THIS IS NEEDED TO FULFILL THE GRAPH REQUIREMENTS OF PLOTLY EXPRESS
    # BY default inner most level, level=1 in this case is selected to be converted into rows
    merg2s = final.stack()
    
    # Convert Heirarchies index to column
    merg2s=merg2s.reset_index()

    # Renaming level_1
    merg2s= merg2s.rename(columns={'level_1':'Month'})

    #Removing (Ma) from first column
    merg2s[heichy]=merg2s[heichy].str.replace(heichy[0:2],'',regex=True).str.replace('(','',regex=True).str.replace(')','',regex=True)
 

    return final1, merg2s


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



#---------------------------------------------------------------------------------------
# Creating options list for heir/level Dropdown from subfolders created in 'logs' folder
#  single_level_full list
#
# Only fetching the subfolders with single heirarchy/level like 'man', 'fla'
#-----------------------------------------------------------------------------------------
# IMPORTANT : Call this code from callback function to get the latest logs 
#------------------------------------------------------------------------------------------   
def log_folder_list():
    
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
    
    return  single_level_full           
            

#----------------------------------------------------------------------------------------
#                                 Plotly Dash Section
#------------------------------------------------------------------------------------------




# Set initial default values   
geog='Total'


"""
Example
['bra' 'fla' 'man' 'siz']
['Brand', 'Flavor', 'Vendor', 'Size']
"""


"""
# some Alternate regular expressions following Video

# We have to remove preceding heirarchy number and the ending csv from the file names
print('first',heirlist[2])
first = heirlist[2]
pattern = re.compile(r'_\w+')
matches = pattern.finditer(first)
for match in matches:
    print(match)
"""



"""

#Creating Graphs

Creating Figure object in seperate Cards and embedding into final layout

Also creating Tables using Bootstrap Table component from Pandas dataframe

"""



# Different widths for different columns sizes
# no_of_months = len(final1.columns)-1
# if no_of_months == 3:                      #for 3 months table
#     w1=311
#     w2=440
#     lm=0
#     mr=80
#     cw1=90
#     cw2=40
#     ml1='8rem'
#     ml12='8rem'
#     ml2='0rem'
#     jus='center'
# elif no_of_months == 9:                      #for 9 months table
w1=635
w2=660
lm=0
mr=0
cw1=110
cw2=50 
ml1='6.5rem'
ml12='13.5rem'
ml2='7rem'
jus='None'

#--------------------------------------
#       COLORS
#---------------------------------------

# My colors
col1=['#e5383b','#f3722c','#f8961e','#f7b267','#f9c74f','#90be6d','#43aa8b','#577590','#277da1','#f0f3bd','#335c67','#6d597a','#b56576']
col2=['#ffcdb2','#ffb4a2','#e5989b','#b5838d','#6d6875','#cb997e','#ddbea9','#ffe8d6','#b7b7a4','#6b705c','#e5e5e5','#3d5a80','#b56576']

#Colors from plotly_express.colors- see colors.ipynb  notebook in dashboard/plotlydash folder
carto_pastel = ['rgb(102, 197, 204)', 'rgb(246, 207, 113)', 'rgb(248, 156, 116)', 'rgb(220, 176, 242)', 'rgb(135, 197, 95)', 'rgb(158, 185, 243)', 'rgb(254, 136, 177)', 'rgb(201, 219, 116)', 'rgb(139, 224, 164)', 'rgb(180, 151, 231)', 'rgb(179, 179, 179)'] #px.colors.carto.Pastel
carto_antique = ['rgb(133, 92, 117)', 'rgb(217, 175, 107)', 'rgb(175, 100, 88)', 'rgb(115, 111, 76)', 'rgb(82, 106, 131)', 'rgb(98, 83, 119)', 'rgb(104, 133, 92)', 'rgb(156, 156, 94)', 'rgb(160, 97, 119)', 'rgb(140, 120, 93)', 'rgb(124, 124, 124)'] #px.colors.carto.Antique
carto_safe = ['rgb(136, 204, 238)', 'rgb(204, 102, 119)', 'rgb(221, 204, 119)', 'rgb(17, 119, 51)', 'rgb(51, 34, 136)', 'rgb(170, 68, 153)', 'rgb(68, 170, 153)', 'rgb(153, 153, 51)', 'rgb(136, 34, 85)', 'rgb(102, 17, 0)', 'rgb(136, 136, 136)'] #px.colors.carto.Safe
qual_pastel1 = ['rgb(251,180,174)', 'rgb(179,205,227)', 'rgb(204,235,197)', 'rgb(222,203,228)', 'rgb(254,217,166)', 'rgb(255,255,204)', 'rgb(229,216,189)', 'rgb(253,218,236)', 'rgb(242,242,242)'] #px.colors.qualitative.Pastel1
qual_set2 = ['rgb(102,194,165)', 'rgb(252,141,98)', 'rgb(141,160,203)', 'rgb(231,138,195)', 'rgb(166,216,84)', 'rgb(255,217,47)', 'rgb(229,196,148)', 'rgb(179,179,179)'] #px.colors.qualitative.Set2
qual_t10 = ['#4C78A8', '#F58518', '#E45756', '#72B7B2', '#54A24B', '#EECA3B', '#B279A2', '#FF9DA6', '#9D755D', '#BAB0AC'] #px.colors.qualitative.T10
qual_prism = ['rgb(95, 70, 144)', 'rgb(29, 105, 150)', 'rgb(56, 166, 165)', 'rgb(15, 133, 84)', 'rgb(115, 175, 72)', 'rgb(237, 173, 8)', 'rgb(225, 124, 5)', 'rgb(204, 80, 62)', 'rgb(148, 52, 110)', 'rgb(111, 64, 112)', 'rgb(102, 102, 102)']
seq_magenta = ['rgb(243, 203, 211)', 'rgb(234, 169, 189)', 'rgb(221, 136, 172)', 'rgb(202, 105, 157)', 'rgb(177, 77, 142)', 'rgb(145, 53, 125)', 'rgb(108, 33, 103)']
seq_brwnyl = ['rgb(237, 229, 207)', 'rgb(224, 194, 162)', 'rgb(211, 156, 131)', 'rgb(193, 118, 111)', 'rgb(166, 84, 97)', 'rgb(129, 55, 83)', 'rgb(84, 31, 63)']

color_swatches = ['Pastel','Antique','Prism','Magenta','Brwnyl'
                  # 'Safe','T10',
                  # 'Pastel1',
                  # 'Set2'
                  ]
    

colors = {
    'background': '#111111',
#     'background': 'grey',
    'text': '#7FDBFF',    
    }

"""
This Section is creating 3 Cards for Input select controls as
well as Tabs for selecting Types of Graphes and a Action Button
NOT USED!!
"""

# card3 = dbc.Card(
#     [
#         html.Div(
#             [
#                 dbc.Label("Select Graph Types"),
#                 dbc.Tabs(
#             [
#                 dbc.Tab(tab_id='bar',label='Bar'),
#                 dbc.Tab(tab_id='strip',label='Strip')
#             ],
#                 id='graphs',
#                 active_tab='bar',
#                 className='mb-5'    
#                 ),
#                 dbc.Button("Generate Graphs",id='button1',className='mb-2')
#             ],

#         ),

#     ],
#     body=True,
# )

    
#----------------------------------------------------------------------------    
# Creating Application layout using Dynamic( Pattern-Matching) Call backs
# Elements:
# - Button for Multiple graphs
# - Dropdrop for level/heirarchies
# - input text box for decimal places THRESHOLD
# - Div for dynamicaly adding other dropdown elements from call bac
#----------------------------------------------------------------------------

# Creating jumbotron like style Component
jumbotron = html.Div(
                dbc.Container(
                    [
                        html.H1('Graphical data Analysis', className="display-3"),
                        html.H4(" View Graphical presentaion of Retail KPI reports.", className="lead"),
                        html.H6(" Important features:" ),
                        html.H6(" Different Graph types like (Bar plot, Line, Sunburst) with associated Data table, Multi dimentional selection, Multiple Graphs side by side for easy comparison. " ),                      
                        html.Hr(className="mt-2 mb-5"),                                           
                    ],
                fluid=True,
                className="py-3 text-center",
                ),
            className="p-3 mb-5 bg-light rounded-3",
            )


# if single_level_full:
layout=  dbc.Container(
            [   
                jumbotron,
                dbc.Button('Generate new Graph', className='btn-lg mx-5 border border-1',id='add-graph',n_clicks=0),
                html.Div(id='new_row',children=[]),   # Main elements         
                dcc.Store(id='level_store'),           # storing heir level
                dcc.Store(id='fact_store'),
            ],
    # fluid=True,
    # className = "d-flex justify-content-center"
    
)
    
# else:
#     layout = dbc.Container(
#                     [                               
#                       html.H2('Run "Create KPI Reports" First'),
#                     ],fluid=True,
#                         className="py-3 text-center",)

    


    
# removing add graph button if no kpi reports exist
@callback(
    Output('add-graph','style'),
    Input('add-graph','n_clicks')
    )        
def change_button_style(click):
    
    single_level_full = log_folder_list()
    
    return {'display':'none'} if not single_level_full else {'display':'block'}
        

#Main Callback
@callback(    
    Output('new_row','children'),
    Input('add-graph','n_clicks'),
    State('level_store','data'),
    # Input('fact_store','data'),
    State('new_row','children'),
)
def create_basic_layout(n_clicks, level, div_children):
    
    single_level_full = log_folder_list()
    
    if not level:
        if single_level_full:
            level = single_level_full[0]  # taking first heir subdirectory as default
        else:
            return html.H2('KPI report folders are empty please generate KPI reports first!',className='text-center text-info')
    
    # if list then Converting to a string
    if isinstance(level,list):
        level = level[0]      
        
    # Call function to get kpi list with and without UnderScore
    kpi_list_with_us, kpi_list_without_us = get_facts(level)   
     
    # Create path variable to the levels subfolders   
    # Level convert full name to abbr. using dictionary stored in dash_config.py
    for key,value in dash_config.heirarchies.items():
        if key==level:               # Check if level is full name like 'Brand'
            level_abb = value            # convert it to the abbreviated names stoed in values
            
    FACTS_PATH = PATH.joinpath('../logs/' + dash_config.fold + '/' + level_abb).resolve()
    
    # Creating MBD list        
    # Calling reports_df function with default values
    df_reports = reports_df(kpi_list_with_us[0],level,FACTS_PATH)
    label_list = df_reports.columns.get_level_values(0).unique()
    
    
        
    #-------------------------------------------------
    # Creating new dash component for the layout above
    #   3 Rows Bootstrap
    #--------------------------------------------------
    new_element=  html.Div(
                    id='mukh',
                    
                    children=[
                        dbc.Row(
                                html.H5(
                                        id={
                                           'type': 'dynamic-title',
                                           'index': n_clicks
                                       },
                                        style={
                                               # 'color':'#ae2012',
                                               'color':'#5a5a5a',
                                               'backgroundColor':'#f2f2f2',
                                               'padding':'0.3rem',
                                               'borderRadius':'5px',
                                               'textAlign':'center'},                                  
                                        className='mb-5 display-6',
                                )   
                        ),
                                             
                       dbc.Row([
                               dbc.Col([
                               html.Label("Facts:",
                                          # style={'backgroundColor':'white'}
                                          # className='text-center text-dark'
                                         ),     
                               dcc.Dropdown(
                                   id={
                                        'type': 'dynamic-facts',
                                        'index': n_clicks
                                       },
                                   options=[{'label':f,'value':f} for f in kpi_list_without_us],
                                    # placeholder="Select Fact",
                                    value=kpi_list_without_us[0],
                                   clearable=False,
                                   )],width=5),
                           
                            dbc.Col([
                                html.Label("Markets:",
                                           # style={'color':'black'}
                                          ),
                                dcc.Dropdown(           
                                    id={
                                        'type': 'dynamic-mbds',
                                        'index': n_clicks
                                        },
                                    options=[{'label':m,'value':m} for m in label_list],
                                    value=label_list[0],
                                    # placeholder="Select Market",
                                    clearable=False,
                                    )],width=5),
                           ],
                           # className='mb-5',
                           # style={'marginTop':'-6rem'}
                           # align='center'
                       ),

                        dbc.Row(
                            [               
#                             dbc.Col([
#                                 html.Label("Threshold: ",
#                                            # style={'color':'black'}
#                                           ),
#                                 dcc.Input(

#                                     id={
#                                         'type': 'dynamic-thr',
#                                         'index': n_clicks
#                                         },
#                                     value='0.4',type='text'
#                                 )],width=5),    
                            dbc.Col([
                                html.Label("Heirarchies:",
                                            ),
                                dcc.Dropdown(                      
                                   id={
                                        'type': 'dynamic-heirarchy',
                                        'index': n_clicks
                                        },
                                   options=[{'label':h,'value':h} for h in single_level_full], 
                                   value=single_level_full[0],      # selecting first element of the above list as initial value
                                   clearable=False,
                                    )],width=5),
                                
                                dbc.Col([
                                 html.Label("Select Color Theme: ",
                                             ),
                                 dcc.Dropdown(
                                     id={
                                         'type': 'dynamic-color',
                                         'index': n_clicks
                                         },
                                     options=[{'label':c,'value':c} for c in color_swatches], 
                                     value=color_swatches[0],      # selecting first element of the above list as initial value
                                     clearable=False,
                                 )],width=5),    
                                ],
                                
                            ),
                        
                        dbc.Row(
                            dbc.Tabs(
                                    [
                                        dbc.Tab(label="Line", tab_id="line"),
                                        dbc.Tab(label="Bar", tab_id="bar"),                                     
                                        # dbc.Tab(label="Pie", tab_id="pie"),
                                        dbc.Tab(label="Sunburst", tab_id="sunburst"),
                                        # dbc.Tab(label="Histogram", tab_id="histogram"),
                                        # dbc.Tab(label="Scatter", tab_id="scatter"),
                                    ],
                                    id={
                                        'type': 'dynamic-tabs',
                                        'index': n_clicks
                                        },
                                    active_tab="line",
                                ),
                            className='mt-3',
                            ),       
                      
                    # Both Graphs encapsulated in the single Row
                        dbc.Row(
                            dbc.Col(
                                dcc.Loading(
                                    dcc.Graph(
                                        id={
                                            'type': 'dynamic-graph1',
                                            'index': n_clicks
                                            },
                                        # figure={'layout':{'autosize':True}},
                                        config={'displayModeBar': False},
                                        # responsive=True,               #Setting Graph responsive Not working with line Graph
                                        style={
                                                'marginBottom':'-5.7rem',
                                               'marginLeft':'0rem'
                                              }
                                   )  #Graph        
                               )      # Loading spinner
                            )         #Column
                        ),
                        dbc.Row(
                            dbc.Col(
                                   dcc.Graph(
                                    id={
                                        'type': 'dynamic-graph2',
                                        'index': n_clicks
                                        },
                                    config={'displaylogo':False},
                                    figure={},
                                    # responsive=True,               #Setting Graph responsive Not working with line Graph
                                    style={
                                            'marginLeft':0,
                                            'marginRight':0,
                                            'marginTop':0,
                                            
                                          }
                                )
                                )
                            ),
                            

                    ],             
                  ) # DONT PUT COMMA HERE AS it will generate error "List of List....."
 
    
    div_children.append(new_element)
    return div_children


# Storing level to be used by previous callback
@callback(
    Output('level_store','data'),                                                                 
    Input(component_id={'type': 'dynamic-heirarchy', 'index': ALL}, component_property='value')
    
)
def update_fact_dd(level):
    
    single_level_full = log_folder_list()
    
    
    if not level:
        if single_level_full:
            level = single_level_full[0]  # taking first heir subdirectory as default
        else:
            return html.H2('KPI report folders are empty please generate KPI reports first!',className='text-center text-info')
        
    if isinstance(level,list):
        level = level[0]      # if list then Converting to a string
     
    return level

# Call back to Update KPI and MBD dropdowns above when Heirarchy changes
@callback(
    Output(component_id={'type': 'dynamic-facts', 'index': MATCH}, component_property='options'),
    # Output(component_id={'type': 'dynamic-mbds', 'index': MATCH}, component_property='options'),
    Output(component_id={'type': 'dynamic-facts', 'index': MATCH}, component_property='value'),
    # Output(component_id={'type': 'dynamic-mbds', 'index': MATCH}, component_property='value'),
    # Output('fact_store','data'),
    
    Input(component_id={'type': 'dynamic-heirarchy', 'index': MATCH}, component_property='value'),
    # Input(component_id={'type': 'dynamic-facts', 'index': MATCH}, component_property='value'),
)    

def update_fact_mbd_dd(level):
    #------------
    # KPI Update
    #------------
    # Converting to abbreviated level names / subfolder names
    for key,value in dash_config.heirarchies.items():
        if key==level:
            heir_value_abb=value
    
    # Call function to get kpi list   
    kpi_list_with_us, kpi_list_without_us= get_facts(heir_value_abb)
    
    options1=[{'label':f,'value':f} for f in kpi_list_without_us]
    
    
    
    return options1, kpi_list_without_us[0]


# Call back to Update MBD dropdown OPTION and VALUE parameters above when KPI Changes
@callback(
    Output(component_id={'type': 'dynamic-mbds1', 'index': MATCH}, component_property='options'),
    Output(component_id={'type': 'dynamic-mbds2', 'index': MATCH}, component_property='value'),
    Input(component_id={'type': 'dynamic-facts', 'index': MATCH}, component_property='value'),
    Input(component_id={'type': 'dynamic-heirarchy', 'index': MATCH}, component_property='value'),
)    
def update_mbd_dd(kpi_value,level):
    
    kpi_value=kpi_value.replace(' ','_')   # replacing space with underscore
     
    # Level convert full name to abbr. using dictionary stored in dash_config.py
    for key,value in dash_config.heirarchies.items():
        if key==level:               # Check if level is full name like 'Brand'
            level_abb = value            # convert it to the abbreviated names stoed in values
            
    FACTS_PATH = PATH.joinpath('../logs/' + dash_config.fold + '/' + level_abb).resolve()
    
    # Creating MBD list        
    # Calling reports_df function with default values
    df_reports = reports_df(kpi_value,level,FACTS_PATH)
    mbd_list = df_reports.columns.get_level_values(0).unique()
    
    options=[{'label':f,'value':f} for f in mbd_list]
    
    return options, mbd_list[0]
    

        
#-----------------------------
# Main Callback
# Generates Graphes and Table
#-------------------------------
@callback([
    Output({'type': 'dynamic-graph1', 'index': MATCH}, 'figure'),  # Plot
    Output({'type': 'dynamic-graph2', 'index': MATCH}, 'figure'),  # Table
    Output({'type': 'dynamic-title', 'index': MATCH}, 'children'),
    # Output(component_id={'type': 'dynamic-mbds', 'index': MATCH}, component_property='options'),
    # Output(component_id={'type': 'dynamic-mbds', 'index': MATCH}, component_property='value'),    
    ],
    [Input(component_id={'type': 'dynamic-facts', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-mbds', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-heirarchy', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-tabs', 'index': MATCH}, component_property='active_tab'),
     Input(component_id={'type': 'dynamic-color', 'index': MATCH}, component_property='value'),
     
     # Input({'type': 'dynamic-thr', 'index': MATCH}, 'value'),   USed in bar braph
    ]
        )
def update_graph(kpi_value, mbd_value, heir_value_full,active_tab,color):
    
    # Converting to abbreviated level names / subfolder names
    for key,value in dash_config.heirarchies.items():
        if key==heir_value_full:
            heir_value_abb=value
    
    # Call function to get kpi list fresh value
    # kpi_list_with_us, kpi_list_without_us= get_facts(heir_value_abb)
    
    fact_input=kpi_value.replace(' ','_')   # replacing space with underscore
    
    geog = mbd_value
       
    # Now deriving lists of FACTS from the files in above subfolders
    FACTS_PATH = PATH.joinpath('../logs/' + dash_config.fold +'/' + heir_value_abb).resolve()  # path to the levels subfolders
    
    
    # Fetch other tables from other_tables function
    final1, merg2s = other_tables(fact_input,geog,heir_value_full,FACTS_PATH)
    
   
    
    # ASSIGNING COLORS TO THE GRAPHS AND TABLE
    if color == 'Pastel':
        graph_color = px.colors.carto.Pastel
        tab_color   = carto_pastel
    elif color == 'Antique':
        graph_color = px.colors.carto.Antique
        tab_color   = carto_antique     
    elif color == 'Prism':
        graph_color = px.colors.qualitative.Prism
        tab_color   = qual_prism
    elif color == 'Magenta':
        graph_color = px.colors.sequential.Magenta
        tab_color   = seq_magenta
    elif color == 'Brwnyl':
        graph_color = px.colors.sequential.Brwnyl
        tab_color   = seq_brwnyl    
        
    # elif color == 'Safe':
    #     graph_color = px.colors.carto.Safe
    #     tab_color   = carto_safe 
    # elif color == 'T10':
    #     graph_color = px.colors.qualitative.T10
    #     tab_color   = qual_t10    
        
    # elif color == 'Pastel1':
    #     graph_color = px.colors.qualitative.Pastel1
    #     tab_color   = qual_pastel1 
    # elif color == 'Set2':
    #     graph_color = px.colors.qualitative.Set2
    #     tab_color   = qual_set2         
        
    # When color = None
    
    
    
#-----------------------------
#   Bar graph
#------------------------------

    fig_bar = px.bar(merg2s, color=heir_value_full,x="Month",y=geog,text=geog,
                     color_discrete_sequence= graph_color,
                       # width=500,
                       # height=500,                    
                      # template='simple_white',       
                      # title=kpi,          
                    )

    fig_bar.update_yaxes(
                    autorange="reversed",  # bringing max values on top
                    showline=False,showticklabels=False,ticks="",  #hiding ticks and labels
                    title=""   # Hiding y-axis title            
    )

    fig_bar.update_xaxes(
                   showline=False,showticklabels=False,ticks="",  #hiding ticks and labels
                   title=""                                     # Hiding title of the xaxis
                    )

    fig_bar.update_traces(
                    # marker_color= col1,      #Custom color for whole bar
                    texttemplate='%{text:.2s}', textposition="inside",  # Bringing text inside the bars
                    showlegend=False,
                    )   

    fig_bar.update_layout(
        margin=dict(
                # b=0,
                # l=5,
                # r=10
           ),
        
        bargap=0.01,                                    # control gaps between bars
        uniformtext_minsize=9,uniformtext_mode='hide',  # For controlling text inside the bars
        title_font_size=30,title_font_family="Open Sans",title_font_color="navy",

        # legend=dict(title="",        # Controlled by 'showlegend' above
        # xanchor='left',  # Bring legend to the left
        # x=-1,
        # y=-1,
        #  traceorder="reversed",
        # title_font_family="Times New Roman",
        # font=dict(
        # family="Roboto",
        # size=10,
        # color="black"
        # ),
        # ),
        # legend=dict(orientation='h', title="", x=-0.4,y=1.2),

        legend_tracegroupgap=10,  # gap between legends
        plot_bgcolor="rgba (0,0,0,0)",      # Setting bg to transparent     
        paper_bgcolor="rgba (0,0,0,0)",     # Setting bg to transparent
        # plot_bgcolor=colors['background'],
        # paper_bgcolor=colors['background'],
        # font_color=colors['text']
    )

#-----------------------------------
#        Line Graph
#     
#----------------------------------
    fig_line = px.line(merg2s, x="Month", color=heir_value_full, y=mbd_value,
                        height=500,
                       width = 500,
                        color_discrete_sequence= graph_color
                       # color_discrete_sequence=px.colors.carto.Pastel
                       )    

#-----------------------------------
#        Pie Graph   - NOT WORKING!!!
#----------------------------------

    fig_pie = px.pie(merg2s, values="Month", names=heir_value_full, color=mbd_value, color_discrete_sequence=graph_color)

#-----------------------------------
#        Scatter Graph
#----------------------------------
    
    fig_scat = px.scatter(merg2s,
                          color=heir_value_full,
                          y=geog,
                          x='Month',
                          size=geog,
                          size_max=60,
                          # height=500,
                          # width = 500
                          log_y=True
                         )
    
#-----------------------------------
#        Sunburst Graph
#----------------------------------    

    fig_sunburst = px.sunburst(merg2s,
                               color=heir_value_full,
                               values=geog,
                               # path=["continent","country"],
                               path=['Month',heir_value_full],
                               # hover_name="country", 
                               height=500,
                               width = 500,
                               color_discrete_sequence= graph_color
                              )
    
#-----------------------------------
#        Histogram Graph
#----------------------------------     
    fig_histo = px.histogram(merg2s,
                 x='Month',
                 y=geog,
                 color=heir_value_full,
                 # facet_col="continent",
                 # hover_name="country",
                 # marginal='rug'
                )
    fig_histo.update_yaxes(
                    autorange="reversed",  # bringing max values on top
                                
    ) 
    
#-------------------------------------
# Plotting Table Using Plotly Object
#--------------------------------------

# Colors schemes
# colors_antique=['#855C75','#D9AF6B','#AF6458','#736F4C','#526A83','#625377','#68855C','#9C9C5E','#A06177','#8C785D','#7C7C7C','#855C75','#D9AF6B','#AF6458','#736F4C']

    table = go.Figure(data=[go.Table(
                    columnorder=[0,1,2,3,4,5,6,7,8,9],
                    columnwidth=[cw1,cw2],                    #Setting Individual Column width of 1st column and all rest
                    header=dict(values=list(final1.columns),
                                align=['center'],
                                line_color='#f6f6f6',
                                
    #                             font_size=9
                               ),
                    cells=dict(values=final1.values.T,    # Transpose rows to column to fillcolor only the first column instead of rows
                    # Reference: https://stackoverflow.com/questions/61686382/change-the-text-color-of-cells-in-plotly-table-based-on-value-string
                               align=['center'],
    #                            font=dict(
    #                                     color='white',
    #                                     # color='black',
    # #                                   size=9
    #                                     ),
                               font=dict(color = ['#fff','black']), #Font color for first and next columns
                               line_color='#d1d1d1',   
                               # fill_color=[cmocean_ice,['white']],    # Color swatch for the table first column and white next column
                               fill_color=[tab_color,['white']], 
                              ) 
            )
                          ],
                      
    )
    
    table.update_layout(
        # font_color='white',  # Color of table headers
        # width=600,
        # height=500,
        # -----------------------------------------------------
        # Very important: These next 2 commands make the background 
        # of the plot transparent so that the overlaping next 
        # components (dropdown and input and their labels) can be visible!
        # Here opacity parameter, the last 0, is only important!!!
        #------------------------------------------------------------
        paper_bgcolor='rgba(1,1,1,0)',   
        plot_bgcolor='rgba(1,1,1,0)',
        margin=dict(l=0,r=0,t=0,) ,    # Remove left white space/margin
        # font_color=colors['text'],
        
     )
    
    if active_tab:
        if active_tab=="bar":
            fig=fig_bar
        elif active_tab== "line":   
            fig=fig_line 
        elif active_tab== "pie":   
            fig=fig_pie    
        elif active_tab== "sunburst":   
            fig=fig_sunburst  
        elif active_tab== "histogram":   
            fig=fig_histo 
        # elif active_tab== "scatter":   
        #     fig=fig_scat    
    
    return fig,table,kpi_value + " ( KPI ) for " + heir_value_full +'s' + " for markets on " + mbd_value + " Level" 
