from models.user.user import User
import bcrypt

# Test para crear un usuario a través del modelo
def test_insert_user(db):
    email = "test@example.com"
    name = "Test User"
    password = "testpassword"

    result = User.insert_user(session=db, email=email, name=name, password=password)

    assert result['email'] == email
    assert result['name'] == name
    assert result['password'] != password

# Prueba para obtener un usuario por ID
def test_get_user(db):
    email = "test2@example.com"
    name = "Another User"
    password = "testpassword"

    user_schema = User.insert_user(session=db, email=email, name=name, password=password)

    user = User.get_user(session=db, id=user_schema['id'])

    assert user.email == email
    assert user.name == name

def test_get_user_by_email_and_password(db):
    email = "login_test@example.com"
    name = "Login User"
    password = "securepassword"

    User.insert_user(session=db, email=email, name=name, password=password)

    user = User.get_user_by_email(session=db, email=email)
    assert user.email == email
    assert bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))

# Prueba para la ruta /user/signup (POST)
def test_signup_route(client, db):
    user_data = {
        "email": "felis@example.com",
        "name": "Felis Catus",
        "password": "Fl0R4L 7r1cK"
    }

    response = client.post("/user/signup", json=user_data)
    assert response.status_code == 200

    data = response.get_json()
    assert data["email"] == user_data["email"]
    assert data["name"] == user_data["name"]
