from flask import Flask, request, jsonify

app = Flask(__name__)

feature_flags = {
    "dashboard": {
        "enabled": True,
        "description": "Activer le nouveau tableau de bord.",
        "roles": ["admin", "sre"]
    },
    "beta-feature": {
        "enabled": False,
        "description": "Fonctionnalité expérimentale en beta.",
        "roles": [] # Accessible à tous si activé
    }
}

@app.route('/flags', methods=['GET'])
def get_flags_for_user():


    #Récupère les flags applicables à un utilisateur en fonction de son rôle.
    # 1. Récupérer le rôle depuis les paramètres de l'URL (ex: ?role=admin)
    user_role = request.args.get('role')
    
    applicable_flags = {}
    # 2. Parcourir chaque feature flag
    for key, config in feature_flags.items():
        # 3. Vérifier la logique : le flag est-il activé ET (public OU l'utilisateur a le bon rôle) ?
        is_enabled = config.get('enabled', False)
        is_public = not config.get('roles') # La liste des rôles est vide, donc c'est public
        has_permission = user_role in config.get('roles', [])
        
        # Le flag est actif pour cet utilisateur si les conditions sont remplies
        applicable_flags[key] = is_enabled and (is_public or has_permission)

    return jsonify(applicable_flags)

@app.route('/admin/flags', methods=['GET'])
def get_all_flags():
    """Retourne la liste complète de tous les feature flags et leur configuration."""
    return jsonify(feature_flags)

@app.route('/admin/flags/<string:flag_name>', methods=['POST'])
def create_or_update_flag(flag_name):

    #Crée un feature flag s'il n'existe pas (HTTP 201) ou le met à jour complètement s'il existe (HTTP 200).
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    # Déterminer si c'est une création ou une mise à jour pour le code de statut
    http_status = 200 # OK (Update)
    if flag_name not in feature_flags:
        http_status = 201 # Created
    
    # Créer ou remplacer la configuration du flag
    feature_flags[flag_name] = {
        "enabled": data.get("enabled", False),
        "description": data.get("description", ""),
        "roles": data.get("roles", [])
    }
    
    return jsonify(feature_flags[flag_name]), http_status

@app.route('/admin/toggle/<string:flag_name>', methods=['POST'])
def toggle_flag(flag_name):
    #active ou désactive un feature flag existant
    if flag_name in feature_flags:
        feature_flags[flag_name]["enabled"] = not feature_flags[flag_name]["enabled"]
        return jsonify(feature_flags[flag_name]), 200
    else:
        return jsonify({"error": "Flag not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
