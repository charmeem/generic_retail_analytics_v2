import pandas as pd
from datetime import datetime
import importlib
import os
import sys
import io
import dash
# import dash_core_components as dcc   #deprecated
from dash import dcc, html, callback_context, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64
import pathlib
# from app import app
from dash.exceptions import PreventUpdate
from pathlib import Path
from dash import register_page
import itertools


import helper
importlib.reload(helper)
import h_filter_brand_pcode
importlib.reload(h_filter_brand_pcode)
import kpis
importlib.reload(kpis)
import calculations
importlib.reload(calculations)
import get_report as get_report
importlib.reload(get_report)
import dash_config                        # Config file
importlib.reload(dash_config)


# import apps.reports.scripts.helper as helper
# importlib.reload(helper)
# import apps.reports.scripts.h_filter_brand_pcode as h_filter_brand_pcode
# importlib.reload(h_filter_brand_pcode)
# import apps.reports.scripts.kpis as kpis
# importlib.reload(kpis)
# import apps.reports.scripts.calculations as calculations
# importlib.reload(calculations)
# import apps.reports.scripts.get_report as get_report
# importlib.reload(get_report)


#--------------------------------------------------
#                MAIN PROGRAM
#--------------------------------------------------

register_page(__name__,order=0,name='Generate KPI Reports',path='/report')

# Input Raw data file
# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../dataset").resolve()


#-----------------------------------------------
#     Parsing Contents of input data file
#     into a secured variable
#------------------------------------------------

def parse_contents(contents,filename):
    
    content_type, content_string = contents.split(',')  # Removing the header part of the uploaded contents
    
    decoded = base64.b64decode(content_string)    # Converts binary/text into ASCII
    
    # Reading the copied text from Dash Uploaded component into dataframe
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            # df = pd.read_csv(io.StringIO(decoded.decode("unicode_escape")))
            df = pd.read_csv(io.StringIO(decoded.decode("ISO-8859-1")))  # Decoding ASCII back to binary/text
                
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print("error :",e)
        return html.Div([
            'There was an error processing this file.'
        ])
    
    return df
    
levels=10               #setting number of report levels
level_array = ['combo{}'.format(i+1) for i in range(levels)]       #Creating list 
level_array2 = ['combo{}_1'.format(i+1) for i in range(levels)]       #Creating list
level_array3 = ['combo{}_2'.format(i+1) for i in range(levels)]       #Creating list 

#Sample list
# ['combo1', 'combo2', 'combo3', 'combo4', 'combo5', 'combo6', 'combo7', 'combo8', 'combo9', 'combo10']

# -----------------------------------------------------------------
# Parsing console log to the Dash front end Method 1
# ----------------------------------------------------------------
# import logging

# class DashLoggerHandler(logging.StreamHandler):
#     def __init__(self):
#         logging.StreamHandler.__init__(self)
#         self.queue = []

#     def emit(self, record):
#         msg = self.format(record)
#         self.queue.append(msg)

# logger = logging.getLogger()
# # logger.setLevel(logging.WARNING)
# dashLoggerHandler = DashLoggerHandler()
# logger.addHandler(dashLoggerHandler)

# -----------------------------------------------------------------
# HOW TO OUTPUT PRINT COMMANDS ON THE SCREEN
#
# 1. We will create a log file and store print statements in by appending
# 2. Finaly we will read it and send output
# All is done in Main call back below
# ----------------------------------------------------------------

# f = open('out.txt', 'w')
# f.close()


# ----------------------------------------------------------------------
#                   Layout
# Initial Layout creates:
#  1. Upload component 
#  2. Spinner with emptyt Output component
#  3. Store df columns, heir columns and market columns in browser session 
#------------------------------------------------------------------------

button_style1 = {'background-color': '#FF9900',
                 'color':'black',
                 'width': '300px',
                 'border-color':'#e9ecef'
                 }

# Upload component
upload = html.Div(
    dcc.Upload(
                # html.Button('Select Input Data File'),
                dbc.Button('Select your own Data File',style=button_style1,className='btn-lg mx-2', disabled="true" ),
                id="input_data",
                # style={'padding':'10px'}
                disable_click=True
                 ),
            )

# Loading Spinner Component , tied with csv file loading and view for level attribute checklist via callback
spinner1 = dcc.Loading(
                id='spinner_1',
                type='default',
                children=html.Div(id='loading_output_1')
            )

# Loading Spinner Component , tied with log output in iframe- see Mian callback 
spinner2 = dcc.Loading(
                id='spinner_2',
                type='default',
                fullscreen='True',
                children=html.Iframe(id='console-out',srcDoc='',style={'width':'100%','height':400})
            )

