import pandas as pd
import numpy as np
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server
import dash_bootstrap_components as dbc

# Connect to your app pages
from apps.reports import report
from apps.plots import plot
import base64
import csv
import io

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



#--------------------------------------------------------
#                         TopBar
#    This Section is creating a Multi component NAVBAR
#--------------------------------------------------------

EXPLAINER = """
                WWelcome to our Demo Application that is showcase of some of the Data analytic services we offer.
                
                Take your data business to the next level by choosing latest technolgy.
                
                We arrange, analyze, manage your raw data and present in the way you like on a live dashboards.

                We work in close coperation with the research and Marketing team to develop customized
                SW modules to generate Multi-dimentional/heirarchical Tables for your business KPIs.
                
                We integrate analytics and data science into your solutions, creating personalized
                real-time dashboards that make    managing   business insights easier
                
                This product consists of various components of a data pipeline, each component is self-contained.
                The first component takes raw data and create multi level heirarchical tables for different KPIs.
                Output of these tables are used to create multi layer graphes used to derive businness insights. 
                
               
            """

# Navbar link Component
nav_link=dbc.NavItem(dbc.NavLink("Home",href="#"))

# Dropdown component1
# dropdown1=dbc.DropdownMenu(
#             children=[
#                 dbc.DropdownMenuItem("Report Menu 1"),
#                 dbc.DropdownMenuItem("Report Menu 2"),
#                 dbc.DropdownMenuItem("Report Menu 3"),
#             ],
#             nav=True,
#             label="Reports",
#             in_navbar=True,
#             )

# Dropdown component2
dropdown2=dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Setting Menu 1"),
                dbc.DropdownMenuItem("Setting Menu 2"),
                dbc.DropdownMenuItem("Setting Menu 3"),
            ],
            nav=True,
            label="Settings",
            in_navbar=True,
            )

# Main Navbar code
topbar=dbc.Navbar(
        dbc.Container(
            [
                html.A(            #Html A link enclosing logo
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=app.get_asset_url('piesis_logo.jpg'),height='80px')),
                            dbc.Col(dbc.NavbarBrand(html.H6("Data Analytics Dashboard for Retail Audit",
                                                    className='mt-5'  # margin-top
                                                   )))
                        ],
                        align="center",  #Vertical center
                        # className='g-0',  # Spacing between columns

                    ),
                    href="http://www.letzgetmoving.com",
                    style={"textDecoration": "none"},    
                ),
                dbc.NavbarToggler(id="navbar-toggler1", n_clicks=0), # Toggler option for responsive small screen
                dbc.Collapse(                                        # Option to be used with toggler above for small screens
                    dbc.Nav(                                         # Creating navigation elements           
                        [nav_link,
                         # dropdown1,
                         dropdown2],
                        className="ms-auto",
                        navbar=True
                    ),
                    id="navbar_collapse1",
                    navbar=True
                )
            ],
            fluid=True  # Stretching the contents within containe to full page
        ),
#         color="dark",
#         dark=True,
        className="m-2 mb-5"

)

# Upload component for data file input
upload = html.Div(
    dcc.Upload(
                html.Button('Select Input Data File'),
                id="input_data",
                style={'padding':'10px'}
                 ),
            )

# Loading Spinner Component , tied with level attribute checklist via callback
# spinner1 = dcc.Loading(
#                 id='spinner_1',
#                 type='default',
#                 children=html.Div(id='stored-dataframe')
#             )


# Creating jumbotron like style Component
jumbotran = html.Div(
                dbc.Container(
                    [
                        html.H1('SW for Data Analytics', className="display-3"),
                        html.H4(
                            "Welcome to our Demo Application that is showcase of some of the Data analytic services we offer",
                            className="lead",
                        ),
                        html.Hr(className="mt-2 mb-5"),
                        html.H6(
                            " Take your data business to the next level by choosing latest technolgy.                                                         We arrange, analyze, manage your raw data and present in the way you like on                                                     a live dashboards. We work in close coperation with the research and Marketing team to develop                                     customized SW modules to generate Multi-dimentional heirarchical Tables for your business KPIs.                                   We integrate analytics and data science into your solutions, creating personalized                                               real-time dashboards that make    managing   business insights easier ",
                             
                        ),  
                        
                        # upload,
                    ],
                    # fluid=True,
                    className="py-3 text-center",
                ),
                className="p-3 mb-5 bg-light rounded-3",
            )

