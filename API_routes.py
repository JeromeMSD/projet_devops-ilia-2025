from datetime import datetime
from config_redis import redis_client
from flask import jsonify, Flask, request

app = Flask(__name__)
app.config["DEBUG"] = True

#Route test
@app.route("/test", methods=['GET'])
def test():
    test1 = {"id":1, "name":"Aude", "Lastname":"Javel"}
    return jsonify(test1)

#Route annonce
@app.route('/api/announce', methods=['POST'])
def CreateAnnouncement():

    data = request.get_json()

    #Compteur redis pour incrémenter l'id à chaque annonce crée
    announce_id = redis_client.incr('announce_id')

    announce1 = {
        "id": announce_id,
        "message": data["message"],
        "etat": data["etat"],
        "date":datetime.now().date().isoformat()
    }

    redis_client.lpush("annonces", str(announce1))

    return jsonify({
        "message":"Annonce bien enregistrée",
        "announce": announce1
    }),201

app.run()