# Creating jumbotron like style Component
jumbotron = html.Div(
                dbc.Container(
                    [
                        html.H1('Retail Audit KPI Reports Generator', className="display-3"),
                        html.H4(
                            " You can generate Multi level and Customized Heirarchical Tables for the Retail Audit KPIs ",
                            # "Build customize feature sets to generate desired KPIs using raw data as input",
                            className="lead",
                        ),
                        html.Hr(className="mt-2 mb-5"),
                        # html.P("KPI reports will be used to plot graphs to gain business insights"),
                        dbc.Row([
                            dbc.Col(dbc.Button('Use sample data',className='btn-lg mx-4',id='load_sample')), #Download and use sample data file
                            html.H6("OR"),
                            dbc.Col(upload) # Upload component to upload localy stored data file 
                            ],justify='center'),
                    ],
                    fluid=True,
                    className="py-3 text-center",
                ),
                className="p-3 mb-5 bg-light rounded-3",
            )

# Level reorts types and label header
# lreps = dbc.Card([
#                   dbc.CardHeader(dbc.Row([html.Div(id='lreport')])),           # Label header of Multiple reports
#                   dbc.CardBody(dbc.Row([html.Div(id='level_report',style={'margin-right':'2rem'})]))       # Multilple reports  checkboxes
#                  ])

lreps = dbc.Card([
                  dbc.Row([html.Div(id='lreport')]),                          # Label header of level_report
                  dbc.Row([html.Div(id='level_report')],className="mb-3")      # Multilple reports  checkboxes
                 ])
# Main layout
layout=  dbc.Container(
                [   
                    jumbotron,
                    dbc.Row([dbc.Col(
                        [
                            dbc.Row(spinner1, style={'margin-bottom':'3rem'}),
                            dbc.Row(lreps,id='lreprow',style={'display':'none'}),
                            dbc.Row(html.Div(id='gen_rep'))
                        ],
                           width=6),
                             dbc.Col([dbc.Row(html.Div(id='months_list', style={'margin-bottom':'3rem'})),
                                      dbc.Row(html.Div(id='facts_list', style={'margin-bottom':'3rem'})),
                                      dbc.Row(html.Div(id='market_list'))
                                     ],
                                     width=6)],
                            # justify='center',
                            className="mb-5"
                           ),
                    
                    # html.Div(id='market_report'),   #div for market report check list
                    
                    # html.Div(id='result1'),
                    
                    # Stores
                    dcc.Store(
                        id="df_columns"
                    ),
                    dcc.Store(
                        id="months_store"
                    ),
                    dcc.Store(
                        id="heir_col_store"
                    ),
                    dcc.Store(
                        id="market_col_store"
                    ),
                    dcc.Store(
                        id="level_reports_store"   # Not used
                    ),
                    
                    html.Div(id='errors'),      # Validation of input entries
                    
                    spinner2,
                    
                    html.Div(id='table'),
                    html.Hr(style={'color':'grey','marginBottom':'1rem'}),
                    html.Div("Disclaimer: The data presented in this demo is fictitious, similiarity to any actual data is mere conincidental.",
                             className="mb-4 small")
                    # dcc.Interval(id='interval1', interval=2 * 1000,n_intervals=0),
                    # html.P(id='div-out', children=''),
                    # html.Iframe(id='console-out',srcDoc='',style={'width':'100%','height':400})
                ],
                    # fluid=True,
                    
                )



# layout = html.Div(
#     [
#         html.P("Testing Data store"),
#         html.Div(id="table", children=[]),
        
#     ]
# )
# # This call back retreives dtaframe from browser store
# @callback(
#               Output('table','children'),  
#               Input('stored-dataframe','data'),            # Storing total df columns to the store
#              )

# def read_dataframe(data):  
#     if data is not None:
#         return (print(data.head))





# ----------------------------------------------------------------------
#               Call back 1
# 1. File reading
# 2. Outputs : Generate checklist for:
#               - levels selection
#               - Months Selection
#               - store df columns to be used in other callbacks
#               - storing months selected into store
#------------------------------------------------------------------------
 
@callback(
              Output('loading_output_1','children'),  # Level list Output linked to spinner html div
              Output('df_columns','data'),            # Storing total df columns to the store
              Output('months_store','data'),            # Storing months list to the store  
              Input('input_data','contents'),         # Upload component to load localy stored file
              Input('input_data','filename'),         # Input from loading dcc component
              Input('load_sample','n_clicks'),         # Loading sample from data folder
              # Input('stored-dataframe','data'),  
              prevent_initial_call=True  
             )

