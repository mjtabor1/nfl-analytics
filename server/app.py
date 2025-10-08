import click
from flask import Flask
from config import Config
from extensions import db, migrate, jwt, cors
# from .routes.auth import auth_bp
# from .routes.dashboards import dashboards_bp
# from .routes.players import players_bp
# from .routes.ai import ai_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    cors(app, origins=[app.config["FRONTEND_ORIGIN"]], supports_credentials=True)

    db.init_app(app)
    # migrate.init_app(app, db)
    jwt.init_app(app)

    # app.register_blueprint(auth_bp, url_prefix="/api/auth")
    # app.register_blueprint(dashboards_bp, url_prefix="/api/dashboards")
    # app.register_blueprint(players_bp, url_prefix="/api/players")
    # app.register_blueprint(ai_bp, url_prefix="/api/ai")
    import controllers.nfl.models
    from flask_migrate import Migrate
    Migrate(app, db)

    @app.cli.command("sleeper-import")
    @click.option("--limit", type=int, default=None, help="Limit number of players to import")
    def sleeper_import(limit):
        from controllers.nfl.import_sleeper import import_players_from_sleeper
        result = import_players_from_sleeper(limit=limit)
        click.echo(f"Imported {result['upserted_players']} players and {result['upserted_teams']} teams.")

    @app.get("/api/healthz")
    def health():
        return {"ok": True}

    return app

app = create_app()
