# Frontend

Le frontend utilise React avec Vite.

## Installation

Pour lancer le frontend, il faut lancer les commandes suivantes :

```shell
npm i
npm run dev
```

## Docker

Vous pouvez aussi lancer le frontend avec Docker :

```shell
npm run docker
```

L'application sera disponible sur le port 3000.

## Lint

Pour lancer le linter, il faut lancer la commande suivante :

```shell
npm run lint
```

## Tests

Pour lancer les tests, il faut lancer la commande suivante :

```shell
npm run test
```

## Authentification (mock)

Par défaut, le frontend essaie d'appeler l'API (`VITE_AUTH_MODE=api`). Tant que votre microservice d'authentification n'est pas prêt, vous pouvez activer un mode mock qui simule totalement la connexion en ajoutant dans `.env.local` :

```
VITE_AUTH_MODE=mock
```

Quand l'API sera disponible, supprimez cette variable (ou remettez `api`) et, si besoin, définissez `VITE_API_URL` vers la bonne URL (ex: `http://localhost:5001`). Relancez `npm run dev` pour prendre en compte les changements.

## Sécurité – Scan Trivy

Dernier scan : 2025-11-11  
Image scannée : `frontend:trivy` (basée sur `nginx:1.27-alpine`)

Résumé des vulnérabilités (CRITICAL, HIGH, MEDIUM) :

- CRITICAL : 0
- HIGH     : 0
- MEDIUM   : 0

Commande utilisée :

```bash
docker build -t frontend:trivy .
trivy image --severity CRITICAL,HIGH,MEDIUM --ignore-unfixed frontend:trivy
```
