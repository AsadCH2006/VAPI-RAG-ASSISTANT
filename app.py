from flask import Flask, render_template

from routes.document import document_bp
from routes.vapi import vapi_bp
from flask_cors import CORS
from config.settings import VAPI_PUBLIC_KEY, VAPI_ASSISTANT_ID


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.register_blueprint(document_bp, url_prefix="/api/documents")
    app.register_blueprint(vapi_bp, url_prefix="/api/vapi")

    @app.get("/")
    def home():
        return render_template(
            "index.html",
            api_key=VAPI_PUBLIC_KEY,
            assistant_id=VAPI_ASSISTANT_ID,
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
