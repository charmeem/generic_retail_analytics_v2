import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

            
EXPLAINER1 = """
                 This tool takes MP4 video files as an Input and converts them to Audio MP3 format
                 This also automaticaly create subfolders and put all the files in their respective folders 
            """            
            
# Creating jumbotron like style Component
jumbotran = html.Div(
                dbc.Container(
                    [
                        html.H1('MP4 to MP3 Convertor', className="display-3 mt-5"),
                        # html.H4(
                        #     "This is a Demo Application, a showcase of some of the Data analytic services we offer",
                        #     className="lead",
                        # ),
                        html.Hr(className="mt-2 mb-5"),
                        html.H6(EXPLAINER1),
                        
                    ],
                    # fluid=True,
                    className="py-3 text-center",
                ),
                className="p-3 mb-5 bg-light rounded-3",
            )


layout =  html.Div(
                [
                    dbc.Navbar(
                        dbc.Container(
                            [
                                html.A(  # HTML A link enclosing logo
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Img(
                                                    src="assets/piesis_logo.jpg",
                                                    alt='Logo',
                                                    height = "120rem",
                                                    className="rounded-circle"  # Add rounded image
                                                ),
                                                width=6,  # Adjust column width for logo
                                                className="d-flex justify-content-end"  # Align logo to the right
                                            ),
                                            dbc.Col(
                                                dbc.NavbarBrand(
                                                    html.H6(
                                                        "PieSis Tools",
                                                        className='mt-5',  # margin-top
                                                        style={'color': 'white'}
                                                    )
                                                ),
                                                width=6  # Adjust column width for brand name
                                            )
                                        ],
                                        align="center",  # Vertical center
                                    ),
                                    className="navbar-brand"  # Add navbar-brand class
                                ),
                                dbc.Row(
                                    [
                                        dbc.NavItem(
                                            [
                                                dbc.NavLink(
                                                    "MP4-Mp3 Convertor",
                                                    href="/demo3/",
                                                    external_link=True,
                                                    style={'paddingRight': '3rem', 'display': 'inline', 'color': 'white'}
                                                ),
                                                dbc.NavLink(
                                                    "Home",
                                                    href="/demo3/",
                                                    external_link=True,
                                                    style={'paddingRight': '3rem', 'display': 'inline', 'color': 'white'}
                                                ),
                                                dbc.NavLink(
                                                    "Logout",
                                                    href="/app_3_raw_dash/logout/",
                                                    external_link=True,
                                                    style={"display": "inline", "color": "white"}
                                                ),
                                            ],
                                            className="mt-1",
                                        )
                                    ],
                                    justify="between",  # Align items horizontally between start and end of container
                                ),
                            ],
                            fluid=True  # Stretching the contents within containe to full page
                        ),
                        color="primary",  # Set navbar background color
                        dark=True  # Set navbar text color to white
                    ),

                    dcc.Location(id='url3', refresh=False),
                    dcc.Location(id='redirect3', refresh=True),
                    dcc.Store(id='login-status3', storage_type='session'),
                    html.Div(id='page-content3'),   # main  page callback output
                    
                    html.Div([
                          
                          jumbotran,
                          html.Div(
                                [                  
                                dbc.Input(
                                    placeholder="Enter folder name where MP4 files stored",
                                    type="text",
                                    id="base_folder",
                                    style={'width': '60%', 'margin-right': '1rem', 'fontSize': '20px', 'padding': '15px'}
                                ),
                                dbc.Button(
                                    "Convert",
                                    id="convert-button",
                                    className="btn convert-button ",  # Use Bootstrap button class
                                    style={'margin-right': '1rem', 'fontSize': '20px'}
                                ),
                                ],
                                className = "d-md-flex justify-content-center"
                                #Align Buttons in a line in the center
                                # NOTE: md is important to set responviness for the samll and medium screens
                              )
                        ])
                   
                ]
            )


    
    # ])

