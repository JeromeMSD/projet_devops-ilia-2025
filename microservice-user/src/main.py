from flask import Flask
from flask_cors import CORS

from .controller import register_routes
from dotenv import load_dotenv
import os




load_dotenv()



MICRO_SERVICE_HOST = os.getenv('MICRO_SERVICE_USER_HOST')
MICRO_SERVICE_PORT = int(os.getenv('MICRO_SERVICE_USER_PORT'))


from .controller import register_routes




def create_app():

    app_boot = Flask(__name__)
    CORS(app_boot)



    # Enregistrement des routes
    register_routes(app_boot)

    return app_boot


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host=MICRO_SERVICE_HOST, port=MICRO_SERVICE_PORT)

