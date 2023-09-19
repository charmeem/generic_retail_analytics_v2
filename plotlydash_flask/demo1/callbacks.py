from dash.dependencies import Input, Output
from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
# from models import User
from flask_login import current_user
import json
def register_callbacks(dash_app):
    
    print("babloo")
    # Callback function to login the user, or update the screen if the username or password are incorrect
    # DONOT NEED 
    # @dash_app.callback(
    #     Output('url_login', 'pathname'),
    #     Output('output-state', 'children'),
    #     [Input('login-button', 'n_clicks')], 
    #     [State('uname-box', 'value'),
    #      State('pwd-box', 'value')]
    #     )
    # def login_button_click(n_clicks, username, password):
    #     if n_clicks > 0:
    #         if username == 'test' and password == 'test':
    #             user = User(username)
    #             login_user(user)
    #             return '/success', ''
    #         else:
    #             return ['/login', 'Incorrect username or password']
    
    #------------------------------------------------------------------
    # It will check the user authentication status on every url change and
    # Stores the user id into Store session 
    #------------------------------------------------------------------
    @dash_app.callback(
        # Output('user-status-div', 'children'),  # I donot want to display the link 
        Output('login-status', 'data'),        #saving the user status in session store
        Input('url1', 'pathname'),
        
        )
    def login_status(url):
        print("url1",url)
        ''' callback to display login/logout link in the header '''
        
        if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated \
                and url != '/logout':  # If the URL is /logout, then the user is about to be logged out anyways
            
            return ( 
                # dcc.Link('logout', href='/logout'),
                # print("currentuser2",current_user.get_id()),
                current_user.get_id()
                    )
        else:
            return (
                # dcc.Link('login', href='/login'),
                'loggedout' 
                    )       
    
    #--------------------------------------------------------
    # Main Call back that display the landing page of Dash App
    # As well as code to control authentication
    #-----------------------------------------------------------
    @dash_app.callback(
                  Output('page-content', 'children'),    #These outputs linked to layout.py File
                  Output('redirect', 'pathname'),
                  Input('url1', 'pathname'),
                  
                 )
    def display_page(pathname):
        # print("callbackdemo1")
        ctx = dash.callback_context
        ctx_msg2 = json.dumps({
            'states': ctx.states,
            'triggered': ctx.triggered,
            'inputs': ctx.inputs,
        }, indent=2)
        print(ctx_msg2)
        
        #--------------------------------------------------------
        #                         TopBar
        #    This Section is creating a Multi component NAVBAR
        #--------------------------------------------------------
        
        EXPLAINER1 = """
                         We analyze and perform data cleaning and transformation of your raw data and present in the way you like on
                         a live dashboards. We work in close coperation with the research and Marketing team to develop
                         customized SW modules to generate Multi-dimentional heirarchical Tables for your business KPIs.
                         We integrate analytics and data science into your solutions, creating personalized
                         real-time dashboards that make managing business insights easier.             
                    """
        EXPLAINER2 = """
                        This product is showcase of KPI reports and Graphes related to Merchandising Assortments and consists of various components of a data pipeline, 
                        each component is self-contained. 
                        The first component takes raw data and create multi level heirarchical tables for different KPIs. 
                        Output of these tables are used to create multi layer graphes used to derive business insights.
                    """
        EXPLAINER3 = """
                        So Lets try !
                     """
        EXPLAINER4= """
                        In order to make profitable decisions around the products customers want, category managers and merchandisers need a quick way of analyzing 
                        the demand data.
                        They can use a retail dashboard to analyze the demand data by sales and profit margin performance 
                        by sub-categories, departments, or brands.
                    """
        # Navbar link Component
        
        nav_link=dbc.NavItem([
            dbc.NavLink("Home",href="/demo1/",external_link=True,style={'paddingRight':'3rem','display':'inline','color':'orange'}),
            dbc.NavLink("Logout",href="/app_1_raw_dash/logout/",external_link=True,style={'paddingRight':'3rem','display':'inline','color':'orange'}),
            # dbc.NavLink('User',href="#",style={'paddingRight':'3rem','display':'inline'})
            ], className="mt-1")
        # nav_link2=dbc.NavItem(dbc.NavLink("Logout",href="/app_1_raw_dash/logout/",external_link=True,style={'paddingRight':'4rem'}))

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
        simpletoggle = dbc.NavbarSimple(
                    nav_link,
                    # brand="NavbarSimple",
                    brand_href="#",
                    # className="ms-auto",
                    # color="primary",
                    # dark=True,
                )
        toggler = dbc.NavbarToggler(
                    id="navbar-toggler1", n_clicks=0
                    ), # Toggler option for responsive small screen
        dbc.Collapse(         
                                nav_link,
                                 # nav_link2,
                               className="ms-auto",
                               id="navbar_collapse1",
                               is_open=False,
                               navbar=True,
                            )
        # Main Navbar code
        topbar=dbc.Navbar(
                dbc.Container(
                    [
                    # html.A(            #Html A link enclosing logo
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Img(
                                    src=dash_app.get_asset_url('piesis_logo.jpg'),
                                    # src="plotlydash_flask/demo1/assets/piesis_logo.jpg",
                                    alt='Logo',
                                    height='80px')),
                                dbc.Col(dbc.NavbarBrand(html.H6("Data Analytics Tool + Dashboard for Retail Sector",
                                     className='mt-5'  # margin-top
                                    )))
                            ],
                            align="center",  #Vertical center
                            # className='g-0',  # Spacing between columns

                        ),
                        simpletoggle,
                        
                    ],
                    fluid=True  # Stretching the contents within containe to full page
                ),
        #         color="dark",
        #         dark=True,
                className="m-2 mb-5"

        )


        # Creating jumbotron like style Component
        jumbotran = html.Div(
                        dbc.Container(
                            [
                                html.H1('Welcome to Multipage Retail Data Analytics Tool', className="display-3"),
                                html.H4(
                                    "This is a Demo Application, a showcase of some of the Data analytic services we offer",
                                    className="lead",
                                ),
                                html.Hr(className="mt-2 mb-5"),
                                html.H6(EXPLAINER1),
                                html.P(EXPLAINER2) ,
                                html.H6(EXPLAINER3)
                            ],
                            # fluid=True,
                            className="py-3 text-center",
                        ),
                        className="p-3 mb-5 bg-light rounded-3",
                    )
        # Landing Page of Dash Application
        index_page = dbc.Container([
                        html.Div([
                              html.Div(topbar),
                              jumbotran,
                              html.Div(
                                    [                  
                                    dcc.Link(dbc.Button(page["name"],type='button',className='btn-lg mx-5 my-5 border border-dark border-2'),href=page["relative_path"])     
                                    for page in dash.page_registry.values()
                                    if page["name"] != "Not found 404"                                
                                    # dcc.Link(dbc.Button('GOGI',type='button',className='btn-lg mx-5 my-5 border border-dark border-2'),href='/demo1/pages/report'),
                                    ],
                                    className = "d-md-flex justify-content-center"
                                    #Align Buttons in a line in the center
                                    # NOTE: md is important to set responviness for the samll and medium screens
                                  )
                            ])
                
                ])
        # html.H1("Data Analytics Dashboard",className='mt-3'),
        # dcc.Markdown(EXPLAINER),

        # Creatings Reports                
        report_layout = dbc.Container([
                        html.Div([
                              html.Div(topbar),
                              html.Div([                  
                                    dcc.Link(dbc.Button(page["name"],type='button',className='btn-lg mx-5 my-5 border border-dark border-2'),href=page["relative_path"])     
                                    for page in dash.page_registry.values()
                                    if (page["name"] != "Generate KPI Reports") and (page["name"] != "Not found 404")
                                    ],
                                    className = "d-md-flex justify-content-center"
                                    #Align Buttons in a line in the center
                                    # NOTE: md is important to set responviness for the samll and medium screens
                                  ),
                              
                            ]),
                            
                            ])


        #Graphs
        plot_layout = dbc.Container([
            html.Div([
                html.Div(topbar),
                  html.Div(
                          
                    # html.H1("Data Analytics Dashboard",className='mt-3'),
                    # dcc.Markdown(EXPLAINER),
                    [
                    dcc.Link(dbc.Button(page["name"],type='button',className='btn-lg mx-5 my-5 border border-dark border-2'),href=page["relative_path"])     
                            for page in dash.page_registry.values()
                        
                            if (page["name"] != "Business Graphs") and (page["name"] != "Not found 404")
                        
                            # if page["module"] != "pages.not_found_404"
                    ],
                    className="d-md-flex justify-content-center "     
                    #Align Buttons in a line in the center
                    # NOTE: md is important to set responviness for the samll and medium screens
                  ),             
                
                # dash.page_container
                ]),
                
                ])

        # Report Views
        table_layout = dbc.Container([
            html.Div([
                html.Div(topbar),
                  html.Div(
                          
                    # html.H1("Data Analytics Dashboard",className='mt-3'),
                    # dcc.Markdown(EXPLAINER),
                    [
                    dcc.Link(dbc.Button(page["name"],type='button' ,className='btn-lg mx-5 my-5 border border-dark border-2'),href=page["relative_path"])     
                            for page in dash.page_registry.values()
                            if (page["name"] != "View Reports") and (page["name"] != "Not found 404")
                        
                            # if page["module"] != "pages.not_found_404"
                    ],
                    className="d-md-flex justify-content-center "     
                    #Align Buttons in a line in the center
                    # NOTE: md is important to set responviness for the samll and medium screens
                  ),             
              
                ]),
                
                ])

        # Dash applies validation to your callbacks through validation_layout function,
        # which performs checks:
        # such as validating the types of callback arguments and checking to see whether 
        # the specified Input and Output components actually have the specified properties.
        dash_app.validation_layout = html.Div([
            index_page,
            report_layout,
            plot_layout,
            table_layout,
        ])
        
        ''' callback to determine layout to return '''
        # We need to determine two things for everytime the user navigates:
        # Can they access this page? If so, we just return the view
        # Otherwise, if they need to be authenticated first, we need to redirect them to the login page
        # So we have two outputs, the first is which view we'll return
        # The second one is a redirection to another page is needed
        # In most cases, we won't need to redirect. Instead of having to return two variables everytime in the if statement
        # We setup the defaults at the beginning, with redirect to dash.no_update; which simply means, just keep the requested url
        view = None
        url = dash.no_update
        #-----------------------------------------------
        # DONT need the following codes at the moment
        #--------------------------------------------
        # if pathname == '/login':
        #     view = login
        # elif pathname == '/success':
        #     if current_user.is_authenticated:
        #         view = success
        #     else:
        #         view = failed
        # elif pathname == '/logout':
        #     if current_user.is_authenticated:
        #         logout_user()
        #         view = logout
        #     else:
        #         view = login
        #         url = '/login'
        #---------------------------------------------
            
        # Authentication of direct login of these pages DONE IN FLASK routes.py       
        if pathname == '/demo1/report':
            print("googiii",pathname)
            view=report_layout
        elif pathname == '/demo1/plot':
            view=plot_layout
        elif pathname == '/demo1/table':
            view=table_layout
        
        #Authenticatiion of the Main landing page of Dash App is done here 
        # As it was not possible for me to do that in FLASK
        elif pathname == '/demo1/':
            if current_user.is_authenticated:
                view = index_page
            else:
                view = ''
                url = '/login'
        
        return view,url    
    
