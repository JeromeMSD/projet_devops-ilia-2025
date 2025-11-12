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

## Contributeurs

LITRA Aurélien
LOCTIN Thomas
MATHIEU Arthur
PROTIN Augustin
PUCHEU Mathias
SIDRE Ylian
VILLERET Baptiste
