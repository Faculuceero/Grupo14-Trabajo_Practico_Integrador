from flask import Flask

from plataforma_qa.config import Config
from plataforma_qa.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(config_class)

    db.init_app(app)

    from plataforma_qa.api.categorias import categorias_api_bp
    from plataforma_qa.api.health import health_bp
    from plataforma_qa.api.preguntas import preguntas_api_bp
    from plataforma_qa.api.respuestas import respuestas_api_bp
    from plataforma_qa.api.votos import votos_api_bp
    from plataforma_qa.web.auth import auth_bp
    from plataforma_qa.web.preguntas import preguntas_bp
    from plataforma_qa.web.users import users_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(preguntas_bp)
    app.register_blueprint(categorias_api_bp)
    app.register_blueprint(preguntas_api_bp)
    app.register_blueprint(respuestas_api_bp)
    app.register_blueprint(votos_api_bp)

    return app