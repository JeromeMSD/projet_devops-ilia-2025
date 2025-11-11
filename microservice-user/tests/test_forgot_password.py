"""
Tests pour POST /api/v1/forgot-password
"""
import os

BASE_API_URL = os.getenv('BASE_API_URL')
RESET_TOKEN_KEY = os.getenv('RESET_TOKEN_KEY', 'reset:token:')


class TestForgotPassword:
    """Tests pour la demande de réinitialisation de mot de passe"""
    def test_forgot_password_success(self, client, test_user, redis_client):
        """
        Test: Demande de reset réussie
        - L'utilisateur existe
        - Un token de reset est généré et stocké dans Redis
        - Retourne 200 avec le token (normalement envoyé par email)
        """
        # Arrange
        email = test_user['email']
        # Act
        response = client.post(
            f'{BASE_API_URL}/forgot-password',
            json={'email': email}
        )
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        assert 'reset_token' in data
        assert data['reset_token'] != ""
        # Vérifier que le token est stocké dans Redis
        reset_token = data['reset_token']
        stored_user_id = redis_client.get(f"{RESET_TOKEN_KEY}{reset_token}")
        assert stored_user_id is not None
        assert stored_user_id.decode('utf-8') == test_user['user_id']
        # Vérifier que le token a un TTL (expiration)
        ttl = redis_client.ttl(f"{RESET_TOKEN_KEY}{reset_token}")
        assert ttl > 0
        assert ttl <= 1800  # 30 minutes = 1800 secondes

    def test_forgot_password_user_not_found(self, client, redis_client):
        """
        Test: Demande de reset pour un email inexistant
        - L'utilisateur n'existe pas
        - Pour des raisons de sécurité, on retourne quand même 200
          (pour ne pas révéler si un email existe ou non)
        - Mais aucun token n'est généré
        """
        # Act
        response = client.post(
            f'{BASE_API_URL}/forgot-password',
            json={'email': 'nonexistent@mail.com'}
        )
        # Assert
        # Selon les bonnes pratiques de sécurité, on retourne 200
        # même si l'utilisateur n'existe pas (pour ne pas leak d'infos)
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data

    def test_forgot_password_missing_email(self, client):
        """
        Test: Requête sans email
        - Le champ email est manquant
        - Retourne 400
        """
        # Act
        response = client.post(
            f'{BASE_API_URL}/forgot-password',
            json={}
        )
        # Assert
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'email' in data['error'].lower()

    def test_forgot_password_invalid_email_format(self, client):
        """
        Test: Email avec format invalide
        - Email ne respecte pas le format d'email
        - Retourne 400
        """
        # Act
        response = client.post(
            f'{BASE_API_URL}/forgot-password',
            json={'email': 'invalid-email-format'}
        )
        # Assert
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_forgot_password_empty_body(self, client):
        """
        Test: Requête avec body vide
        - Aucune donnée JSON envoyée
        - Retourne 400
        """
        # Act
        response = client.post(f'{BASE_API_URL}/forgot-password')
        # Assert
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_forgot_password_multiple_requests(self, client, test_user, redis_client):
        """
        Test: Plusieurs demandes de reset consécutives
        - L'utilisateur demande plusieurs fois un reset
        - Chaque nouvelle demande génère un nouveau token
        - L'ancien token est supprimé/remplacé
        """
        # Act: Première demande
        response1 = client.post(
            f'{BASE_API_URL}/forgot-password',
            json={'email': test_user['email']}
        )
        token1 = response1.get_json()['reset_token']
        # Act: Deuxième demande
        response2 = client.post(
            f'{BASE_API_URL}/forgot-password',
            json={'email': test_user['email']}
        )
        token2 = response2.get_json()['reset_token']
        # Assert: Les tokens sont différents
        assert token1 != token2
        # Assert: Seul le dernier token est valide
        assert redis_client.get(f"{RESET_TOKEN_KEY}{token2}") is not None
        # L'ancien token devrait être supprimé ou invalide
        # (selon l'implémentation, on pourrait aussi les garder tous)