def create_heirarchy_checklist(list_of_contents,list_of_names,click):  
    
    if list_of_contents is not None:
        df = parse_contents(list_of_contents,list_of_names)
    elif click is not None:
        df = pd.read_csv('plotlydash_flask/demo1/dataset/sample/retail_gen_dash.csv')   
        
    # heircols = df.columns   #Storing df columns list into variable
    
    # Selecting Hardcoded columns instead from dash_config.py file
    
    # Cleaning, removing first column :"Unmmaed"
    # garbage = ["Unnamed"]        # List of columns to be removed
    
    # for i in garbage:
        # heircols = [x for x in heircols if i not in x]

    tmonths = df.Month.unique()   # Total months


    # Creating controls based on the df above
    levels = dbc.Card([
                    html.Div([
                            html.H5("Select the desired attributes:"),
                            dcc.Checklist(
                               id='heir_columns',
                               options=[{'label':v,'value':k} for k,v in dict(itertools.islice(dash_config.heircols.items(),0,4)).items()],
                               inline=True,
                               labelStyle={'margin-right':'2.3rem'} 
                               ),
                            dcc.Checklist(
                               id='heir_columns2',
                               options=[{'label':v,'value':k,'disabled':'True'} for k,v in dict(itertools.islice(dash_config.heircols.items(),4,9)).items()],
                               inline=True,
                               labelStyle={'margin-right':'2.3rem','color':'#e2e2e2'} 
                               ),
                            
                            ],
                            # className='mr-5'
                            )],
                    body=True,
                    )

    return [levels, dash_config.heircols,tmonths]

#-------------------------------------------------------
#       Callback 1-2 Creating Months checklist 
#----------------------------------------------------------
@callback(   
    Output('months_list', 'children'),    # Market checklist
    # Input('heir_columns', 'value')
    Input('months_store','data'),             # Reading months list from the Store
    )
def create_months_checklist(monthsl):
    if monthsl is not None:       
        monthc = dbc.Card([
                        html.Div([
                            html.H5("Select reporting Months:"),
                            dcc.Checklist(
                               id='months',
                               options=[{'label':m,'value':m} for m in monthsl],
                               inline=True,
                               labelStyle={'margin-right':'2rem'} 
                               )
                            ],
                            # className="m-2
                            )],
                        body=True,  # Generates card body with padding
                        )

        return monthc

#----------------------------------
# Callback 1-3 to generate FACTS list
#----------------------------------
@callback(   
    Output('facts_list', 'children'),    # facts checklist
    Input('heir_columns', 'value')
    # Input('months_store','data'),             # Reading months list from the Store , ! Just using it to trigger the list
    )
def create_facts_checklist(heir):  
    facts_card = dbc.Card([
                    html.Div([                            
                                html.H5("Select KPI Reports"),
                                dcc.Checklist(
                                    id='facts',
                                    options=[{'label':v,'value':k} for k,v in dict(itertools.islice(dash_config.facts.items(),0,4)).items()],
                                    inline=True,
                                    labelStyle={'margin-right':'2rem'}
                                ),
                                dcc.Checklist(
                                    id='facts2',
                                    options=[{'label':v,'value':k,'disabled':'True'} for k,v in dict(itertools.islice(dash_config.facts.items(),4,21)).items()],
                                    inline=True,
                                    labelStyle={'margin-right':'2rem','color':'#e2e2e2'}
                                ),
                            ])
                ],
                body=True,  # Generates card body with padding
                )
    
    return facts_card
    
# --------------------------------- --------------------------------------
#               Call back   2
#  Call back for Market checklst:
# 1. card2 =  Output component Market checklst 
# Here we have to do follow things:
# 1. To create market_list
# 2. Store the market_list check values to store and restored that in step 3
# 3. Get market_list previous values set and insert that ticks in the market_list layout
# NOTE: when heirarchy check list updated the market list recalculates but the previous checked values in market list IS LOST.
#       To cater this I have to get these values 'market_col_store' saved in store in callback 3 and retreived here !!! 
#-------------------------------------------------------------------------

@callback(   
    Output('market_list', 'children'),    # Market checklist
    Input('heir_columns', 'value'),
    Input('df_columns','data'),             # Reading total columns from the Store
    # Input('market_col_store', 'data'),  #Read checked values from market list and set it as values in Checklist below
    # prevent_initial_call=True
    )
