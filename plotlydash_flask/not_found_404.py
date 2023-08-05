from dash import html
import dash

# the URI from where the dash application can be called
dash.register_page(__name__,
                    # path='/not-found-404',
                    # redirect_from=["/"]
                    )


layout = html.Span("")
