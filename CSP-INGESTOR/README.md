# 🌩️ PolyStatus - API d'ingestion CSP

**PolyStatus** est un microservice léger permettant de surveiller les statuts des fournisseurs de services cloud.  
Il ingère leurs flux JSON, stocke les événements dans Redis et expose une API REST facile à utiliser pour les consulter.

---

## Fonctionnalités principales

- Enregistrer des fournisseurs CSP et leurs flux JSON
- Actualiser les événements en temps réel
- Consulter tous les événements ou seulement ceux actifs (non opérationnels)
- Documentation Swagger intégrée pour tester facilement l’API

---

## Prérequis

- Requirement.txt
- Redis (host par défaut `redis`, port `6379`)
- Docker pour un déploiement conteneurisé

---

## Lancer le service

### En local

Lancez docker-compose.yml 

```docker-compose build --no-cache```
```docker-compose up```

## Accéder à Swagger UI

### En local

http://localhost:8083/docs


# Endpoints API

## Ajouter un fournisseur CSP

```POST /api/v1/csp/providers```

Exemple Json :

```Json
{
  "name": "github",
  "feed_url": "https://www.githubstatus.com/api/v2/components.json",
  "type": "json"
}
```
Réponse attendue :

```json
{
  "message": "Provider enregistré avec succès"
}
```

## Actualiser les événements d’un fournisseur

Exemple :

POST /api/v1/csp/refresh?provider=github

Réponse :

```json
{
  "message": "Refreshed 5 events",
  "events": [
    {"provider": "github", "service": "GitHub API", "status": "operational"},
    ...
  ]
}
```

```tips
Cette route récupère les derniers événements du fournisseur et les stocke dans Redis.
```

## Récupérer les événements

GET ```/api/v1/csp/events?active=<true|false>```

Exemple :

GET /api/v1/csp/events?active=true

Réponse :

```json
[
  {"provider": "github", "service": "GitHub API", "status": "degraded_performance"},
  ...
]
```
Si ``active=true``, seuls les statuts non opérationnels seront retournés.

# Ajouter des fournisseurs

## Option 1 : Via l’API

```http
POST /api/v1/csp/providers
Content-Type: application/json

{
  "name": "aws",
  "feed_url": "https://status.aws.amazon.com/data.json",
  "type": "json"
}
```

## Option 2 : Directement via Redis CLI (Windows CMD)

```cmd
curl -X POST "http://localhost:8083/api/v1/csp/providers" -H "Content-Type: application/json" -d "{\"name\": \"cloudflarestatus\", \"feed_url\": \"https://www.cloudflarestatus.com/api/v2/summary.json\", \"type\": \"json\"}"

curl -X POST "http://localhost:8083/api/v1/csp/providers" -H "Content-Type: application/json" -d "{\"name\": \"github\", \"feed_url\": \"https://www.githubstatus.com/api/v2/summary.json\", \"type\": \"json\"}"

curl -X POST "http://localhost:8083/api/v1/csp/providers" -H "Content-Type: application/json" -d "{\"name\": \"aws\", \"feed_url\": \"https://status.aws.amazon.com/data.json\", \"type\": \"json\"}"

curl -X POST "http://localhost:8083/api/v1/csp/providers" -H "Content-Type: application/json" -d "{\"name\": \"googlecloud\", \"feed_url\": \"https://status.cloud.google.com/incidents.json\", \"type\": \"json\"}"

curl -X POST "http://localhost:8083/api/v1/csp/providers" -H "Content-Type: application/json" -d "{\"name\": \"azure\", \"feed_url\": \"https://status.azure.com/en-us/status/feed\", \"type\": \"json\"}"
```

# Organisation Redis

csp:providers → Hash de tous les fournisseurs

csp:events:<provider> → Liste des événements par fournisseur

## Fournisseurs déjà configurés

```text
azure
googlecloud
cloudflarestatus
github
aws
```

Chaque fournisseur peut être mis à jour via ``/api/v1/csp/refresh``.

## Tester l’API sans Swagger (pas recommandé, pas 100% fonctionnel)

### Avec curl :

```bash
curl -X GET "http://127.0.0.1:8083/api/v1/csp/events?active=true" -H "accept: application/json"
```
### Avec HTTPie :

```bash
http GET http://127.0.0.1:8083/api/v1/csp/events active==true
```


# Notes annexes :

PolyStatus fonctionne uniquement avec des flux JSON pour l’instant.

Les événements sont normalisés pour avoir au minimum ``provider``, ``service`` et ``status``.

Les doublons ne sont pas créés pour un même fournisseur et même service.