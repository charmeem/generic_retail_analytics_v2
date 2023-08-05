
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Connect to main app.py file
# from app import app
# from app import server
import dash_bootstrap_components as dbc

def create_dashboard(server):
    
    # Connect to your app pages
    # from apps.reports import report
    # from apps.plots import plot
        
    
    # meta_tags are required for the app layout to be mobile responsive
    dash_app = dash.Dash(
            server=server,
            # pages_folder='./plotlydash_flask/plotlydash/pages',
            pages_folder='.',
            # url_base_pathname='/',
            # routes_pathname_prefix="/dashapp/",
            # routes_pathname_prefix="/",
            use_pages=True,
            suppress_callback_exceptions=True,
            external_stylesheets=[dbc.themes.MINTY],
            meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}]
                    )   
        
    return dash_app.server    
