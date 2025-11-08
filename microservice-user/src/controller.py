from flask import Flask
from .routes.login import login_bp



def register_routes(app: Flask):
    """
        Dans ce fichier chaque membre du groupe viendra enregistrer sa/ses routes qu'il aura écrites dans son/ses fichiers.
    """

    # Routes de login et verification du token
    app.register_blueprint(login_bp)
