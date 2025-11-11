import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
load_dotenv()
MICRO_SERVICE_HOST = os.getenv('MICRO_SERVICE_USER_HOST', '0.0.0.0')
MICRO_SERVICE_PORT = int(os.getenv('MICRO_SERVICE_USER_PORT', 5010))


def create_app() -> Flask:
    app_boot = Flask(__name__)
    CORS(app_boot)
    # Enregistrement des routes
    from .controller import register_routes
    register_routes(app_boot)
    return app_boot


if __name__ == '__main__':
    app: Flask = create_app()
    app.run(debug=False, host=MICRO_SERVICE_HOST, port=MICRO_SERVICE_PORT)
