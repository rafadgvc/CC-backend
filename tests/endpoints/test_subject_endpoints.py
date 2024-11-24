

def test_get_subject(client, auth_token, setup_subject):
    """Prueba obtener un sujeto por ID."""
    subject_id = setup_subject.get('id')
    response = client.get(
        f'/subject/{subject_id}',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json.get("id") == subject_id
    assert response.json.get("name") == setup_subject.get('name')


def test_get_user_subjects(client, auth_token, setup_subject):
    """Prueba obtener las Asignaturas creadas por el usuario."""
    response = client.get(
        '/subject/user-subjects',
        headers={"Authorization": f"Bearer {auth_token}"},
        query_string={"limit": 10, "offset": 0}
    )
    assert response.status_code == 200
    assert len(response.json["items"]) > 0
    assert response.json.get("items")[0].get("id") == setup_subject.get('id')


def test_add_subject(client, auth_token):
    payload = {"name": "Mitología"}
    response = client.post(
        '/subject',
        headers={"Authorization": f"Bearer {auth_token}"},
        json=payload
    )
    assert response.status_code == 200
    assert response.json["name"] == "Mitología"


def test_get_subject_unauthorized(client):
    response = client.get('/subject/1')
    assert response.status_code == 401

def test_delete_subject(client, auth_token, setup_subject):
    """Prueba eliminar una Asignatura por ID."""
    subject_id = setup_subject.get('id')
    response = client.delete(
        f'/subject/{subject_id}',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 204


def test_edit_subject(client, auth_token, setup_subject):
    """Prueba a editar una Asignatura existente."""
    subject_id = setup_subject.get('id')
    updated_data = {"name": "Geografía Regional"}
    response = client.put(
        f'/subject/{subject_id}',
        headers={"Authorization": f"Bearer {auth_token}"},
        json=updated_data
    )
    assert response.status_code == 204

    response = client.get(
        f'/subject/{subject_id}',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json.get("name") == updated_data.get("name")


# def test_edit_subject_unauthorized(client, setup_subject):
#     """Prueba editar una Asignatura sin autenticación."""
#     subject_id = setup_subject.get('id')
#     updated_data = {"name": "Nuevo Nombre No Autenticado"}
#     response = client.put(
#         f'/subject/{subject_id}',
#         json=updated_data
#     )
#     assert response.status_code == 401


def test_edit_subject_invalid_data(client, auth_token, setup_subject):
    """Prueba editar una Asignatura con datos inválidos."""
    subject_id = setup_subject.get('id')
    invalid_data = {"invalid_field": "Valor Invalido"}
    response = client.put(
        f'/subject/{subject_id}',
        headers={"Authorization": f"Bearer {auth_token}"},
        json=invalid_data
    )
    assert response.status_code == 422
