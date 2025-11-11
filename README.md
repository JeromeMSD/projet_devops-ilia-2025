ceci plutot:

# User Microservice - Documentation Complète

## Description du Projet

Microservice de gestion des utilisateurs, de l'authentification et des rôles pour une architecture microservices. Ce service agit comme *API d'authentification centrale (Auth Gateway)* pour les autres microservices du système.

### Fonctionnalités Principales

- Inscription et authentification des utilisateurs (JWT)
- Gestion des rôles (USER, ADMIN, SRE)
- Réinitialisation de mot de passe
- Vérification des tokens pour les autres microservices
- Stockage des sessions dans Redis
- Documentation API avec Swagger UI

---

## Technologies Utilisées

- *Backend*: Flask 3.0.0
- *Base de données*: Redis 7-alpine
- *Authentification*: JWT (PyJWT 2.8.0)
- *Sécurité*: bcrypt 4.1.2
- *Tests*: pytest 7.4.3, pytest-flask 1.3.0
- *Conteneurisation*: Docker, Docker Compose
- *Documentation*: Swagger UI

---

## Installation et Configuration

### Prérequis

- Python 3.11+
- Redis 7+
- Docker et Docker Compose (pour le déploiement conteneurisé)

### Installation Locale (Sans Docker)

1. *Cloner le repository*
bash
git clone https://github.com/JeromeMSD/projet_devops-ilia-2025.git
cd microservice-user


2. *Créer un environnement virtuel*

* Sur Linus/macOS
bash
python -m venv .venv
source venv/bin/activate  


* Sur Windows
bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1



3. *Installer les dépendances*
bash
pip install -r requirements.txt


4. *Configurer les variables d'environnement*

Copier le fichier .env.example vers .env et configurer les valeurs : 

bash
cp .env.example .env


Contenu du fichier .env:
env
# Redis configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB_USERS=0
REDIS_TEST_DB=1

# User configuration
EMAIL_KEY=email:
USER_KEY=user:

# JWT configuration
JWT_SECRET_KEY=dev-secret-key
RESET_TOKEN_KEY=reset:token:

# Flask configuration
MICRO_SERVICE_USER_HOST=0.0.0.0
MICRO_SERVICE_USER_PORT=5010

FLASK_TESTING=false
BASE_API_URL=/api/v1


5. *Démarrer Redis localement*
bash
redis-server


6. *Lancer l'application*
bash
flask run


L'application sera accessible sur http://localhost:5010

---

## Déploiement avec Docker Compose

### Prérequis

- Docker 20.10+

### Lancement

1. *Construire et démarrer les services*
bash
docker compose up -d --build 


2. *Vérifier les logs*
bash
docker compose logs -f


3. *Arrêter les services*
bash
docker-compose down


4. *Arrêter et supprimer les volumes*
bash
docker compose down -v


### Services Docker Compose

Le fichier docker-compose.yaml définit deux services:

- *redis*: Base de données Redis (port 6385:6379)
- *user-microservice*: Application Flask (port 5010:5010)

---

## Documentation API

### Accès à la Documentation Swagger

Une fois l'application lancée, accédez à la documentation interactive:


http://localhost:5010/api/docs


### Routes Disponibles

#### 1. Authentification

*POST /api/v1/register*
- Inscription d'un nouvel utilisateur
- Body: { firstname, lastname, email, password, role }
- Rôles disponibles: USER, ADMIN, SRE
- Retourne: 201 avec les informations utilisateur

*POST /api/v1/login*
- Connexion d'un utilisateur
- Body: { email, password }
- Retourne: 200 avec JWT token et informations utilisateur

*GET /api/v1/verify-token*
- Vérifie la validité d'un token JWT
- Header: Authorization: Bearer <token>
- Retourne: 200 avec informations utilisateur si token valide

*POST /api/v1/logout*
- Déconnexion (révoque le token)
- Header: Authorization: Bearer <token>
- Retourne: 200 si déconnexion réussie

#### 2. Gestion des Utilisateurs

*GET /api/v1/users*
- Récupère tous les utilisateurs (avec filtrage optionnel par rôle)
- Query param (optionnel): ?role=ADMIN|USER|SRE
- Header: Authorization: Bearer <token>
- Permissions: ADMIN ou SRE uniquement
- Retourne: 200 avec liste des utilisateurs

*PUT /api/v1/users/{user_id}*
- Modifie un utilisateur
- Header: Authorization: Bearer <token>
- Body: { firstname?, lastname?, role? }
- Permissions: ADMIN ou SRE uniquement
- Retourne: 200 avec utilisateur modifié

#### 3. Réinitialisation de Mot de Passe

*POST /api/v1/forgot-password*
- Demande de réinitialisation de mot de passe
- Body: { email }
- Retourne: 200 avec reset_token (valable 30 minutes)

*POST /api/v1/reset-password*
- Réinitialise le mot de passe avec un token de reset
- Body: { reset_token, new_password }
- Retourne: 200 si réinitialisation réussie

---

## Tests

### Exécuter les Tests

*Tous les tests*
bash
python3 -m pytest tests -v



*Tests spécifiques*
bash
python3 -m pytest tests/test_login.py -v
python3 -m pytest tests/test_register.py -v
python3 -m pytest tests/test_find_users_by_role.py -v


### Configuration des Tests

Les tests utilisent automatiquement :
- Base de données Redis dédiée (DB 1)
- Variable d'environnement FLASK_TESTING=true
- Nettoyage automatique avant et après chaque test

---

## Architecture du Projet


