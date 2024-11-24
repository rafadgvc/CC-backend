
def test_get_node(client, auth_token, setup_node):
    """Prueba a obtener un Nodo por ID."""
    node_id = setup_node.get('id')
    response = client.get(
        f'/node/{node_id}',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json.get("id") == node_id
    assert response.json.get("name") == setup_node.get('name')


# def test_get_node_unauthorized(client, setup_node):
#     """Prueba a obtener un Nodo sin autenticación."""
#     node_id = setup_node.get('id')
#     response = client.get(f'/node/{node_id}')
#     assert response.status_code == 401


def test_add_node(client, auth_token, setup_subject, setup_node):
    """Prueba a crear un Nodo."""
    payload = {
        "name": "Mistralton Cave",
        "subject_id": setup_subject.get('id'),
        "parent_id": setup_node.get('id')
    }
    response = client.post(
        '/node',
        headers={"Authorization": f"Bearer {auth_token}"},
        json=payload
    )
    assert response.status_code == 200
    assert response.json.get("name") == "Mistralton Cave"
    assert response.json.get("subject_id") == setup_subject.get('id')


def test_add_node_invalid_data(client, auth_token):
    """Prueba a crear un Nodo con datos inválidos."""
    payload = {"n": "Pledge Grove"}
    response = client.post(
        '/node',
        headers={"Authorization": f"Bearer {auth_token}"},
        json=payload
    )
    assert response.status_code == 400


def test_edit_node(client, auth_token, setup_node):
    """Prueba a editar un Nodo existente."""
    node_id = setup_node.get('id')
    updated_data = {"name": "Giant Chasm"}
    response = client.put(
        f'/node/{node_id}',
        headers={"Authorization": f"Bearer {auth_token}"},
        json=updated_data
    )
    assert response.status_code == 204

    # Verificar los cambios
    response = client.get(
        f'/node/{node_id}',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json.get("name") == updated_data["name"]


def test_delete_node(client, auth_token, setup_node):
    """Prueba a eliminar un Nodo por ID."""
    node_id = setup_node.get('id')
    response = client.delete(
        f'/node/{node_id}',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 204

    # Verificar que el nodo ya no existe
    response = client.get(
        f'/node/{node_id}',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 404


# def test_delete_node_unauthorized(client, setup_node):
#     """Prueba eliminar un Nodo sin autenticación."""
#     node_id = setup_node.get('id')
#     response = client.delete(f'/node/{node_id}')
#     assert response.status_code == 401


def test_get_subjects_nodes(client, auth_token, setup_subject, setup_node):
    """Prueba a obtener la lista de nodos asociados a una asignatura."""
    subject_id = setup_subject.get('id')
    response = client.get(
        f'/node/list/{subject_id}',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert len(response.json.get("items", [])) > 0
    assert response.json.get("items")[0].get("subject_id") == subject_id
