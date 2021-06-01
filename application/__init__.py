# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import logging
from logging import FileHandler, Formatter
import dateutil.parser
import babel.dates
from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

# Globally accessible libraries
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()


def init_app():
    app = Flask(__name__)
    app.config.from_object('config')

    # initialize plugins
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    with app.app_context():
        app.jinja_env.filters['datetime'] = format_datetime
        from application.models import artist, venue
        from application import routes

        if not app.debug:
            file_handler = FileHandler('error.log')
            file_handler.setFormatter(
                Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
            )
            app.logger.setLevel(logging.INFO)
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.info('errors')

        return app


# TODO: connect to a local postgresql database


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, date_format='medium'):
    date = dateutil.parser.parse(value)
    if date_format == 'full':
        date_format = "EEEE MMMM, d, y 'at' h:mma"
    elif date_format == 'medium':
        date_format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, date_format, locale='en')


