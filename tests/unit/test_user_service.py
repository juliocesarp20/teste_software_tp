import pytest
from unittest.mock import Mock
from repository.user_repository import UserRepository
from model.currency import Currency
from model.user import User
from model.account import Account
from services.user_service import UserService , UserNotFoundException, \
MailInvalidException, AgeInvalidException
class MockCurrency(Currency):
    def __init__(self):
        super().__init__(1.0, "MockCurrency1")

class MockCurrency2(Currency):
    def __init__(self):
        super().__init__(1.0, "MockCurrency2")

@pytest.fixture
def user_repository_instance():
    return Mock()

@pytest.fixture
def user_service(user_repository_instance):
    return UserService(user_repository_instance)

def test_create_user(user_service, user_repository_instance):
    user_service.create_user("Joao Silva", "senha123", "joao.silva@example.com", "1985-05-10",
                             currency=MockCurrency())
    user_repository_instance.get_user_by_id.return_value = User(1,"Joao Silva", "senha123", "joao.silva@example.com", "1985-05-10",None)
    assert user_service.get_user_by_id(1).username == "Joao Silva"
    user_repository_instance.create_user.assert_called_once()

def test_create_user_invalid_email(user_service, user_repository_instance):
    with pytest.raises(MailInvalidException, match="Invalid email format"):
        user_service.create_user(None, "senha123", "invalid_email", "1990-01-01",
                                  currency=MockCurrency())

def test_create_user_age_requirement_not_met(user_service, user_repository_instance):
    with pytest.raises(AgeInvalidException, match="Age requirement of 18 years old not met"):
        user_service.create_user("John Doe", "password123", "john.doe@example.com", "2023-01-01",
                                  currency=MockCurrency())

def test_delete_user(user_service, user_repository_instance):
    user_id = user_service.create_user("Joao Silva", "senha123",
                                                   "joao.silva@example.com", "1985-05-10",
                                                   currency=MockCurrency())
    user_service.delete_user(user_id)

    user_repository_instance.delete_user.assert_called_once()

def test_edit_username(user_service, user_repository_instance):
    user_id = user_repository_instance.create_user("Joao Silva", "senha123",
                                                   "joao.silva@example.com", "1985-05-10",
                                                   currency=MockCurrency())
    user_service.edit_user(user_id, new_username="Joao Silveira Silvio")
    user_repository_instance.edit_user.assert_called_once()

def test_edit_user_no_changes(user_service, user_repository_instance):
    user_id = user_repository_instance.create_user("Joao Silva", "senha123",
                                                   "joao.silva@example.com", "1985-05-10",
                                                   currency=MockCurrency())
    user_repository_instance.edit_user.return_value = True
    edited = user_service.edit_user(user_id, "Joao Silva")
    assert edited == True
    user_repository_instance.create_user.assert_called_once()

def test_user_not_found(user_service, user_repository_instance):
    user_repository_instance.get_user_by_id.return_value = False
    with pytest.raises(UserNotFoundException, match="User with ID 2 not found"):
        user_service.get_user_by_id(2)

def test_edit_user_invalid_email(user_service, user_repository_instance):
    user_id = user_repository_instance.create_user("John Doe", "password123",
                                                   "john.doe@example.com", "1990-01-01",
                                                   currency=MockCurrency())
    with pytest.raises(MailInvalidException, match="Invalid email format"):
        user_service.edit_user(user_id, new_email="invalid_email")

def test_edit_user_invalid_birth_date(user_service, user_repository_instance):
    user_id = user_repository_instance.create_user("John Doe", "password123",
                                                   "john.doe@example.com", "1990-01-01",
                                                   currency=MockCurrency())
    with pytest.raises(AgeInvalidException, match="Age requirement of 18 years old not met"):
        user_service.edit_user(user_id, new_birth_date="2015-02-10")

def test_get_users(user_service, user_repository_instance):
    mock_currency1 = MockCurrency()
    mock_currency2 = MockCurrency2()

    user_repository_instance.filter_by_currency.return_value = [
        User(1,"User1", "password123",
                                                 "user1@example.com", "1990-01-01",
                                                 Account(50,mock_currency1)),
        User(2,"User1", "password123",
                                                 "user1@example.com", "1990-01-01",
                                                 Account(50,mock_currency1)),
        User(3,"User1", "password123",
                                                 "user1@example.com", "1990-01-01",
                                                 Account(50,mock_currency1))
    ]
    users_with_2_mock_currencies = user_service.filter_by_currency(mock_currency1)

    users_with_2_mock_currencies = {user.id for user in user_service.filter_by_currency(mock_currency1)}

    assert set(users_with_2_mock_currencies) == {1,2,3}
