
def test_signup_user(client):
    """Prueba registrar un usuario único."""
    payload = {
        "email": "unique@example.com",
        "name": "Unique User",
        "password": "securepassword"
    }
    response = client.post('/user/signup', json=payload)
    assert response.status_code == 200


def test_signup_duplicate_user(client):
    """Prueba registrar un usuario con email duplicado."""
    payload = {
        "email": "duplicate@example.com",
        "name": "First User",
        "password": "securepassword"
    }
    client.post('/user/signup', json=payload)  # Primer usuario

    # Intento duplicado
    response = client.post('/user/signup', json=payload)
    assert response.status_code == 400  # Debe devolver error por duplicado
