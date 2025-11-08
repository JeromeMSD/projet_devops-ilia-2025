from flask import Flask
from routes.findalluser import Get_all_users
from routes.createuser import Create_user

def register_routes(app: Flask):
    """
        Dans ce fichier chaque membre du groupe viendra enregistrer sa/ses routes qu'il aura écrites dans son/ses fichiers.
    """
    app.register_blueprint(Get_all_users)
    #app.register_blueprint(Create_user)

    

    