from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()

def create_app(config_object='config.Config'):
    app = Flask(
        __name__, 
        template_folder='templates', 
        static_folder='static'
    )
    app.config.from_object(config_object)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    # register blueprints
    from app.routes.auth import auth
    app.register_blueprint(auth)

    return app
