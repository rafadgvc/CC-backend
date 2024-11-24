
def test_add_question(client, auth_token, setup_subject, setup_node):
    """Prueba a crear una pregunta."""
    payload = {
        "title": "¿En que accidente geográfico se sitúa la leyenda de los tres espadachines?",
        "subject_id": setup_subject.get("id"),
        "node_ids": [setup_node.get("id")],
        "active": True,
        "time": 10,
        "difficulty": 4,
        "type": "desarrollo",
        "question_parameters": {
            "items": [],
            "total": 0
        },
        "answers": {
            "items": [],
            "total": 0
        }
    }
    response = client.post(
        '/question',
        headers={"Authorization": f"Bearer {auth_token}"},
        json=payload
    )
    assert response.status_code == 200
    assert response.json.get("title") == "¿En que accidente geográfico se sitúa la leyenda de los tres espadachines?"
    assert response.json.get("subject_id") == setup_subject.get('id')
    assert response.json.get("difficulty") == 4
    assert response.json.get("time") == 10



def test_delete_question(client, auth_token, setup_question):
    """Prueba a eliminar una pregunta por ID."""
    question_id = setup_question.get('id')
    response = client.delete(
        f'/question/{question_id}',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 204


def test_get_user_questions(client, auth_token, setup_question):
    """Prueba a listar las preguntas creadas por el usuario."""
    response = client.get(
        '/question/user-questions',
        headers={"Authorization": f"Bearer {auth_token}"},
        query_string={"limit": 10, "offset": 0}
    )
    assert response.status_code == 200
    assert len(response.json.get("items", [])) > 0


def test_get_subject_questions(client, auth_token, setup_subject, setup_question):
    """Prueba a listar Preguntas asociadas a una Asignatura específica."""
    subject_id = setup_subject.get('id')
    response = client.get(
        f'/question/subject-questions/{subject_id}',
        headers={"Authorization": f"Bearer {auth_token}"},
        query_string={"limit": 10, "offset": 0}
    )
    assert response.status_code == 200
    assert len(response.json.get("items", [])) > 0
    assert response.json.get("items")[0].get("subject_id") == subject_id


def test_get_full_question(client, auth_token, setup_question):
    """Prueba obtener una pregunta completa por ID."""
    question_id = setup_question.get('id')
    response = client.get(
        f'/question/full/{question_id}',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json.get("id") == question_id
    assert "answers" in response.json


def test_disable_question(client, auth_token, setup_question):
    """Prueba desactivar una pregunta."""
    question_id = setup_question.get('id')
    response = client.put(
        f'/question/disable/{question_id}',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json.get("active") is False


def test_update_question(client, auth_token, setup_subject, setup_node, setup_question):
    """Prueba actualizar una pregunta."""
    question_id = setup_question.get('id')
    updated_data = {
        "id": question_id,
        "title": "Explique la leyenda de los dos reyes de Unova",
        "subject_id": setup_subject.get("id"),
        "difficulty": 2,
        "time": 20,
        "parametrized": False,
        "node_ids": [setup_node.get("id")],
        "type": "desarrollo",
        "question_parameters": {
            "items": [],
            "total": 0
        },
        "answers": {
            "items": [],
            "total": 0
        },
        "active": True
    }
    response = client.put(
        f'/question/{question_id}',
        headers={"Authorization": f"Bearer {auth_token}"},
        json=updated_data
    )
    assert response.status_code == 200
    assert response.json.get("title") == "Explique la leyenda de los dos reyes de Unova"
    assert response.json.get("subject_id") == setup_subject.get('id')
    assert response.json.get("difficulty") == 2
    assert response.json.get("time") == 20
