from flask import Flask

from plataforma_qa.config import Config
from plataforma_qa.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(config_class)

    db.init_app(app)

    from plataforma_qa.api.health import health_bp
    from plataforma_qa.web.users import users_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(users_bp)

    return app
