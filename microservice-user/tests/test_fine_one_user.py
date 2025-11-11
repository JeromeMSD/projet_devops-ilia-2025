import pytest
from src.routes.find_one_user import User, UserRepository, UserNotFoundError


def test_get_user_by_id_success():
    """Test recuperer un utilisateur existant"""
    # ARRANGE
    repository = UserRepository()
    user = User(1, "Dupont", "Jean", "admin")
    repository._users[1] = user
    
    # ACT
    result = repository.get_by_id(1)
    
    # ASSERT
    assert result.identifiant == 1
    assert result.nom == "Dupont"
    assert result.prenom == "Jean"
    assert result.role == "admin"


def test_get_user_by_id_not_found():
    """Test recuperer un utilisateur inexistant"""
    # ARRANGE
    repository = UserRepository()
    
    # ACT & ASSERT
    with pytest.raises(UserNotFoundError):
        repository.get_by_id(1)