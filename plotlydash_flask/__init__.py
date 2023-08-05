"""Initialize Flask app."""
from flask import Flask
from dash import Dash
from flask_assets import Environment
import dash_bootstrap_components as dbc
from os import getpid
import sys
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

#--------------------------------------------------------------------------
# Importing supporting scripts
# import scripts
# Use sys.path to make importing easier
# Just add the paths to sys.path and system will search the module automaticaly
# See lazy_pandas for more detail
#---------------------------------------------------------------------------
sys.path.append('plotlydash_flask')
sys.path.append('plotlydash_flask/demo1/')
sys.path.append('plotlydash_flask/demo1/apps/reports/scripts')



def create_app(dash_debug, dash_auto_reload):
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    
    # Using a production configuration
    # app.config.from_object('config.ProdConfig')
    
    # Using a development configuration
    app.config.from_object('config.Config')
    
    #INitializing mail object for mail sending from Contact form
    # mail = Mail(app)
    
    # register all dash apps
    # Callbacks and layouts are organized into seperate files
    # For detail explanation See link in Design.py Reference 1 & 6, also stored as a web file in learning/flask/
    #
    # FIRST DASH APP
    from layout import layout as app_1_layout
    from callbacks import register_callbacks as app_1_callbacks
    # Create Dash app 1 'demo1' within Flask object
    register_dash_app(
        flask_server=app,
        title='App 1',
        base_pathname='demo1',
        layout=app_1_layout,
        register_callbacks_funcs=[app_1_callbacks],
        dash_debug=dash_debug,
        dash_auto_reload=dash_auto_reload
    )
    
    # SECOND DASH APP
    # from layout2 import layout as app_2_layout
    # from callbacks2 import register_callbacks as app_2_callbacks
    
    # Create Dash app 2 'demo2' within Flask object
    # register_dash_app(
    #     flask_server=app,
    #     title='App 2',
    #     base_pathname='demo2',
    #     layout=app_2_layout,
    #     register_callbacks_funcs=[app_2_callbacks],
    #     dash_debug=dash_debug,
    #     dash_auto_reload=dash_auto_reload
    # )
    
    
    #Calling register_extensions functions 
    # like db, mail, login related codes
    register_extensions(app)
    
    # Calling blueprint register function defined below
    register_blueprints(app)

        
    # if running on gunicorn with multiple workers this message should print once for each worker if preload_app is set to False
    print(f'Flask With Dash Apps Built Successfully with PID {str(getpid())}.')
    
    return app
    
def register_dash_app(flask_server, title, base_pathname, layout, register_callbacks_funcs, dash_debug, dash_auto_reload):
    
    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}
    
    # Creating Dash object within Flask server
    my_dash_app = Dash(
        __name__,
        server=flask_server,
        # url_base_pathname=f'/{base_pathname}/',
        # requests_pathname_prefix=f'/{base_pathname}/',
        routes_pathname_prefix=f'/{base_pathname}/',
        # assets_folder=get_root_path(__name__) + '/static/',
        meta_tags=[meta_viewport],
        pages_folder='.',
        use_pages=True,                          #Allow to build multipages app, see pages folder
        suppress_callback_exceptions=True,
        external_stylesheets=[dbc.themes.MINTY],
    )
    
    #Following Flask Factory Patteren
    with flask_server.app_context():
        my_dash_app.title = title
        my_dash_app.layout = layout
        my_dash_app.css.config.serve_locally = True
        my_dash_app.enable_dev_tools(debug=dash_debug,dev_tools_hot_reload=dash_auto_reload )
        
        #Calling callback functions in main callback.py file
        # This will create landing page of our Dash app
        for call_back_func in register_callbacks_funcs:
            call_back_func(my_dash_app)
              

        # Compile CSS  
        # NOT USING CURRENTLY MIGHT BE LATER
        # compile_static_assets(assets)

# Register extensions
# Through this function the objects are initialized and can be used Globaly in our app like in routes.py file
def register_extensions(app):
    from extensions import db,login_manager,mail
    # from models import db, User
    
    # from plotlydash_flask.extensions import db
    # from plotlydash_flask.extensions import login_manager
    # from plotlydash_flask.extensions import mail
    from os import environ
    
    assets = Environment() 
    
    assets.init_app(app)           # assets initialization
    
    db.init_app(app)               # db initialization
    
    login_manager.init_app(app)    # login initialization
    
    login_manager.login_view = '/login'   # seems having no effect on login
    
    # Update Mail related Config parameters to avaoid error
    app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER=environ.get("MAIL_SERVER"),
    MAIL_PORT = environ.get("MAIL_PORT"),
    MAIL_USERNAME = environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD"),
    # MAIL_USE_TLS = environ.get("MAIL_USE_TLS"),  #NOT WORKING
    # MAIL_USE_SSL = environ.get("MAIL_USE_SSL"),  #NOT WORKING
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,    
    )) 
    mail.init_app(app)               # Email initialization for contact form send email function
    
    #----------------------------------------
    # Flask-Admin
    #----------------------------------------
    # # set optional bootswatch theme
    # app.config['FLASK_ADMIN_SWATCH'] = 'Cosmo'                       #https://bootswatch.com/3/    
    # admin = Admin(app, name='microblog', template_mode='bootstrap3')
    
    # # Add administrative views here
    # admin.add_view(ModelView(User, db.session))
    # # admin.add_view(ModelView(Post, db.session))
    
    #------------------------------------------------

    # Registers a function to be run BEFORE THE FIRST REQUEST to this instance of the application
    # Without this the DATABASE was not creating
    @app.before_first_request
    def create_tables():
        db.create_all()   # Create sql tables for our data models
    
    # Old method NOT WORKING
    # with app.app_context():
    #     db.create_all()  # Create sql tables for our data models
    
    
# Register Blueprints
def register_blueprints(app):
    import routes
    import auth
    
    app.register_blueprint(routes.main_bp)  # main Application routes
    app.register_blueprint(auth.auth_bp)    # User authentication routes
    


