import os
from flask import Blueprint, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL = '/api/docs'
API_URL = '/swagger.yaml'
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
swagger_bp = Blueprint('swagger_doc', __name__)

# 2. Configuration du Swagger UI (Route /api/docs)
# Le Blueprint Swagger UI est créé et enregistré comme une sous-route.
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "User Microservice API"
    }
)
# Enregistrement de Blueprint de Swagger UI sur notre Blueprint local
swagger_bp.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Route pour Servir swagger.yaml (Route /swagger.yaml)
# Cette route est attachée directement à notre Blueprint 'swagger_bp'


@swagger_bp.route(API_URL)
def swagger_yaml():
    """Sert le fichier swagger.yaml depuis la racine du projet."""
    return send_from_directory(
        ROOT_DIR,
        'swagger.yaml'
    )
