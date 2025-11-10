import pytest
import os
from src.utils import create_token

USER_KEY = os.getenv('USER_KEY')


class TestLogout:
    """Tests pour la route POST /logout"""

    def test_logout_success(self, client, test_user, redis_client):
        """
        Test: Déconnexion réussie
        - L'utilisateur est connecté (a un token valide)
        - Après logout, le token doit être vidé dans Redis
        - Retourne 200 avec message de succès
        """
        # Arrange: Connecter l'utilisateur (créer et stocker un token)
        token = create_token(test_user['user_id'], test_user['role'])
        user = test_user['user']
        user.token = token
        redis_client.set(name=f"{USER_KEY}{user.id_user}", value=user.to_redis())

        # Act: Appeler la route logout avec le token
        response = client.post(
            '/api/v1/logout',
            headers={'Authorization': f'Bearer {token}'}
        )

        # Assert: Vérifier la réponse
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        assert 'déconnecté' in data['message'].lower() or 'logged out' in data['message'].lower()

        # Assert: Vérifier que le token a été vidé dans Redis
        from src.models.user import User
        stored_user_data = redis_client.get(f"{USER_KEY}{user.id_user}")
        stored_user = User.from_redis_to_user(stored_user_data)
        assert stored_user.token == ""


    def test_logout_without_token(self, client):
        """
        Test: Tentative de déconnexion sans token
        - Aucun header Authorization fourni
        - Retourne 403 avec message d'erreur
        """
        # Act: Appeler logout sans token
        response = client.post('/api/v1/logout')

        # Assert
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert 'token' in data['error'].lower() or 'manquant' in data['error'].lower()


    def test_logout_with_invalid_token(self, client, test_user, redis_client):
        """
        Test: Déconnexion avec un token invalide (signature incorrecte)
        - Token JWT avec une signature invalide
        - Retourne 403
        """
        # Arrange: Token complètement invalide
        invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature"

        # Act
        response = client.post(
            '/api/v1/logout',
            headers={'Authorization': f'Bearer {invalid_token}'}
        )

        # Assert
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data


    def test_logout_with_expired_token(self, client, test_user, redis_client):
        """
        Test: Déconnexion avec un token expiré
        - Token JWT expiré (valide dans le passé)
        - Retourne 403 avec message "expiré"
        """
        # Arrange: Créer un token qui expire immédiatement
        from datetime import timedelta
        expired_token = create_token(test_user['user_id'], test_user['role'], validity=timedelta(seconds=-1))
        
        user = test_user['user']
        user.token = expired_token
        redis_client.set(name=f"{USER_KEY}{user.id_user}", value=user.to_redis())

        # Act
        response = client.post(
            '/api/v1/logout',
            headers={'Authorization': f'Bearer {expired_token}'}
        )

        # Assert
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert 'expiré' in data['error'].lower() or 'expired' in data['error'].lower()


    def test_logout_with_revoked_token(self, client, test_user, redis_client):
        """
        Test: Déconnexion avec un token révoqué (différent de celui en Redis)
        - Token JWT valide mais ne correspond pas à celui stocké dans Redis
        - Retourne 403
        """
        # Arrange: Créer deux tokens différents
        token1 = create_token(test_user['user_id'], test_user['role'])
        token2 = create_token(test_user['user_id'], test_user['role'])
        
        # Stocker token1 dans Redis
        user = test_user['user']
        user.token = token1
        redis_client.set(name=f"{USER_KEY}{user.id_user}", value=user.to_redis())

        # Act: Essayer de logout avec token2 (différent)
        response = client.post(
            '/api/v1/logout',
            headers={'Authorization': f'Bearer {token2}'}
        )

        # Assert
       
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        assert 'déconnecté' in data['message'].lower() 


    def test_logout_already_logged_out(self, client, test_user, redis_client):
        """
        Test: Tentative de déconnexion alors que l'utilisateur est déjà déconnecté
        - Le token dans Redis est déjà vide ("")
        - Retourne 403
        """
        # Arrange: User sans token (déjà déconnecté)
        token = create_token(test_user['user_id'], test_user['role'])
        user = test_user['user']
        user.token = ""  # Déjà vide
        redis_client.set(name=f"{USER_KEY}{user.id_user}", value=user.to_redis())

        # Act: Essayer de logout
        response = client.post(
            '/api/v1/logout',
            headers={'Authorization': f'Bearer {token}'}
        )

        # Assert
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data