#----------------------------------------------------
#        DASH LAYOUT COMPONENT
#---------------------------------------------------


#------------------------------
# Styling the Clicked Button
#------------------------------

button_style1 = {'background-color': '#cbf3f0',
                 'color':'black',
                 'width': '200px',
                 'border-color':'#e9ecef'
                 }



app.layout = html.Div([
                dcc.Location(id='url', refresh=False),
                html.Div(id='page-content')
                ])
                

index_page = dbc.Container([
    html.Div([
        html.Div(topbar),
        html.Div([      
            # html.H1("Data Analytics Dashboard",className='mt-3'),
            # dcc.Markdown(EXPLAINER),
            
            dcc.Link(dbc.Button('Overview',style=button_style1,
                                className='btn-lg mx-5 my-5'
                               ),       
                     href='/apps/plots/plot'),
            dcc.Link(dbc.Button('Reports',style=button_style1, className='btn-lg mx-5 my-5'),       
                     href='/apps/reports/report'),
            dcc.Link(dbc.Button("Graphes",style=button_style1, className='btn-lg mx-5 my-5'),       
                     href='/apps/plots/plot'),
            ],
            className="d-flex justify-content-center "),             #Align Buttons in a line in the center
        
        jumbotran,  
        html.Div(id='hello')
        ]),
        
        ]
   )



page_1_layout =dbc.Container(
                    html.Div([
                        html.Div(topbar),
                        html.Div([      
                            dcc.Link(dbc.Button('Overview',style=button_style1,
                                                className='btn-lg mx-5 my-5'
                                               ),       
                                     href='/apps/plots/plot'),
                            
                            dcc.Link(dbc.Button("Graphes",style=button_style1, className='btn-lg mx-5 my-5'),       
                                     href='/apps/plots/plot'),
                            
                            dcc.Link(dbc.Button('Home',style=button_style1, className='btn-lg mx-5 my-5'),       
                                     href='/'),
                            ],
                            className="d-flex justify-content-center "),             #Align Buttons in a line in the center
                            
                            report.layout
                            
                        ])
                   )
                 

page_2_layout = dbc.Container(
                    html.Div([
                        html.Div(topbar),
                        html.Div([      
                            dcc.Link(dbc.Button('Overview',style=button_style1,
                                                className='btn-lg mx-5 my-5'
                                               ),       
                                     href='/apps/plots/plot'),
                            dcc.Link(dbc.Button('Reports',style=button_style1, className='btn-lg mx-5 my-5'),       
                                     href='/apps/reports/report'),
                            dcc.Link(dbc.Button("Home",style=button_style1, className='btn-lg mx-5 my-5'),       
                                     href='/'),
                            ],
                            className="d-flex justify-content-center "),             #Align Buttons in a line in the center
                            
                            plot.layout
                            
                        ])
                   )


    
@app.callback(
              Output('page-content', 'children'),
              Input('url', 'pathname')
             )
def display_page(pathname):
    if pathname == '/apps/plots/plot':
        return page_2_layout
    if pathname == '/apps/reports/report':
        return page_1_layout
    else:
        return index_page


# This call back manages to load, parse and store the datframe into browser store
@app.callback(
              Output('hello','children'),            # Storing total df columns to the store
              # Input('input_data','contents'),         # Upload component
              # Input('input_data','filename'),         # Input from loading dcc component
              Input('stored-dataframe','data'),
              prevent_initial_call=True  
             )

def store_dataframe(df):  
    # if list_of_contents is not None:
    #     df = parse_contents(list_of_contents,list_of_names) 
    print(df.head())
#     df = df.to_dict()  # convert df to dict inorder to store into data Store

#     dcc.Store(id="stored-dataframe",data=df),    # Storing DF
    return df

if __name__ == '__main__':
    app.run_server(debug=False)
