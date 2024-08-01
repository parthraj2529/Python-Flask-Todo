from flask import Flask
from db import db
from flask_smorest import Api
from resources.task import blp as TaskBluePrint
from resources.user import blp as UserBluePrint

def create_app(db_url=None):  # Use = instead of ==
    app = Flask(__name__)
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    
    db.init_app(app)

    with app.app_context():
        import models  # noqa: F401

        db.create_all()

    api = Api(app)
    api.register_blueprint(TaskBluePrint)
    api.register_blueprint(UserBluePrint)


    return app
