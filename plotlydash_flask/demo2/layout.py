import dash
from dash import dcc, html
 
#------------------------------
 # Styling the Clicked Button
 #------------------------------

# layout = html.Div([
#                 dcc.Location(id='url', refresh=True),
#                 html.Div(id='page-content'),
#                 dash.page_container
                
#                 ])

layout = html.Div([
    
    dcc.Location(id='url2', refresh=False),
    dcc.Location(id='redirect2', refresh=True),
    dcc.Store(id='login-status2', storage_type='session'),
    # html.Div(id='user-status-div'),
    # html.Br(),
    # html.Hr(),
    # html.Br(),
    html.Div(id='page-content2'),
    dash.page_container           # The output of our pages will be shown here. ref. 3 in design.txt
])

# print("LAYOUT2",layout)