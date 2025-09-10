from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, cors
# from .routes.auth import auth_bp
# from .routes.dashboards import dashboards_bp
# from .routes.players import players_bp
# from .routes.ai import ai_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    cors(app, origins=[app.config["FRONTEND_ORIGIN"]], supports_credentials=True)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # app.register_blueprint(auth_bp, url_prefix="/api/auth")
    # app.register_blueprint(dashboards_bp, url_prefix="/api/dashboards")
    # app.register_blueprint(players_bp, url_prefix="/api/players")
    # app.register_blueprint(ai_bp, url_prefix="/api/ai")

    @app.get("/api/healthz")
    def health():
        return {"ok": True}

    return app

app = create_app()
