"""Application entry point."""
from plotlydash_flask import create_app  #__init__.py FILE
from config import Config

# app object is created in __init__.py file 
# where Flask object is created.
# create_app()
#
# __init__.py further embedd Dash object from dashboard.py file
# init_dashboard()

app = create_app(dash_debug=Config.dash_debug, dash_auto_reload=Config.dash_auto_reload)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
