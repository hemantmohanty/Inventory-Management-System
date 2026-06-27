from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Database config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sales.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "your-very-secret-key"

    # Init SQLAlchemy
    db.init_app(app)

    # ---- Blueprints import + register () ----
    from app.routes.login import login_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.edit import edit_bp
    from app.routes.create import create_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(create_bp)
    app.register_blueprint(edit_bp)
    # --------------------------------------------------------------

    return app