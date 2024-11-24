import pytest
from sqlalchemy import text

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
    """Limpia la base de datos en un orden específico."""
    session = create_session()

    # Orden específico de tablas
    ordered_tables = [
        # "result", "exam_question_association", "exam", "answer", "question_parameter", "node_question_association",
        "question", "node", "subject", "user"
    ]  # Nombres de tablas en el orden deseado

    for table_name in ordered_tables:
        if table_name in Base.metadata.tables:
            table = Base.metadata.tables[table_name]
            print(f"Deleting records from table: {table_name}")
            session.execute(table.delete())  # Borra todos los registros de la tabla
            if table_name == "user":
                session.query(User).filter_by(email="ceratopsia@example.com").delete()
                session.commit()

            # Verificar si la tabla está vacía
            sent = "SELECT COUNT(*) FROM " + table_name
            result = session.execute(text(sent)).scalar()
            print(f"Records remaining in {table_name}: {result}")
        else:
            print(f"Table {table_name} not found in metadata!")

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


@pytest.fixture
def setup_subject(client, auth_token):
    """Crea una Asignatura de prueba."""
    payload = {"name": "Geografía"}
    response = client.post(
        '/subject',
        headers={"Authorization": f"Bearer {auth_token}"},
        json=payload
    )
    assert response.status_code == 200
    return response.json


@pytest.fixture
def setup_node(client, auth_token, setup_subject):
    """Crea un Nodo de prueba."""
    payload = {
        "name": "Teselia",
        "subject_id": setup_subject.get('id'),
        "parent_id": -1,
    }
    response = client.post(
        '/node',
        headers={"Authorization": f"Bearer {auth_token}"},
        json=payload
    )
    assert response.status_code == 200
    return response.json