def create_market_checklist(heir_cols,total_cols):
    # Calculate Market list by subtracting selected heirchy columns from the total columns
    
    if heir_cols == None:
        heir_cols=[]
    if total_cols == None:
        total_cols=[]  
        
    # market_list = [el for el in total_cols if el not in heir_cols]
    
    # Using hardcoded insted in this generic version from dash_config.py
       
        
    #MBD selected columns
    card2 = dbc.Card([
                        html.Div([
                                html.H5("Select Market Segments:"),
                                dcc.Checklist(
                                    # market_list,           # Label
                                    # market_list,   # Values
                                    id='market_columns',
                                    options=[{'label':b,'value':b} for b in dash_config.market_list[0:3]],
                                    inline=True,
                                    labelStyle={'margin-right':'2rem'} 
                                   ),
                                dcc.Checklist(
                                    # market_list,           # Label
                                    # market_list,   # Values
                                    id='market_columns2',
                                    options=[{'label':b,'value':b,'disabled':'True'} for b in dash_config.market_list[3:7]],
                                    inline=True,
                                    labelStyle={'margin-right':'2rem','color':'#e2e2e2'} 
                                   )
                                ],
                                # className="m-2
                                )],
                        body=True,)

    
                    
    #------------------------------------------------------------
    # Limiting the checked checkbox  == 10 
    # Method 2   easy one
    #------------------------------------------------------------
    if len(heir_cols) >= 11:
        return [html.Div([dbc.Alert("You can select upto 10 columns Only !", color="info"),
                          card2,
                          # cardfacts
                          ])]
                           
    return [html.Div([
                card2,
                # html.H6("Select multiple reports to be reported:(from Feature set #1)"), #The level report checklists will be rendered here
                # html.P("Generate multiple reports"),
                # html.Div(id='level_report'),                       
                ])]
        
        
#-----------------------------------------------
#   Call back 3
#   Generating dual Level reporting checklists
#-----------------------------------------------

@callback(   
    Output('level_report', 'children'),    # Level reports checklist
    Output('lreport','children'),          # Only Header/Label
    Output('lreprow','style'),             # changing display of this element to visible
    Output('gen_rep','children'),          # Button generates report
    Input('heir_columns', 'value'),
    prevent_initial_call=True
     )
def create_level_report_checklist(heir_cols):
    # header element 'lreport'
    if heir_cols is None:
        raise PreventUpdate
    else:
        header = html.Div(html.H6("Build hierarchical tree & generate simulteneous reports :") )
    
        # GENERATING MULTIPLE CHECKLISTS USING FOR LOOP
        lis=[]     
        # if not heir_cols is None:
        for t in level_array:
            lis.append(html.Div([   
                                    dcc.Checklist(id='{}_1'.format(t),options=[{'label':'{}'.format(t),'value':t}],
                                                  inline=True),
                                    dcc.Checklist(id='{}_2'.format(t),options=[{'label':h,'value':h} for h in heir_cols],
                                                  inline=True,style={'display':'none'}),
                                   ],
                                    )) 
        # IMPORTANT indentation: return when any of heir_cols checkbox is checked 
        return [lis,
                header,
                {'display':'block'},
                dbc.Button('Generate Reports',id='reportgen',className='mt-5 btn-lg'),
                ]
    
    
#---------------------------------
# OLD CODE
#---------------------------------

# @callback(   
#     Output('level_report', 'children'),    # Market checklist
#     Input('heir_columns', 'value'),
#     Input('level_store1','data')        # Read level reports checks from store 
#     # prevent_initial_call=True
#     )
# def create_level_report_checklist(heir_cols,type_checks1):
#     # Heirarchies to be selected for reporting - Total 12 
#     if heir_cols is None and type_checks1 is None:
#         heir_cols=[]
#         type_checks1=[]
#     card3 = dbc.Card([
#                         html.Div([
#                                 html.H6("Select Types of Levels to be reported:"),
#                                 html.P("Print multiple simultenous reports"),
#                                 dcc.Checklist(id='card3_1',options=[{'label':'Type1','value':'1'}],inline=True,value=type_checks1),
#                                 dcc.Checklist(id='card3_2',options=[{'label':i,'value':i} for i in heir_cols],inline=True,style={'display':'none'}),

#                                 dcc.Checklist(id='card4_1',options=[{'label':'Type2','value':'1'}],inline=True,value=[],),
#                                 dcc.Checklist(id='card4_2',options=[{'label':i,'value':i} for i in heir_cols],inline=True,style={'display':'none'}),

#                                 dcc.Checklist(id='card5_1',options=[{'label':'Type3','value':'1'}],inline=True,value=[],),
#                                 dcc.Checklist(id='card5_2',options=[{'label':i,'value':i} for i in heir_cols],inline=True,style={'display':'none'}),

#                                 dcc.Checklist(id='card6_1',options=[{'label':'Type4','value':'1'}],inline=True,value=[],),
#                                 dcc.Checklist(id='card6_2',options=[{'label':i,'value':i} for i in heir_cols],inline=True,style={'display':'none'}),

