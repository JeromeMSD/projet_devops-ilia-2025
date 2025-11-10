import os

from dotenv import load_dotenv
from flask import Flask
from .routes.find_all_user import get_all_users_bp
from .routes.login import login_bp
from .routes.swagger import swagger_bp
from .routes.register import register_bp
from .routes.logout import logout_bp 

load_dotenv()
BASE_API_URL = os.getenv('BASE_API_URL')

def register_routes(app: Flask):
    """
        Dans ce fichier chaque membre du groupe viendra enregistrer sa/ses routes qu'il aura écrites dans son/ses fichiers.
    """
    # Route du registration
    app.register_blueprint(register_bp,url_prefix=BASE_API_URL )

    # Routes de login et verification du token
    app.register_blueprint(login_bp, url_prefix=BASE_API_URL)

    # Route de recuperation de tous les utilisateurs presents en BD
    app.register_blueprint(get_all_users_bp, url_prefix=BASE_API_URL)

    # Routes servant le swagger ui et le swagger.yaml
    app.register_blueprint(swagger_bp)

    #Route pour le déconexion
    app.register_blueprint(logout_bp, url_prefix=BASE_API_URL)




