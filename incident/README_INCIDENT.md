# Microservice - Gestion des Incidents

Ce microservice fait partie du projet PolyStatus. Son rôle est de gérer tout le cycle de vie des incidents : création, suivi, assignation, et postmortem.

## Installation

Ce projet utilise des dépendances de production et de développement séparées.

-   `requirements.txt`: Contient les paquets nécessaires pour faire tourner le service (ex: `Flask`, `redis`).
-   `requirements-dev.txt`: Contient les paquets nécessaires pour tester et développer (ex: `pytest`).

Pour installer toutes les dépendances nécessaires au développement local, lancez :

```bash
# Depuis le dossier incidents/
pip install -r requirements.txt -r requirements-dev.txt
```

## Lancement local

Pour démarrer le serveur Flask :

```
python src/main.py
```

Le serveur sera accessible à l'adresse http://127.0.0.1:5000

## Tester le code

Il y a deux façons de tester le service pour s'assurer qu'il fonctionne.

### Manuellement (avec curl)

Tu peux "attaquer" l'API directement depuis un autre terminal pour voir si elle répond bien avec la commande :

```
curl http://127.0.0.1:5000/api/v1/incidents/health
```

### Automatiquement (avec pytest)

Dans le dossier Incident avec la commande :

```
pytest
```
##  Docker
### Construire l'image
Depuis le dossier incidents/ :
```
docker build -t incidents-service .
```
### Lancer le conteneur
```
docker run -p 5000:5000 incidents-service
```
Le service sera disponible ici : 
```
http://localhost:5000/api/v1/incidents/health
```
## Scanner avec Trivy
### Si Trivy est déjà installé :
```
trivy image incidents-service
```
Ajouter ici les résultats du dernier scan trivy :
```
Résultat dernier scan

CRITICAL: X
HIGH: X
MEDIUM: X
LOW: X
```
## Swagger
Le fichier swagger.yaml se trouve à la racine du microservice et doit rester synchronisé avec les routes implémentées

## Contributeurs

LITRA Aurélien
LOCTIN Thomas
MATHIEU Arthur
PROTIN Augustin
PUCHEU Mathias
SIDRE Ylian
VILLERET Baptiste
