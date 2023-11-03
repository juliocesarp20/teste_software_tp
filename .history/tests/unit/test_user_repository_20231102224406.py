import pytest
from .repository.user_repository import UserRepository, UserNotFoundException, \
    MailInvalidException, AgeInvalidException
from model.currency import Currency


class MockCurrency(Currency):
    def __init__(self):
        super().__init__(1.0, "MockCurrency1")


class MockCurrency2(Currency):
    def __init__(self):
        super().__init__(1.0, "MockCurrency2")


@pytest.fixture
def user_repository_instance():
    return UserRepository()


def test_create_user(user_repository_instance):
    user_repository_instance.create_user("Joao Silva", "senha123",
                                         "joao.silva@example.com", "1985-05-10",
                                         currency=MockCurrency())
    assert len(user_repository_instance.users) == 1


def test_create_user_invalid_email(user_repository_instance):
    with pytest.raises(MailInvalidException) as exc_info:
        user_repository_instance.create_user(None, "senha123",
                                             "invalid_email", "1990-01-01",
                                             currency=MockCurrency())
    assert str(exc_info.value) == "Invalid email format"


def test_create_user_age_requirement_not_met(user_repository_instance):
    with pytest.raises(AgeInvalidException) as exc_info:
        user_repository_instance.create_user("John Doe", "password123",
                                             "john.doe@example.com", "2023-01-01",
                                             currency=MockCurrency())
    assert str(exc_info.value) == "Age requirement of 18 years old not met"


def test_delete_user(user_repository_instance):
    user_id = user_repository_instance.create_user("Joao Silva", "senha123",
                                                   "joao.silva@example.com",
                                                   "1985-05-10",
                                                   currency=MockCurrency())
    user_repository_instance.delete_user(user_id)
    assert len(user_repository_instance.users) == 0


def test_edit_username(user_repository_instance):
    user_id = user_repository_instance.create_user("Joao Silva", "senha123",
                                                   "joao.silva@example.com",
                                                   "1985-05-10",
                                                   currency=MockCurrency())
    user_repository_instance.edit_user(user_id, new_username="Joao Silveira Silvio")
    user = user_repository_instance.get_user_by_id(user_id)
    assert user.username == "Joao Silveira Silvio"


def test_edit_user_no_changes(user_repository_instance):
    user_id = user_repository_instance.create_user("Joao Silva", "senha123",
                                                   "joao.silva@example.com",
                                                   "1985-05-10",
                                                   currency=MockCurrency())
    user_repository_instance.edit_user(user_id, "Joao Silva")
    user = user_repository_instance.get_user_by_id(user_id)
    assert user.username == "Joao Silva"


def test_edit_user_not_found(user_repository_instance):
    user_repository_instance.create_user("Joao Silva", "senha123",
                                         "joao.silva@example.com", "1985-05-10",
                                         currency=MockCurrency())
    with pytest.raises(UserNotFoundException) as exc_info:
        user_repository_instance.edit_user(2, new_username="Joao Silveira Silvio")
    assert str(exc_info.value) == "User with ID 2 not found"


def test_edit_user_invalid_email(user_repository_instance):
    user_id = user_repository_instance.create_user("John Doe", "password123",
                                                   "john.doe@example.com",
                                                   "1990-01-01",
                                                   currency=MockCurrency())
    with pytest.raises(MailInvalidException) as exc_info:
        user_repository_instance.edit_user(user_id, new_email="invalid_email")
    assert str(exc_info.value) == "Invalid email format"


def test_edit_user_invalid_birth_date(user_repository_instance):
    user_id = user_repository_instance.create_user("John Doe", "password123",
                                                   "john.doe@example.com",
                                                   "1990-01-01",
                                                   currency=MockCurrency())
    with pytest.raises(AgeInvalidException) as exc_info:
        user_repository_instance.edit_user(user_id, new_birth_date="2015-02-10")
    assert str(exc_info.value) == "Age requirement of 18 years old not met"


def test_get_users(user_repository_instance):
    # Arrange
    mock_currency1 = MockCurrency()
    mock_currency2 = MockCurrency2()
    user1 = user_repository_instance.create_user("User1", "password123",
                                                 "user1@example.com", "1990-01-01",
                                                 currency=mock_currency1)
    user2 = user_repository_instance.create_user("User2", "password456",
                                                 "user2@example.com", "1995-02-15",
                                                 currency=mock_currency2)
    user3 = user_repository_instance.create_user("User3", "password789",
                                                 "user3@example.com", "1985-05-10",
                                                 currency=mock_currency1)
    user4 = user_repository_instance.create_user("User4", "password321",
                                                 "user4@example.com", "1998-12-20",
                                                 currency=mock_currency2)
    user5 = user_repository_instance.create_user("User5", "password654",
                                                 "user5@example.com", "1988-06-30",
                                                 currency=mock_currency1)

    users_with_2_mock_currencies = user_repository_instance.get_users_by_currency(
        mock_currency1)

    users_with_2_mock_currencies = {user.id for user in
                                    user_repository_instance.get_users_by_currency(
                                        mock_currency1)}

    assert set(users_with_2_mock_currencies) == {user1, user3, user5}
