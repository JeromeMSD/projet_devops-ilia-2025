# projet\_devops-ilia-2025

Polytech Dijon - ILIA - Projet DevOps 2025

## Contributeurs (Microservice Communication)

| Prénom      | Nom     | Pseudo GitHub                                         |
|----------|------------|-------------------------------------------------------|
| Emmanuel  | PEYRONNET | [Emmanuel0071](https://github.com/Emmanuel0071)       |


## Information lancement avec docker

## Creation dockerfile

```bash
docker build -t feature-flags-app .
```

### lancement  docker

```bash
docker run -d -p 5000:5000 feature-flags-app
```

-----
## Information commande d'instalation pour le faire manuellement sans Docker

```bash
pip install -r requirements.txt
```

-----

## Pour tester il faut faire python pour lancer le serveur
```bash
python -m src.server
```

-----

# information Général

## pour voir les differents roles présent:

[http://127.0.0.1:5000/admin/flags](http://127.0.0.1:5000/admin/flags)

## pour voir si admin par exemple est dans une des "fonctionalité"

[http://127.0.0.1:5000/flags?role=admin](http://127.0.0.1:5000/flags?role=admin)

## pour trouver le backoffice

[http://127.0.0.1:5000/backoffice/role=admin](http://127.0.0.1:5000/backoffice/role=admin)
[http://127.0.0.1:5000/backoffice/role=sre](http://127.0.0.1:5000/backoffice/role=sre)
[http://127.0.0.1:5000/backoffice/role=user](http://127.0.0.1:5000/backoffice/role=user)

-----

## exemple de requete pour rajouter un nouveau flag dans les deux presents pour le moment en la metant dans un autre terminal

```bash
Invoke-WebRequest -Uri http://127.0.0.1:5000/admin/flags/new-login-page -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"enabled": true, "description": "Nouvelle page de connexion", "roles": ["sre"]}'
```


-----

test unitaire :

```bash
pytest test/test_app.py
```
