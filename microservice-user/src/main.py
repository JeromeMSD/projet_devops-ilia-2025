from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from .controller import register_routes
from dotenv import load_dotenv
import os

load_dotenv()

#from controller import register_routes

MICRO_SERVICE_HOST = os.getenv('MICRO_SERVICE_USER_HOST')
MICRO_SERVICE_PORT = int(os.getenv('MICRO_SERVICE_USER_PORT'))

# Swagger configuration
SWAGGER_URL = '/api/docs'
API_URL = '/swagger.yaml'

MICRO_SERVICE_HOST = os.getenv('MICRO_SERVICE_USER_HOST')
MICRO_SERVICE_PORT = int(os.getenv('MICRO_SERVICE_USER_PORT'))


def create_app():
    app_boot = Flask(__name__)

    # Enregistrement des routes
    register_routes(app_boot)

    # Swagger UI configuration
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "User Microservice API"
        }
    )
    app_boot.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Route to serve swagger.yaml
    @app_boot.route('/swagger.yaml')
    def swagger_yaml():
        return send_from_directory(
            os.path.join(os.path.dirname(os.path.dirname(__file__))),
            'swagger.yaml'
        )



    # Enregistrement des routes
    register_routes(app_boot)

    return app_boot


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host=MICRO_SERVICE_HOST, port=MICRO_SERVICE_PORT)