microservice-user/
├── src/
│   ├── main.py              # Point d'entrée de l'application
│   ├── controller.py        # Enregistrement des routes
│   ├── auth.py              # Décorateur d'authentification
│   ├── utils.py             # Fonctions utilitaires (JWT, hash)
│   ├── redis_client.py      # Client Redis singleton
│   ├── models/
│   │   └── user.py          # Modèle User
│   └── routes/
│       ├── register.py      # Route d'inscription
│       ├── login.py         # Routes de connexion
│       ├── logout.py        # Route de déconnexion
│       ├── find_users_by_role.py  # Récupération utilisateurs
│       ├── update_user.py   # Modification utilisateur
│       ├── forgot_password.py     # Demande de reset
│       ├── reset_password.py      # Reset mot de passe
│       └── swagger.py       # Documentation Swagger
├── tests/
│   ├── conftest.py          # Configuration des fixtures
│   └── test_*.py            # Tests unitaires
├── docker-compose.yaml
├── Dockerfile
├── .flake8
├── .flaskenv    # configurations pour le lancement de flask
├── .gitignore
├── .dockerignore
├── requirements.txt
├── swagger.yaml
├── .env
├── .env.example
└── README.md


---

## Sécurité

### Mots de Passe

- Hashés avec bcrypt (salt automatique)
- Validation: minimum 6 caractères, 1 majuscule, 1 chiffre

### Tokens JWT

- Clé secrète configurable (variable JWT_SECRET_KEY)
- Validité: 24 heures par défaut
- Stockage dans Redis pour révocation
- Vérification de signature et expiration

### Protection des Routes

- Décorateur @auth_required() pour les routes protégées
- Vérification des rôles: @auth_required(roles=['ADMIN', 'SRE'])
- Validation du token à chaque requête

---

## Variables d'Environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| REDIS_HOST | Hôte Redis | localhost |
| REDIS_PORT | Port Redis | 6379 |
| REDIS_DB_USERS | DB Redis (production) | 0 |
| REDIS_TEST_DB | DB Redis (tests) | 1 |
| JWT_SECRET_KEY | Clé secrète JWT | dev-secret-key |
| MICRO_SERVICE_USER_PORT | Port du service | 5010 |
| BASE_API_URL | Préfixe des routes | /api/v1 |

---

## Codes de Retour HTTP

| Code | Description |
|------|-------------|
| 200 | Succès |
| 201 | Ressource créée |
| 400 | Données invalides |
| 401 | Mot de passe incorrect |
| 403 | Accès refusé (token invalide/expiré) |
| 404 | Ressource non trouvée |
| 409 | Conflit (email déjà utilisé) |
| 500 | Erreur serveur |

---

## Dépendances (requirements.txt)


Flask==3.0.0
flask-cors==6.0.0
flask-swagger-ui==4.11.1
redis==7.0.0
PyJWT==2.8.0
werkzeug==3.0.6
python-dotenv==1.0.0
bcrypt==4.1.2
pytest==7.4.3
pytest-flask==1.3.0


---

## Contributeurs

Ce microservice a été développé dans le cadre du projet DevOps - ILIA 2025 à Polytech Dijon.

### Équipe de Développement

- THIERRY NGOUPAYE DJIO [github](https://github.com/ThierryNgoupaye)
- Estelle Clotilde NGAH NDONGO ~ [github](https://github.com/estelleNdongo)
- Aymen Ben Chaabane ~ [gitHub](https://github.com/aymen147)
- Vanelle MENDJE ~ [gitHub](https://github.com/MENDJEV)
- Simo Franck ~ [gitHub](https://github.com/FranckSimo314)

---

## Bonnes Pratiques

### Développement

- Écrire des tests pour chaque nouvelle route
- Respecter les conventions de nommage Python (PEP 8)
- Commenter le code complexe

### Production

- Changer JWT_SECRET_KEY par une clé forte
- Utiliser HTTPS pour les communications
- Limiter les tentatives de connexion (rate limiting)
- Surveiller les logs Redis et Flask

---

## Troubleshooting

### Erreur de connexion Redis

bash
# Vérifier que Redis est démarré
redis-cli ping
# Doit retourner: PONG

# Vérifier la connexion Docker
docker ps


### Port déjà utilisé

bash
# Changer le port dans .env
MICRO_SERVICE_USER_PORT=5011

# Ou libérer le port
sudo lsof -ti:5010 | xargs kill -9


### Tests échouent

bash
# Nettoyer la DB de test
redis-cli -n 1 FLUSHDB

# Vérifier la variable d'environnement
export FLASK_TESTING=true


---

## Licence

Ce projet est développé dans un cadre académique à Polytech Dijon.

---

## Support

Pour toute question ou problème, veuillez contacter l'équipe de développement ou ouvrir une issue sur le repository Git.



| Nom            | Prénom           | Pseudo GitHub              | Lien GitHub                                           |
|------          |-----------       |----------------            |-------------                                 |
| DZESSI SIMO    | Franck Junior    | FracnkSimo314              |[Profil](https://github.com/FranckSimo314)    |
| NGOUPAYE DJIO  | Thierry         |    ThierryNgoupaye         | [Profil](https://github.com/ThierryNgoupaye) |
| BEN CHAABANE   | Aymen     |    aymen147                | [Profil](https://github.com/aymen147)        |
| MENDJE TCHEMMOE| Vanelle          |  MENDJEV                   | [Profil](https://github.com/MENDJEV)         |
| NDONGO NGAH    | Estelle Clotilde |  estelleNdongo            | [Profil](https://github.com/estelleNdongo)     |
