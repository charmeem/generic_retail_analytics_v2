"""Compile static assets."""
from flask import current_app as app
from flask_assets import Bundle


def compile_static_assets(assets):
    """
    Compile stylesheets if in development mode.
    :param assets: Flask-Assets Environment
    :type assets: Environment
    """
    assets.auto_build = True
    assets.debug = False
    
    # less_bundle = Bundle(
    #     "less/*.less",
    #     filters="less,cssmin",
    #     output="dist/css/styles.css",
    #     extra={"rel": "stylesheet/less"},
    # )
    # assets.register("less_all", less_bundle)
    
    style_bundle = Bundle(
        'src/less/*.less',
        filters='less,cssmin',
        output='dist/css/style.min.css',
        extra={'rel': 'stylesheet/css'}
        )
    
    js_bundle = Bundle(
        'src/js/main.js',
        filters='jsmin',
        output='dist/js/main.min.js'
        )
    
    # Register style bundle
    assets.register('main_styles', style_bundle)
    assets.register('main_js', js_bundle)
    
    
    if app.config["FLASK_ENV"] == "development":
        # Build LESS styles
        style_bundle.build()
        js_bundle.build()
        
    return assets

    