#                                 dcc.Checklist(id='card7_1',options=[{'label':'Type5','value':'1'}],inline=True,value=[],),
#                                 dcc.Checklist(id='card7_2',options=[{'label':i,'value':i} for i in heir_cols],inline=True,style={'display':'none'}),

#                                 dcc.Checklist(id='card8_1',options=[{'label':'Type6','value':'1'}],inline=True,value=[],),
#                                 dcc.Checklist(id='card8_2',options=[{'label':i,'value':i} for i in heir_cols],inline=True,style={'display':'none'}),

#                                 dcc.Checklist(id='card9_1',options=[{'label':'Type7','value':'1'}],inline=True,value=[],),
#                                 dcc.Checklist(id='card9_2',options=[{'label':i,'value':i} for i in heir_cols],inline=True,style={'display':'none'}),

#                                 dcc.Checklist(id='card10_1',options=[{'label':'Type8','value':'1'}],inline=True,value=[],),
#                                 dcc.Checklist(id='card10_2',options=[{'label':i,'value':i} for i in heir_cols],inline=True,style={'display':'none'}),
#                                 ],
#                                 # className="m-2
#                                 )],body=True,)
#     return [html.Div([
#                     card3
#                 ])]

    
    
#-----------------------------------------------
# Call back 4
# Limiting Market selection list to 10
# Rendering final MBD checklist
# INPUT trigger two way
# a. when heirarch checks changes in Last call back
# b. When market checks changes in THIS Callback
#--------------------------------------

@callback(   
    Output('market_report', 'children'),
    Output('market_col_store', 'data'),  # Store Market list checks values
    Input('heir_columns', 'value'),
    Input('market_columns','value'),
    # prevent_initial_call=True,
    )
def selecting_market_columns(heir,checks):
    # ctx = dash.callback_context
    # ctx_msg2 = json.dumps({
    #     'states': ctx.states,
    #     'triggered': ctx.triggered,
    #     'inputs': ctx.inputs,
    # }, indent=2)
    # print(ctx_msg2)
    
    if checks==None:
        checks_updated=[]
        #Render MBD list genereted from Market columns selected above
        # Heirarchies to be selected for reporting                    
        cardm = dbc.Card([
                            html.Div([
                                    html.H6("Select Markets to be reported: (Select from Feature set #2)"),
                                    html.Span("Markets: "),
                                    dcc.Checklist(
                                       id='cardm',
                                        options=[{'label':i,'value':i} for i in checks_updated],
                                        inline=True),
                                     
                                    ],
                                    
                                   ),
                             
                                      
                                ],
                            body=True,
                            )
   
        return ['',checks]
        
    else:    
        # Need to write a code that checks if the updated value of heir_col is already in 'checks' list, the market report list
        # if yes then 'check' must have that removed from its list
        # MEANS 'checlk' LIST IS CONTROLLED BY TWO INPUTS
        checks_updated = [el for el in checks if el not in heir]
        
        cardm = dbc.Card([
                            html.Div([
                                    html.H6("Select Markets to be reported:(from Feature set #2)"),
                                    html.Span("Markets: "),
                                    dcc.Checklist(
                                       id='cardm',
                                        options=[{'label':i,'value':i} for i in checks_updated],
                                        inline=True),
                                    html.Button(id='gen_rep',children="Generate Reports"),
                                        ], 
                                    
                                   )],
                            body=True,
                            )

        if len(checks_updated) >= 11:
                return [html.Div([dbc.Alert("You can select upto 10 markets Only !", color="info"),
                                  cardm]),
                                 checks_updated]    
    
        return [cardm,checks_updated]


#------------------------------------------------------
#                    Call back 5
#     for toggling level reports check boxes
#------------------------------------------------------

for l in level_array:    
    @callback([   
        Output('{}_2'.format(l), 'style'),
        Output('{}_1'.format(l), 'data'),
        Input('{}_1'.format(l), 'value'),
        Input('{}_2'.format(l), 'value'),
        ])
    def selecting_heirarchy_report2(control1,control2):   
        
        # Displaying or hiding the heirarchies selectors
        if control1:
            return [{'display':'block','color':'#989898'},control1]
        else:
            return [{'display':'none'},'']  

#--------------------------------------------------
# Clear  previous iframe
#-------------------------------------------------=
# @callback(
#     # Output('div-out','children'),
#     Output('console-out','style'),     # Rendering print messages in Iframe
#     Input('gen_rep','n_clicks')       # Button to generate reports
#     )
# def clear_iframe(n):
#     if n>1:
#         return ({'display':'none'})




