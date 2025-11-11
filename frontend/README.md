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