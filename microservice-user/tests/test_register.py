import pytest
import json
from src.redis_client import get_redis_client
import os

# Constantes des clés pour la vérification
EMAIL_KEY = os.getenv('EMAIL_KEY')
USER_KEY = os.getenv('USER_KEY')


@pytest.fixture
def base_user_data():
    """Données valides pour une inscription réussie."""
    return {
        "firstname": "Jane",
        "lastname": "Doe",
        "email": "jane.doe@example.com",
        "password": "Secure123!",
        "role": "USER"
    }


class TestRegister:
    """Suite de tests pour la route POST /register."""
    
    API_URL = '/api/v1/register' # Route sans préfixe d'API si vous utilisez le Wrapper, sinon utilisez '/api/v1/register'

    # -----------------------------------------------------------
    # SCÉNARIOS DE SUCCÈS (Code 201)
    # -----------------------------------------------------------

    def test_register_success(self, client, redis_client, base_user_data):
        """Teste l'inscription réussie d'un nouvel utilisateur (201 Created)."""
        
        response = client.post(self.API_URL, json=base_user_data)
        assert response.status_code == 201
        
        data = response.get_json()
        assert 'message' in data
        assert 'user' in data
        
        user_info = data['user']
        assert user_info['email'] == base_user_data['email']
        assert 'id_user' in user_info
        
        # 🧪 VÉRIFICATION REDIS : Vérifier l'existence et l'intégrité des clés
        user_id = user_info['id_user']
        
        # 1. Vérification de l'Index Email (Clé type STRING)
        assert redis_client.exists(f"{EMAIL_KEY}{base_user_data['email']}") == 1
        
        # 2. Vérification des Données Utilisateur (Clé type STRING JSON)
        user_data_redis = redis_client.get(f"{USER_KEY}{user_id}")
        assert user_data_redis is not None
        
        # Vérifier que le mot de passe hashé est bien dans Redis (non exposé)
        user_dict = json.loads(user_data_redis.decode('utf-8'))
        assert 'password' in user_dict # Le hash est sous la clé 'password'
        assert user_dict['token'] == "" # Le token doit être vide au départ


    def test_register_duplicate_email(self, client, base_user_data):
        """Teste l'inscription avec un email déjà existant (409 Conflict)."""
        
        # 1. Inscrire une première fois (doit réussir)
        client.post(self.API_URL, json=base_user_data)
        assert response.status_code == 201
        
        # 2. Tenter d'inscrire à nouveau avec le même email
        response = client.post(self.API_URL, json=base_user_data)
        print(response)
        
        assert response.status_code == 409
        data = response.get_json()
        assert 'error' in data
        assert 'déjà existe' in data['error']


    # -----------------------------------------------------------
    # SCÉNARIOS D'ÉCHEC DE VALIDATION (Code 400)
    # -----------------------------------------------------------

    @pytest.mark.parametrize("field, value", [
        ("firstname", None), 
        ("lastname", "Test"),
        ("email", "invalid-email"),
        ("password", "court1"), # Trop court
        ("password", "sanschiffre"), # Manque chiffre
        ("password", "SANSMAJ1"), # Manque minuscule (si on suppose qu'il faut maj/min) - Base sur votre RegEx
        ("role", "GUEST") # Rôle invalide
    ])
    def test_register_invalid_data(self, client, base_user_data, field, value):
        """Teste différentes erreurs de validation des champs."""
        
        # Copier les données valides et injecter la valeur invalide
        invalid_data = base_user_data.copy()
        invalid_data[field] = value
        
        # Si le champ est None, nous le retirons du dictionnaire pour simuler un champ manquant
        if value is None:
             del invalid_data[field] 
             
        response = client.post(self.API_URL, json=invalid_data)
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        
        # Vérifier que le message d'erreur mentionne le champ en question
        if value is None:
            assert f'{field} manquant' in data['error'] 
        else:
            assert 'valide' in data['error'] or 'role valide' in data['error']


    def test_register_empty_body(self, client):
        """Teste l'inscription avec un body vide (None)."""
        
        response = client.post(self.API_URL, json={})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'requis' in data['error']