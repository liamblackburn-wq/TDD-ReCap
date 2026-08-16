from src.models import User


def test_create_apprentice_user():
    user = User.create_user(
        username="test_apprentice",
        password="apprentice123",
        role="apprentice"
    )

    assert user.id is not None
    assert user.username == "test_apprentice"
    assert user.role == "apprentice"

    assert user.password_hash != "apprentice123"
    assert user.check_password("apprentice123") is True

    db_user = User.get_or_none(User.username == "test_apprentice")
    assert db_user is not None


def test_create_admin_user():
    user = User.create_user(
        username="test_admin",
        password="admin123",
        role="admin"
    )

    assert user.id is not None
    assert user.username == "test_admin"
    assert user.role == "admin"

    assert user.password_hash != "admin123"
    assert user.check_password("admin123") is True

    db_user = User.get_or_none(User.username == "test_admin")
    assert db_user is not None