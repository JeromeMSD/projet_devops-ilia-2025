from flask import Flask, request, jsonify

app = Flask(__name__)

feature_flags = {
    "new-dashboard": {
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
    """
    Récupère les flags applicables à un utilisateur en fonction de son rôle.
    Exemple d'appel : /flags?role=admin
    """
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
