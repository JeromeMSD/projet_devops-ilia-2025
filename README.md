# Microservice User

Ce microservice fait partie du projet DevOps et gère les utilisateurs : création, modification, consultation et authentification.

---

## Technologies utilisées

- Python 3.x
- Flask
- Redis (pour stockage/cache éventuel)
- bcrypt (hachage des mots de passe)
- PyJWT (authentification basée sur token JWT)
- python-dotenv (gestion des variables d'environnement)
- pytest et pytest-flask (tests unitaires)

---

## Prérequis

- Python 3.x installé
- Redis installé et lancé (si utilisé)
- `pip` pour installer les dépendances

---

## Fonctionnalités principales

| Route | Méthode | Description |
|-------|---------|-------------|
| `/api/v1/users` | POST | Créer un nouvel utilisateur |
| `/api/v1/users` | GET | Récupérer la liste des utilisateurs |
| `/api/v1/users/<id>` | GET | Récupérer les détails d’un utilisateur |
| `/api/v1/users/<id>` | PUT | Modifier les informations d’un utilisateur |
| `/api/v1/auth/login` | POST | Authentification et récupération d’un token JWT |

---

## Lancer le microservice

1. Installer les dépendances :

```bash
pip install -r requirements.txt
Lancer le serveur Flask :

bash
Copier le code
export FLASK_APP=src/main.py
export FLASK_ENV=development
flask run
Le microservice sera disponible à l’adresse : http://127.0.0.1:5000/

Tests
Pour lancer les tests unitaires :

bash
Copier le code
pytest
Notes
Les données des utilisateurs peuvent être stockées temporairement dans un fichier CSV ou Redis selon la configuration.

Toutes les routes renvoient des objets JSON. Exemple : { "id": 1, "username": "user1", "email": "user@example.com" }.

Il est recommandé d’utiliser Postman ou curl pour tester les différentes routes.



| Nom            | Prénom           | Pseudo GitHub              | Lien GitHub                                           |
|------          |-----------       |---------------             |-------------                                 |
| DZESSI SIMO    | Franck Junior    | FracnkSimo314              |[Profil](https://github.com/FranckSimo314)    |
| NGOUPAYE DJIO  |  Thierry         |    ThierryNgoupaye         | [Profil](https://github.com/ThierryNgoupaye) |
| AYMEN          | Ben chaabane     |    aymen147                | [Profil](https://github.com/aymen147)        |
| MENDJE TCHEMMOE| Vanelle          |  MENDJEV                   | [Profil](https://github.com/MENDJEV)         |
| NDONGO NGAH    | Estelle Clotilde |  estelleNdongo             [Profil](https://github.com/estelleNdongo)     |
