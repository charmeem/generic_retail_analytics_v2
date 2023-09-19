
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output

# Connect to main app.py file
# from app import app
# from app import server
import dash_bootstrap_components as dbc
import dash_auth

def init_dashboard(server):
    
    # Connect to your app pages
    # from apps.reports import report
    # from apps.plots import plot
        
    
    # meta_tags are required for the app layout to be mobile responsive
    app = dash.Dash(
            server=server,
            
            # pages_folder='./plotlydash_flask/plotlydash/pages',
            pages_folder='.',
            # url_base_pathname='/dashboard',
            routes_pathname_prefix='/',
            # routes_pathname_prefix="/",
            use_pages=True,
            suppress_callback_exceptions=True,
            external_stylesheets=[dbc.themes.MINTY],
            meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}]
                    )   
    
    

    # Initialize callbacks after our app is loaded
    # Pass dash app as a parameter
    init_callbacks(app)
        
    
    return app.server    


def init_callbacks(app):
    print('viewfunctions',app.server.view_functions)
    
    # # Basic Authentication of DASH
    # # Keep this out of source code repository - save in a file or a database
    # VALID_USERNAME_PASSWORD_PAIRS = {
    #     'hello': 'world'
    # }

    # auth = dash_auth.BasicAuth(
    #     app,
    #     VALID_USERNAME_PASSWORD_PAIRS
    # )
    
    # Connect to your app pages
    # from apps.reports import report
    # from apps.plots import plot
        
    

    #--------------------------------------------------------
    #                         TopBar
    #    This Section is creating a Multi component NAVBAR
    #--------------------------------------------------------

    EXPLAINER1 = """
                     Wew analyze and perform data cleaning and transformation of your raw data and present in the way you like on
                     a live dashboards. We work in close coperation with the research and Marketing team to develop
                     customized SW modules to generate Multi-dimentional heirarchical Tables for your business KPIs.
                     We integrate analytics and data science into your solutions, creating personalized
                     real-time dashboards that make managing business insights easier.             
                """
    EXPLAINER2 = """
                    This product is showcase of KPI reports and Graphes related to Merchandising Assortments and consists of various components of a data pipeline, 
                    each component is self-contained. 
                    The first component takes raw data and create multi level heirarchical tables for different KPIs. 
                    Output of these tables are used to create multi layer graphes used to derive businness insights.
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
    nav_link=dbc.NavItem(dbc.NavLink("Home",href="/dashboard",style={'paddingRight':'4rem'}))

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
                                dbc.Col(
                                    html.Img(
                                    src=app.get_asset_url('piesis_logo.jpg'),
                                    # src="plotlydash_flask/plotlydash/assets/piesis_logo.jpg",
                                    alt='Logo',
                                    height='80px')),
                                dbc.Col(dbc.NavbarBrand(html.H6("Data Analytics Multipage Dashboard for Retail Audit",
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
                             # dropdown2
                             ],
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


    # Creating jumbotron like style Component
    jumbotran = html.Div(
                    dbc.Container(
                        [
                            html.H1('Multipage Data Analytics Dashboard', className="display-3"),
                            html.H4(
                                "Welcome to our Demo Application, a showcase of some of the Data analytic services we offer",
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

    #----------------------------------------------------
    #        DASH LAYOUT COMPONENT
    #---------------------------------------------------


    #------------------------------
    # Styling the Clicked Button
    #------------------------------

    app.layout = html.Div([
                    dcc.Location(id='url', 
                                 refresh=False
                                ),
                    html.Div(id='page-content'),
                    dash.page_container
                    
                    ])

    # print("registry",dash.page_registry.values())

    index_page = dbc.Container([
                    html.Div([
                          html.Div(topbar),
                          jumbotran,
                          html.Div(
                                [                  
                                dcc.Link(dbc.Button(page["name"],type='button',className='btn-lg mx-5 my-5 border border-dark border-2'),href=page["relative_path"])     
                                for page in dash.page_registry.values()
                                if page["module"] != "..plotlydash.pages.not_found_404"
                                
                                # dcc.Link(dbc.Button('GOGI',type='button',className='btn-lg mx-5 my-5 border border-dark border-2'),href='/plotlydash/pages/report'),
                                ],
                                className = "d-flex justify-content-center"
                              )

                          # dash.page_container
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
                    if (page["name"] != "Generate KPI Reports") and (page["module"] != "..plotlydash.pages.not_found_404")
                    ],
                    className = "d-flex justify-content-center"
                  ),
              # html.Div(id='test'),
              # dash.page_container
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
                    
                        if (page["name"] != "Business Graphs") and (page["module"] != "..plotlydash.pages.not_found_404")
                    
                        # if page["module"] != "pages.not_found_404"
                ],
                className="d-flex justify-content-center "     #Align Buttons in a line in the center
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
                    
                        if (page["name"] != "View Reports") and (page["module"] != "..plotlydash.pages.not_found_404")
                    
                        # if page["module"] != "pages.not_found_404"
                ],
                className="d-flex justify-content-center "     #Align Buttons in a line in the center
              ),             
            
            # dash.page_container
            ]),
            
            ])


    @callback(
                  Output('page-content', 'children'),
                  Input('url', 'pathname')
                 )
    def display_page(pathname):
        
        if pathname == '/plotlydash/pages/report':
            return report_layout
        elif pathname == '/plotlydash/pages/plot':
            return plot_layout
        elif pathname == '/plotlydash/pages/table':
            return table_layout
        
        else:
            return index_page
        
    

    



