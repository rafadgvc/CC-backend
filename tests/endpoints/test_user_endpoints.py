import pytest


def test_signup_user(client):
    """Prueba el signup."""
    payload = {
        "email": "oryctolagus@example.com",
        "name": "oryctolagus Cuniculus",
        "password": "V-CR347e"
    }
    response = client.post('/user/signup', json=payload)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "email, password, expected_status",
    [
        ("ceratopsia@example.com", "1R0n d3f3n53", 200),  # Caso exitoso
        ("ceratopsia@example.com", "Fl45h C4nN0n", 401),  # Contraseña incorrecta
        ("tenebrisvulpes@example.com", "1llU5i0N", 401),  # Usuario inexistente
    ]
)
def test_login(client, setup_user, email, password, expected_status):
    """Prueba el endpoint de login."""
    payload = {"email": email, "password": password}
    response = client.post('/user/login', json=payload)

    assert response.status_code == expected_status

    if expected_status == 200:

        assert "access_token_cookie" in response.json


def test_logout(client, setup_user, auth_token):
    response = client.post(
        '/user/logout',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200


def test_signup_duplicate_user(client):
    """Prueba el signup con email de un usuario existente."""
    payload = {
        "email": "Dopelganger@example.com",
        "name": "Döppel Gänger",
        "password": "N16H7 5H4d3"
    }
    good_response = client.post('/user/signup', json=payload)
    assert good_response.status_code == 200

    response = client.post('/user/signup', json=payload)
    assert response.status_code == 400





