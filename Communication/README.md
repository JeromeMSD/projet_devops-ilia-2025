# Microservice : Communication

Ce microservice gère toutes les communications sortantes de la plateforme PolyStatus, y compris les annonces publiques, le statut des services et l'envoi d'emails transactionnels.

## Contributeurs (Microservice Communication)

| Nom | Prénom | Pseudo GitHub | Rôles |
| Yasmine | [Nom] | [@pseudo] | [] |
| Cyrine | [Nom] | [@pseudo] | []|
| Mahdi | [Nom] | [@pseudo] | Docker |
| Esteban | [Nom] | [@pseudo] |[] |
| Oumnia | MIMOUNI | https://github.com/OumniaMimouni | Route Email (TDD) , Actions analyse Trivy|

## Prérequis

* [Python 3.10+](https://www.python.org/)
* [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/) (doit être lancé localement pour que l'API fonctionne)

## Installation et Lancement (Local)

Suivez ces étapes pour lancer le microservice sur votre machine locale.

1.  **Accéder au dossier du microservice :**
    (En supposant que vous êtes à la racine du projet `projet_devops-ilia-2025`)

    ```bash
    cd Communication
    ```

2.  **Créer un environnement virtuel Python (venv) :**
    ```bash
    python3 -m venv venv
    ```

3.  **Activer l'environnement virtuel :**
    * Sur macOS/Linux :
        ```bash
        source venv/bin/activate
        ```
    * Sur Windows :
        ```bash
        .\venv\Scripts\activate
        ```
    *(Votre terminal devrait maintenant afficher `(venv)` au début.)*

4.  **Installer les dépendances :**
    (Assurez-vous d'avoir un fichier `requirements.txt`)
    ```bash
    pip install -r requirements.txt
    ```

5.  **Lancer le serveur Redis :**
    (Dans un **nouveau terminal séparé**, lancez votre serveur Redis)
    ```bash
    redis-server
    ```

6.  **Lancer l'application Flask :**
    (De retour dans votre premier terminal avec le `venv` activé)
    ```bash
    python3 src/API_routes.py
    ```
    *L'API est maintenant accessible à l'adresse (par défaut) : `http://localhost:5000`*

## Tests (TDD)

Nous utilisons `pytest` pour les tests unitaires et d'intégration.

Pour lancer la suite de tests (après avoir installé les dépendances) :

```bash
# Assurez-vous que votre venv est activé ( venv )
(venv) ... % pytest

## Documentation de l'API (Swagger)

La documentation complète de l'API, détaillant tous les endpoints et les schémas de données, est disponible dans le fichier `swagger.yaml` situé à la racine du projet.

Vous pouvez utiliser un éditeur en ligne comme [editor.swagger.io](https://editor.swagger.io/) pour visualiser le fichier.

## Routes Implémentées

| Méthode | Route | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/public/announce` | Crée une nouvelle annonce publique. |
| `GET` | `/api/v1/public/status` | Récupère le statut public global (données fictives). |
| `POST` | `/api/v1/email` | Envoie un email transactionnel. |
| `GET` | `/api/v1/test` | Route de test basique. |
