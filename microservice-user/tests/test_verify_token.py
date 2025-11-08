from datetime import timezone

from src.utils import create_token


class TestVerifyToken:
    """Tests pour la route /verify-token"""

    def test_verify_token_success(self, client, test_user, redis_client):
        """Test : Vérification d'un token valide"""
        # D'abord se connecter pour obtenir un token
        login_response = client.post('/login',
                                     json={
                                         'email': test_user['email'],
                                         'password': test_user['password']
                                     }
                                     )
        token = login_response.get_json()['user']['token']

        # Vérifier le token
        response = client.get('/verify-token',
                              headers={'Authorization': f'Bearer {token}'}
                              )

        assert response.status_code == 200
        data = response.get_json()

        assert 'message' in data
        assert data['message'] == 'Utilisateur connecté'
        assert 'user' in data
        assert data['user']['email'] == test_user['email']

    def test_verify_token_missing_token(self, client):
        """Test : Requête sans token"""
        response = client.get('/verify-token')

        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data

    def test_verify_token_invalid_token(self, client):
        """Test : Token JWT invalide"""
        response = client.get('/verify-token',
                              headers={'Authorization': 'Bearer invalid_token_xyz'}
                              )

        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert 'invalide' in data['error'].lower()

    def test_verify_token_revoked(self, client, test_user, redis_client):
        """Test : Token révoqué (vide dans Redis)"""
        # Se connecter
        login_response = client.post('/login',
                                     json={
                                         'email': test_user['email'],
                                         'password': test_user['password']
                                     }
                                     )
        token = login_response.get_json()['user']['token']

        # Révoquer le token (le vider dans Redis)
        from src.models.user import User
        user = User.from_redis_to_user(redis_client.get(test_user['user_id']))
        user.token = ""
        redis_client.set(test_user['user_id'], user.to_redis())

        # Vérifier le token
        response = client.get('/verify-token',
                              headers={'Authorization': f'Bearer {token}'}
                              )

        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert 'révoqué' in data['error'].lower() or 'expiré' in data['error'].lower()


    def test_verify_token_different_token(self, client, test_user, redis_client):
        """Test : Token valide, mais différent de celui stocké"""
        # Se connecter
        login_response = client.post('/login',
                                     json={
                                         'email': test_user['email'],
                                         'password': test_user['password']
                                     }
                                     )

        # Créer un autre token valide
        another_token = create_token(test_user['user_id'])

        # Vérifier avec l'autre token
        response = client.get('/verify-token',
                              headers={'Authorization': f'Bearer {another_token}'}
                              )

        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert 'invalide' in data['error'].lower()



    def test_verify_token_without_bearer(self, client, test_user):
        """Test : Token sans préfixe 'Bearer'"""
        # Se connecter
        login_response = client.post('/login',
                                     json={
                                         'email': test_user['email'],
                                         'password': test_user['password']
                                     }
                                     )
        token = login_response.get_json()['user']['token']

        # Envoyer sans 'Bearer'
        response = client.get('/verify-token',
                              headers={'Authorization': token}
                              )

        # Devrait quand même fonctionner car votre code fait .replace('Bearer ', '')
        assert response.status_code == 200

    def test_verify_token_expired(self, client, test_user, redis_client, monkeypatch):
        """Test : Token expiré"""
        # Créer un token qui expire immédiatement
        import jwt
        from datetime import datetime, timedelta

        payload = {
            'id_user': test_user['user_id'],
            'exp': datetime.now(timezone.utc) - timedelta(seconds=1)  # Déjà expiré
        }
        expired_token = jwt.encode(payload, 'your-secret-key', algorithm='HS256')

        # Stocker le token expiré
        from src.models.user import User
        user = User.from_redis_to_user(redis_client.get(test_user['user_id']))
        user.token = expired_token
        redis_client.set(test_user['user_id'], user.to_redis())

        # Vérifier
        response = client.get('/verify-token',
                              headers={'Authorization': f'Bearer {expired_token}'}
                              )

        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert 'expiré' in data['error'].lower()

        # Vérifier que le token a été nettoyé dans Redis
        user = User.from_redis_to_user(redis_client.get(test_user['user_id']))
        assert user.token == ""


