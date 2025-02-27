from flask import Flask
from flask_bootstrap import Bootstrap

from redis import Redis

from config import config


bootstrap = Bootstrap()
redis = Redis(host='db', port=6379)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
