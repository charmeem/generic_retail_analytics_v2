import dash
from dash import dcc, html
import dash_bootstrap_components as dbc


layout = html.Div([
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
                                    height='80px',
                                    className="rounded-circle"  # Add rounded image
                                ),
                                width=2  # Adjust column width for logo
                            ),
                            dbc.Col(
                                dbc.NavbarBrand(
                                    html.H6(
                                        "PieSis Tools",
                                        className='mt-5',  # margin-top
                                        style={'color': 'white'}
                                    )
                                ),
                                width=10  # Adjust column width for brand name
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
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Input(
                                    placeholder="Enter keyword and press Search button",
                                    type="search",
                                    id="search-input",
                                    style={'width': '60%', 'margin-right': '1rem'}
                                ),
                                dbc.Button(
                                    "Search",
                                    id="search-button",
                                    className="btn btn-primary",  # Use Bootstrap button class
                                    style={'margin-right': '1rem'}
                                ),
                            ],
                            className="d-flex justify-content-center",  # Centered input and button
                            width=8  # Adjust column width for search bar
                        )
                    ],
                    className="mt-5"
                ),
            ],
            className="mt-5",
            fluid=True
        )
    ],
        className="mt-5"  # Add spacing below the navbar
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)