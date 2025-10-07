
import os
from flask import Flask, redirect, url_for
from app.routes.listing import listing_bp

def create_app():
    app = Flask(__name__)
    app.config["DB_PATH"] = os.environ.get("DB_PATH", os.path.abspath("jobs.db"))
    app.register_blueprint(listing_bp)
    @app.route("/")
    def home():
        return redirect(url_for("listing.list_jobs"))
    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", "5001"))
    app.run(host="0.0.0.0", port=port, debug=True)
