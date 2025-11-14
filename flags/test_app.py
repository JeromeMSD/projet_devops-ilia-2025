import json
import pytest
from server import app
from flags.app import feature_flags as app_feature_flags

@pytest.fixture
def client():
    #Crée un client de test pour l'application Flask.
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def reset_feature_flags():
    #Réinitialise les feature flags avant chaque test pour garantir l'isolation.
    # Sauvegarde l'état original
    original_flags = {
        "dashboard": {
            "enabled": True,
            "description": "Activer le nouveau tableau de bord.",
            "roles": ["admin", "sre"]
        },
        "beta-feature": {
            "enabled": False,
            "description": "Fonctionnalité expérimentale en beta.",
            "roles": []
        }
    }
    # Avant le test, on s'assure que les flags sont dans leur état initial
    app_feature_flags.clear()
    app_feature_flags.update(original_flags)
    yield
    # Le nettoyage après le test n'est pas strictement nécessaire avec ce setup,
    # mais c'est une bonne pratique si l'état pouvait être partagé.


def test_get_flags_for_admin(client):
    #Vérifie que le rôle 'admin' a accès au flag 'dashboard'.
    response = client.get('/flags?role=admin')
    assert response.status_code == 200
    data = response.get_json()
    assert data['dashboard'] is True

def test_get_flags_for_user_without_role(client):
    #Vérifie qu'un utilisateur sans rôle spécifique n'a pas accès au 'dashboard'.
    response = client.get('/flags?role=user')
    assert response.status_code == 200
    data = response.get_json()
    assert data['dashboard'] is False

def test_get_flags_for_no_role_provided(client):
    #Vérifie le comportement quand aucun rôle n'est fourni.
    response = client.get('/flags')
    assert response.status_code == 200
    data = response.get_json()
    assert data['dashboard'] is False

def test_get_flags_for_public_feature_when_disabled(client):
    #Vérifie qu'un flag public mais désactivé n'est pas accessible.
    # 'beta-feature' est public (roles=[]) mais enabled=False
    response = client.get('/flags?role=any_user')
    assert response.status_code == 200
    data = response.get_json()
    assert data['beta-feature'] is False

def test_get_all_flags(client):
    #Vérifie que l'endpoint /admin/flags retourne bien tous les flags.
    response = client.get('/admin/flags')
    assert response.status_code == 200
    data = response.get_json()
    assert "dashboard" in data
    assert "beta-feature" in data
    assert data["dashboard"]["roles"] == ["admin", "sre"]

def test_create_new_flag(client):
    #Teste la création d'un nouveau feature flag.
    new_flag_data = {
        "enabled": True,
        "description": "Un tout nouveau flag de test.",
        "roles": ["tester"]
    }
    response = client.post(
        '/admin/flags/new-test-flag',
        data=json.dumps(new_flag_data),
        content_type='application/json'
    )
    assert response.status_code == 201  # 201 Created
    data = response.get_json()
    assert data['description'] == "Un tout nouveau flag de test."

    # Vérifions qu'il a bien été ajouté
    response_get = client.get('/admin/flags')
    all_flags = response_get.get_json()
    assert "new-test-flag" in all_flags

def test_update_existing_flag(client):
    #Teste la mise à jour d'un flag existant.
    update_data = {
        "enabled": True,
        "description": "Description mise à jour.",
        "roles": ["admin", "sre", "dev"]
    }
    response = client.post(
        '/admin/flags/dashboard',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 200  # 200 OK
    data = response.get_json()
    assert data['description'] == "Description mise à jour."
    assert "dev" in data['roles']

def test_toggle_flag(client):
    #Teste l'activation/désactivation d'un flag existant.
    # D'abord, s'assurer que le flag 'beta-feature' est désactivé
    response = client.get('/admin/flags')
    assert response.status_code == 200
    data = response.get_json()
    assert data['beta-feature']['enabled'] is False

    # Activer le flag
    response_toggle = client.post('/admin/toggle/beta-feature')
    assert response_toggle.status_code == 200
    data_toggle = response_toggle.get_json()

    #verification de l'etat du flag
    assert data_toggle['enabled'] is True