#---------------------------------------------------
#  MAIN CALLBACK FOR REPORT GENERATION
#  FETCHING VARIABLES USED FOR REPORT GENERATION
#  Using access retail desktop scripts in q2py.py
#---------------------------------------------------

@callback(
    # Output('div-out','children'),
    Output('console-out','srcDoc'),     # Rendering print messages in Iframe
    Output('errors','children'),         # Validation checks
    Input('gen_rep','n_clicks'),        # Button to generate reports
    Input('input_data','contents'),         # Upload component to fetch again the data frame
    Input('input_data','filename'),         # Input from loading dcc component
    Input('load_sample','n_clicks'),         # Loading sample from data folder
    State('level_report','children'),  # level report
    State('market_columns','value'),
    State('months','value'),
    State('facts','value'),
    # Input('stored-dataframe','data')
    )

def generate_report(n_click,list_of_contents,list_of_names,sample_button,rep,market_array, months,kpia):
    
    if not market_array:
        return ['',html.H6('WARNING: So many missing inputs',className=' text-center text-danger')] 
    
    
    # Adding 'Mkt1' to the market_array as Mkt1 is 'Total' column
    market_array = ['Mkt1'] + market_array
    
    # Initiate log file so clear the old iframe log contents
    # If you want to accumulate log then take following code out of this callback
    f = open('out.txt', 'w')
    f.close()
        
    
    #------------------------------------------------------------------------
    # Using Callback context to fetch level reports check box's values 
    #
    # Search from the children the required level boxes checked
    #
    # value() function is used to check if value key exists in the dictionary
    #
    # IMPORTANT: .get() function is used with dictionaries to keep on ietrating for loop with missing keys.
    # https://stackoverflow.com/questions/63768189/python-how-to-deal-with-missing-keys-while-iterating-through-a-list-of-diction
    #-------------------------------------------------------------------------
    
    ctx = dash.callback_context
    
    #Type checked - Type1 e.g
    heirmain = [ctx.states["level_report.children"][n]["props"]["children"][0]["props"].get("value") for n,a in enumerate(level_array)]
    # levels within that type checked - Manufact e.g
    hlistmain = [ctx.states["level_report.children"][n]["props"]["children"][1]["props"].get("value") for n,a in enumerate(level_array)]
  
    
    # if hlistmain:
    #     print("hlistmain",hlistmain)
    #     print("hlist1",hlistmain[0])
    #     print("hlist2",hlistmain[1])
        
    # since tlits are list of lists we have to use double indeces'[][]' to get the element from that list    
    # print(tlist1[0][0])
    # print(tlist2[0][0])
    
    
    # Removing None elements from heirmain
    # hlistmain = list(filter(None,hlistmain))
    heirn = list(filter(None,heirmain))
    
    # Cretaing flat list only for types (heirarchies)
    heir = [heirn[a][0] for a,tlist in enumerate(heirn)]
    
    #-------------------------
    # Error handling
    # If any input missed
    #-------------------------
    # print(n_click,heir,market_array, months,kpia,hlistmain)
    
    if not months:
        return ['',html.H6('WARNING: Please select at least one month',className=' text-center text-danger')] 
    
    if not heir:
        return ['',html.H6('WARNING: Please select at least one report Type',className=' text-center text-danger')] 
    
    if len(market_array)<2:
        return ['',html.H6('WARNING: Please select at least one Market',className=' text-center text-danger')] 
    
    if not kpia:
        return ['',html.H6('WARNING: Please select at least one KPI above',className=' text-center text-danger')] 
    
    def checknone(hlistmain):
        res = True
        for i in hlistmain:
            if i :
                return False
        return res
    result = checknone(hlistmain)
    
    if result:
        return ['',html.H6('WARNING: Please select at least one level',className=' text-center text-danger')] 

    
    
    # flat_tlist2 = [tlistn2[a][0] for a,tlist in enumerate(tlistn2)]
    # tdict = [dict(zip(tlist1[n][0],tlist2[n][0])) for n,t in enumerate(tlist1)]
    
    #-------------------------------------------------------
    #  Starting q2py function routines
    #---------------------------------------------------------
    
    #------------------------------------------------------
    # Storing Print output in a log file to be later below
    # -----------------------------------------------------
    orig_stdout = sys.stdout
    
    f = open('out.txt', 'a')
    
    sys.stdout = f
    
    print(" Report Generation Started at ",datetime.today())
    
    sys.stdout = orig_stdout
    
    f.close()
    
    # Scaling facts - can be coded as UI controlled
    vol_fac = 1000000
    val_fac = 1000000
    
    
    # Fetching main df 
    if list_of_contents is not None:
        
        dbmi = parse_contents(list_of_contents,list_of_names)  
        
        # FILTER DB BASED ON MONTHS SELECTION
        dbm = dbmi[dbmi['Month'].isin(months)]
        
        # Applying scaling for sales volume and values
        dbm['Weights'] = dbm['Weights']/vol_fac
        
        dbm['Price'] = dbm['Price']/val_fac
     
    elif sample_button is not None:
        
        dbmi = pd.read_csv('plotlydash_flask/demo1/dataset/sample/retail_gen_dash.csv')
        
        # filter db based on months selection
        dbm = dbmi[dbmi['Month'].isin(months)]
            
        
        # Applying scaling for sales volume and values
        dbm['Weights'] = dbm['Weights']/vol_fac
        
        dbm['Price'] = dbm['Price']/val_fac
        
        
    for hr in heir:
        # make sure heirarchy as integer
        # hr=int(hr)
        
        #----------------------------------------------------    
        # CALLING hlistg FUNCTION
        #------------------------------------------------------
        hlist = helper.hlistg(hr,hlistmain)
        
        
        # 'Variant' column has blanks so converting it to nan
        # Another solution is to Manualy Fill NA in data
        # for h in hlist:
        #     dbm[h] = dbm[h].apply(str)
        # OR,    
        # if 'Variant' in hlist:
            # dbm['Variant'] = dbm['Variant'].apply(str)

        # To solve the values mismatch due to the name case mismatch convert first letter to Capital
        # Heirarchy part
        if hlist:
            for h in hlist:
                if h in dbm.columns:
                    if not dbm[h].isnull().all():
                        dbm[h] = dbm[h].str.title()

        #--------------------------------------------------            
        # Strip off 'Mkt1'
        # 'Mkt1' is symbolic name for 'Total' market
        # So its name can be removed
        #------------------------------------------------
        if 'Mkt1' in market_array:
            market_array2 = [string for string in market_array if string !='Mkt1']
        else:
            market_array2 = market_array

        for m in market_array2:
            if m in dbm.columns:
                if not dbm[m].isnull().all():
                    dbm[m] = dbm[m].str.upper()

        # Creating CS_Stock column
        dbm['CS_Stock'] = dbm['Stk1'] + dbm['Stk2']

        # Not using new sale calculation due to the mismatch in cigarettae volume/value results
        # dbm['Sale_new'] = dbm['OpeningStock']+dbm['Purchase']-dbm['Stk1']-dbm['Stk2']

        # For sales items kpi we will use fresh sales calculation
        for kpi in kpia:
            if not kpi == 'sales_items':
                dbm['Sale_new'] = dbm['Sale']

        # Calculate Total store Volume(projected volume) to be used in weighted handling calcs.
        dbm = helper.proj_vol(dbm)
        d=5


        #-------------------------------------------------------------------------
        # Generating individual kpi reports one by one
        #
        # We can later use linux script to merge the files to generate single file
        #--------------------------------------------------------------------------

        for kpi in kpia:
            if kpi == 'sale_price':
                # Fill blanks by zero as blanks does not add up in CS_stock calculations below, NOT FOR NUMERIC Handling
                dbm = dbm.fillna(0)

            #Always fetch originol db for every kpi calculations
            # Calling function to Calculate Kpis
            # Note This is only for handling KPIs

            if kpi in ['num_hand','wt_hand','oos_hand','ooswt','hih','stock_cover']:                                          # Refactor
                db=dbm

            # calculation formulas only for non handling kpi types.
            else:
                db = calculations.calcs(dbm,kpi)
                
                # Calling function to genertae new rounded base table
                if not kpi in ['ooscost','sppd','sales_items']:
                    if hlist:
                        #Refactor
                        db = helper.rounded_vol_db(db,d,kpi,hlist,market_array2)

                # Converting indeces into columns
                db=db.reset_index()

            if hlist:
                indexf = hlist
                # CALLING EXTERNAL FUNCTION 'get_report' 
                hchy = get_report.get_report_func(db,dbm,kpi,d,indexf,hr,market_array)

            # Calculating Shares KPIs
            if kpi in ['vol_share','val_share','purvol_share','stockvol_share','fwdstockvol_share','fwdstockvol_share','shareleg']:     #Refactor  
                hchy = hchy/hchy.iloc[0]*100
                # hchy = hchy.applymap(lambda x:round(x,d))


            # Generating csv output
            # Just changing the name of this kpi for printing and clarity
            if kpi == 'sale_price':
                kpi = 'price_pack'


            # Output the result
            # Check dash_config.py file
            Path('plotlydash_flask/demo1/logs/'+ dash_config.fold).mkdir(parents=True, exist_ok=True)
            
            # Appplying round method to all the columns
            hchy = hchy.applymap(lambda x:round(x,d))
            
            
            #------------------------------------------------------------------
            # Creating heirarchy based subfolder  e.g man, bra, man_flav
            # 
            # The log files will be stored in their respective folders
            # The plot.py will fetch these files based on the dropdown selection
            #
            # print("HLIST",hlist)  
            #  ['Brand', 'Vendor']
            #------------------------------------------------------------------
            
            # Selecting first 3 chars of hlist array and store into new array
            hfold=[]
            if hlist:
                for h in hlist:
                    h = h[:3]
                    hfold.append(h)
          
            # Join the elements to be used in directory creation and convert to lowercase
            hfold= "_".join(hfold).lower()
            
            # Creating subfolder as to_csv does not create the missing subfolders
            os.makedirs('plotlydash_flask/demo1/logs/'+ dash_config.fold + '/' + hfold,exist_ok=True)
            
            if kpi=='vol_abs':

                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Sales_Volume.csv'.format(dash_config.fold,hfold))

            if kpi=='val_abs':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Sales_Value.csv'.format(dash_config.fold,hfold))

            if kpi=='purvol_abs':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Purchase_Volume.csv'.format(dash_config.fold,hfold))

            if kpi=='stockvol_abs':
                hchy=hchy*10
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Stocks_Volume.csv'.format(dash_config.fold,hfold))

            if kpi=='fwdstockvol_abs':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Forward_Stocks_Volume.csv'.format(dash_config.fold,hfold))

            if kpi=='vol_share':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Volume_Share.csv'.format(dash_config.fold,hfold))

            if kpi=='val_share':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Value_Share.csv'.format(dash_config.fold,hfold))

            if kpi=='purvol_share':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Purchase_Volume_Share.csv'.format(dash_config.fold,hfold))

            if kpi=='stockvol_share':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Stock_Value_Share.csv'.format(dash_config.fold,hfold))

            if kpi=='fwdstockvol_share':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Forward_stock_volume_share.csv'.format(dash_config.fold,hfold))

            if kpi=='sales_items':
                # Values of this kpi needs to be in rounded off
                hchy = hchy.applymap(lambda x:round(x))
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Sales_Items.csv'.format(dash_config.fold,hfold))

            if kpi=='num_hand':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Numeric_distribution.csv'.format(dash_config.fold,hfold))

            if kpi=='wt_hand':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Weighted_handling.csv'.format(dash_config.fold,hfold))

            if kpi=='oos_hand':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/OOS_Numerical.csv'.format(dash_config.fold,hfold))

            if kpi=='ooswt':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/OOS_weighted.csv'.format(dash_config.fold,hfold))

            if kpi=='saleleg':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Sales_Volume_leg.csv'.format(dash_config.fold,hfold))

            if kpi=='shareleg':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Volume_share_Leg.csv'.format(dash_config.fold,hfold))

            if kpi=='hih':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Handling_in_handlers.csv'.format(dash_config.fold,hfold))

            if kpi=='sish':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/SISH.csv'.format(dash_config.fold,hfold))

            if kpi=='ooscost':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/COOS.csv'.format(dash_config.fold,hfold))

            if kpi=='sppd':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/SPPD.csv'.format(dash_config.fold,hfold))

            if kpi=='price_pack':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Retail_SP_Per_pack.csv'.format(dash_config.fold,hfold))
            if kpi=='price_stick':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Retail_SP_Per_unit.csv'.format(dash_config.fold,hfold))

            if kpi=='stock_cover':
                hchy.to_csv('plotlydash_flask/demo1/logs/{}/{}/Stocks_Cover_days.csv'.format(dash_config.fold,hfold))
            
            # Openeing log file to append the print statement
            orig_stdout = sys.stdout
            f = open('out.txt', 'a')
            sys.stdout = f
            print(kpi + "_" + hr + " Report Generated at ",datetime.today())
            sys.stdout = orig_stdout
            f.close()
            

            # Show reports finish message once done with all kpis
            if kpi==kpia[-1]:
                # Opening log file to append following print statements
                orig_stdout = sys.stdout
                f = open('out.txt', 'a')
                sys.stdout = f
                print(">>>>>>>")
                print("Reports Done")
                sys.stdout = orig_stdout
                f.close()
                
    
    # Openeing log file to READ and OUTPUT
    file = open('out.txt', 'r')
    data=''
    lines = file.readlines()
    if lines.__len__()<=120:
        last_lines=lines
    else:
        last_lines = lines[-120:]
    for line in last_lines:
        data=data + line + '<BR>'
    file.close()
        
    return [data, '']
    
    