# Microservice User

Ce microservice fait partie du projet DevOps et gère les utilisateurs : création, modification, consultation et authentification.


---

## Ce qu’on utilise

- Python 3.x
- Flask
- Redis (pour stocker des infos si besoin)
- bcrypt (pour sécuriser les mots de passe)
- PyJWT (pour les tokens de connexion)
- python-dotenv (pour gérer les variables d'environnement)
- pytest et pytest-flask (pour tester les routes)

---

## Routes principales

| Route | Méthode | Ce que ça fait |
|-------|---------|----------------|
| `/api/v1/users` | POST | Créer un nouvel utilisateur |
| `/api/v1/users` | GET | Voir tous les utilisateurs |
| `/api/v1/users/<id>` | GET | Voir les infos d’un utilisateur |
| `/api/v1/users/<id>` | PUT | Modifier les infos d’un utilisateur |
| `/api/v1/auth/login` | POST | Se connecter et récupérer un token |

---

## Comment lancer le microservice

1. Installer les dépendances :

```bash
pip install -r requirements.txt
Lancer le serveur Flask :

bash
Copier le code
export FLASK_APP=src/main.py
export FLASK_ENV=development
flask run
Le microservice sera accessible sur : http://127.0.0.1:5000/

Tester
Pour lancer les tests, faire :

bash
Copier le code
pytest
Notes
Les données peuvent être stockées dans un fichier CSV ou dans Redis selon ce qu’on choisit.

Toutes les réponses des routes sont en JSON.

