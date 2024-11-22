import pytest
from app import app
from db.versions.db import create_session, Base
from models.user.user import User

@pytest.fixture
def client():
    """Crea un cliente de pruebas para la aplicación Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def setup_test_data():
    """Prepara datos de prueba en la base de datos."""
    session = create_session()
    user = User.insert_user(session, email="test@example.com", name="Test User", password="12345")
    return user


@pytest.fixture(autouse=True)
def clean_database():
    """Limpia la base de datos entre tests."""
    session = create_session()
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())  # Borra todos los registros de cada tabla
    session.commit()


@pytest.fixture
def setup_user():
    """Crea un usuario de prueba en la base de datos."""
    session = create_session()
    user = User.insert_user(
        session=session,
        email="ceratopsia@example.com",
        name="Ceratopsia Cerapoda",
        password="1R0n d3f3n53"
    )
    yield user

    session.query(User).filter_by(email="ceratopsia@example.com").delete()
    session.commit()


@pytest.fixture
def auth_token(client, setup_user):
    """Obtiene un token JWT para usar en los tests."""
    login_payload = {
        "email": "ceratopsia@example.com",
        "password": "1R0n d3f3n53"
    }
    response = client.post('/user/login', json=login_payload)
    assert response.status_code == 200
    return response.json["access_token_cookie"]
