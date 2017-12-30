# Welcome to the Flask-Bootstrap sample application. This will give you a
# guided tour around creating an application using Flask-Bootstrap.
#
# To run this application yourself, please install its requirements first:
#
#   $ pip install -r sample_app/requirements.txt
#
# Then, you can actually run the application.
#
#   $ flask --app=sample_app dev
#
# Afterwards, point your browser to http://localhost:5000, then check out the
# source.
import babel

from flask import Flask
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap

from .frontend import frontend
from .nav import nav


def format_datetime(value, format='medium'):
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format="y/MM/dd HH:mm"
    return babel.dates.format_datetime(value, format)


def iota_explorer(value):
    return f'https://thetangle.org/transaction/{value}'


def create_app(configfile=None):
    # We are using the "Application Factory"-pattern here, which is described
    # in detail inside the Flask docs:
    # http://flask.pocoo.org/docs/patterns/appfactories/

    app = Flask(__name__)

    # We use Flask-Appconfig here, but this is not a requirement
    AppConfig(app)

    # Install our Bootstrap extension
    Bootstrap(app)

    # Our application uses blueprints as well; these go well with the
    # application factory. We already imported the blueprint, now we just need
    # to register it:
    app.register_blueprint(frontend)

    # Because we're security-conscious developers, we also hard-code disabling
    # the CDN support (this might become a default in later versions):
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

    # We initialize the navigation as well
    nav.init_app(app)

    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['iota_explorer'] = iota_explorer

    return app

if __name__ == '__main__':
    app = create_app()
