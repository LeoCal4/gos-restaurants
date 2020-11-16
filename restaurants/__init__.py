import os

from flask import Flask
from flask_environments import Environments
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import connexion
from connexion.resolver import RestyResolver

__version__ = '0.1'

db = None
migrate = None
login = None
debug_toolbar = None


def create_app():
    """
    This method create the Flask application.
    :return: Flask App Object
    """
    global db
    global app
    global migrate
    global login

    conn = connexion.App(__name__)#, instance_relative_config=True)
    app = conn.app

    flask_env = os.getenv('FLASK_ENV', 'None')
    if flask_env == 'development':
        config_object = 'config.DevConfig'
    elif flask_env == 'testing':
        config_object = 'config.TestConfig'
    elif flask_env == 'production':
        config_object = 'config.ProdConfig'
    else:
        raise RuntimeError(
            "%s is not recognized as valid app environment. You have to setup the environment!" % flask_env)

    # Load config
    env = Environments(app)
    env.from_object(config_object)

    # registering db
    db = SQLAlchemy(
        app=app
    )

    # requiring the list of models
    register_extensions(app)
    register_blueprints(app)

    # creating migrate
    migrate = Migrate(
        app=app,
        db=db
    )

    # checking the environment
    if flask_env == 'testing':
        # we need to populate the db
        db.create_all()

    if flask_env == 'testing' or flask_env == 'development':
        register_test_blueprints(app)

    conn.add_api('../swagger.yml')
    
    return app


def register_extensions(app):
    """
    It register all extensions
    :param app: Flask Application Object
    :return: None
    """
    global debug_toolbar

    if app.debug:
        try:
            from flask_debugtoolbar import DebugToolbarExtension
            debug_toolbar = DebugToolbarExtension(app)
        except ImportError:
            pass


def register_blueprints(app):
    """
    This function registers all views in the flask application
    :param app: Flask Application Object
    :return: None
    """
    from restaurants.views import blueprints
    for bp in blueprints:
        app.register_blueprint(bp, url_prefix='/')


def register_test_blueprints(app):
    """
    This function registers the blueprints used only for testing purposes
    :param app: Flask Application Object
    :return: None
    """

    from restaurants.views.utils import utils
    app.register_blueprint(utils)
