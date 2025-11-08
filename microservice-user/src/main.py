from flask import Flask
from .controller import register_routes
from dotenv import load_dotenv
import os

load_dotenv()

MICRO_SERVICE_HOST = os.getenv('MICRO_SERVICE_USER_HOST')
MICRO_SERVICE_PORT = int(os.getenv('MICRO_SERVICE_USER_PORT'))


def create_app():
    app_boot = Flask(__name__)



    # Enregistrement des routes
    register_routes(app_boot)

    return app_boot


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host=MICRO_SERVICE_HOST, port=MICRO_SERVICE_PORT)

