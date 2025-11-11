
import pytest
import os
from src.utils import verify_password

BASE_API_URL = os.getenv('BASE_API_URL')
USER_KEY = os.getenv('USER_KEY')
RESET_TOKEN_KEY = os.getenv('RESET_TOKEN_KEY', 'reset:token:')


class TestResetPassword:
    """Tests pour la réinitialisation de mot de passe"""

    def test_reset_password_success(self, client, test_user, redis_client):
        """
        Test: Réinitialisation réussie
        - L'utilisateur demande un reset et reçoit un token
        - Il utilise ce token pour changer son mot de passe
        - Le mot de passe est mis à jour dans Redis
        - Le token de reset est supprimé après utilisation
        """
        # Arrange: Demander un token de reset
        response_forgot = client.post(
            f'{BASE_API_URL}/forgot-password',
            json={'email': test_user['email']}
        )
        reset_token = response_forgot.get_json()['reset_token']
        new_password = "NewPassword456"

        # Act: Réinitialiser le mot de passe
        response = client.post(
            f'{BASE_API_URL}/reset-password',
            json={
                'reset_token': reset_token,
                'new_password': new_password
            }
        )

        # Assert: Réponse OK
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        assert 'succès' in data['message'].lower() or 'success' in data['message'].lower()

        # Assert: Le mot de passe a été mis à jour
        from src.models.user import User
        user_data = redis_client.get(f"{USER_KEY}{test_user['user_id']}")
        user = User.from_redis_to_user(user_data)
        assert verify_password(new_password, user.password)

        # Assert: Le token de reset a été supprimé
        assert redis_client.get(f"{RESET_TOKEN_KEY}{reset_token}") is None


    def test_reset_password_invalid_token(self, client, test_user, redis_client):
        """
        Test: Token de reset invalide
        - Le token n'existe pas dans Redis
        - Retourne 400 ou 403
        """
        # Act
        response = client.post(
            f'{BASE_API_URL}/reset-password',
            json={
                'reset_token': 'invalid-token-123',
                'new_password': 'NewPassword456'
            }
        )

        # Assert
        assert response.status_code in [400, 403]
        data = response.get_json()
        assert 'error' in data


    def test_reset_password_expired_token(self, client, test_user, redis_client):
        """
        Test: Token de reset expiré
        - Le token a expiré (TTL dépassé)
        - Retourne 403
        """
        # Arrange: Créer un token et le supprimer manuellement (simuler expiration)
        response_forgot = client.post(
            f'{BASE_API_URL}/forgot-password',
            json={'email': test_user['email']}
        )
        reset_token = response_forgot.get_json()['reset_token']
        
        # Supprimer le token pour simuler l'expiration
        redis_client.delete(f"{RESET_TOKEN_KEY}{reset_token}")

        # Act
        response = client.post(
            f'{BASE_API_URL}/reset-password',
            json={
                'reset_token': reset_token,
                'new_password': 'NewPassword456'
            }
        )

        # Assert
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert 'expiré' in data['error'].lower() or 'expired' in data['error'].lower() or 'invalide' in data['error'].lower()


    def test_reset_password_weak_password(self, client, test_user, redis_client):
        """
        Test: Nouveau mot de passe trop faible
        - Le mot de passe ne respecte pas les règles (6 chars, 1 maj, 1 minuscule, 1 chiffre)
        - Retourne 400
        """
        # Test avec différents mots de passe invalides
        invalid_passwords = [
            'short',           # Trop court
            'nouppercase1',    # Pas de majuscule
            'NOLOWERCASE1',    # Pas de minuscule
            'NoNumber',        # Pas de chiffre
        ]

        for invalid_password in invalid_passwords:
            # Arrange: Obtenir un nouveau token de reset pour chaque test
            response_forgot = client.post(
                f'{BASE_API_URL}/forgot-password',
                json={'email': test_user['email']}
            )
            reset_token = response_forgot.get_json()['reset_token']
            
            # Act
            response = client.post(
                f'{BASE_API_URL}/reset-password',
                json={
                    'reset_token': reset_token,
                    'new_password': invalid_password
                }
            )

            # Assert
            assert response.status_code == 400, f"Expected 400 for password '{invalid_password}', got {response.status_code}"
            data = response.get_json()
            assert 'error' in data


    def test_reset_password_missing_fields(self, client):
        """
        Test: Champs manquants
        - reset_token ou new_password manquant
        - Retourne 400
        """
        # Test sans reset_token
        response1 = client.post(
            f'{BASE_API_URL}/reset-password',
            json={'new_password': 'NewPassword456'}
        )
        assert response1.status_code == 400
        assert 'error' in response1.get_json()

        # Test sans new_password
        response2 = client.post(
            f'{BASE_API_URL}/reset-password',
            json={'reset_token': 'some-token'}
        )
        assert response2.status_code == 400
        assert 'error' in response2.get_json()


    def test_reset_password_empty_body(self, client):
        """
        Test: Body vide
        - Aucune donnée JSON
        - Retourne 400
        """
        # Act
        response = client.post(f'{BASE_API_URL}/reset-password')

        # Assert
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data


    def test_reset_password_token_single_use(self, client, test_user, redis_client):
        """
        Test: Un token ne peut être utilisé qu'une seule fois
        - Après une réinitialisation réussie
        - Le même token ne peut plus être réutilisé
        """
        # Arrange: Obtenir un token et réinitialiser une première fois
        response_forgot = client.post(
            f'{BASE_API_URL}/forgot-password',
            json={'email': test_user['email']}
        )
        reset_token = response_forgot.get_json()['reset_token']

        # Première réinitialisation
        response1 = client.post(
            f'{BASE_API_URL}/reset-password',
            json={
                'reset_token': reset_token,
                'new_password': 'FirstNewPassword123'
            }
        )
        assert response1.status_code == 200

        # Act: Essayer de réutiliser le même token
        response2 = client.post(
            f'{BASE_API_URL}/reset-password',
            json={
                'reset_token': reset_token,
                'new_password': 'SecondNewPassword456'
            }
        )

        # Assert: Le token ne peut plus être utilisé
        assert response2.status_code == 403
        data = response2.get_json()
        assert 'error' in data