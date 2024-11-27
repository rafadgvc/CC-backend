

def test_add_exam(client, auth_token, setup_subject, setup_node, setup_question, setup_question_2):
    """Prueba a crear un examen."""
    question1 = setup_question
    question2 = setup_question_2
    node_id = setup_node.get("id")
    payload = {
        "title": "Test Geografía de Teselia",
        "subject_id": setup_subject.get('id'),
        "questions": {
            "items": [
                {
                    "id": question1.get('id'),
                    "title": question1.get('title'),
                    "subject_id": question1.get('subject_id'),
                    "node_ids": [node_id],
                    "active": question1.get('active'),
                    "time": question1.get('time'),
                    "difficulty": question1.get('difficulty'),
                    "type": question1.get('type'),
                    "section_number": 0,
                    "question_parameters": {
                        "items": [],
                        "total": 0
                    },
                    "answers": {
                        "items": [],
                        "total": 0
                    },
                },
                {
                    "id": question2.get('id'),
                    "title": question2.get('title'),
                    "subject_id": question2.get('subject_id'),
                    "node_ids": [node_id],
                    "active": question2.get('active'),
                    "time": question2.get('time'),
                    "difficulty": question2.get('difficulty'),
                    "type": question2.get('type'),
                    "section_number": 0,
                    "question_parameters": {
                        "items": [],
                        "total": 0
                    },
                    "answers": {
                        "items": [],
                        "total": 0
                    }
                }

            ],
            "total": 2
        }
    }
    response = client.post(
        '/exam',
        headers={"Authorization": f"Bearer {auth_token}"},
        json=payload
    )
    assert response.json.get("title") == "Test Geografía de Teselia"
    assert response.json.get("subject_id") == setup_subject.get('id')


def test_get_exam(client, auth_token, setup_exam):
    """Prueba a obtener un examen por ID."""
    exam_id = setup_exam.get('id')
    response = client.get(
        f'/exam/{exam_id}',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json.get("id") == exam_id
    assert "questions" in response.json



def test_delete_exam(client, auth_token, setup_exam):
    """Prueba a eliminar un examen por ID."""
    exam_id = setup_exam.get('id')
    response = client.delete(
        f'/exam/{exam_id}',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 204


def test_select_nodes_questions(client, auth_token, setup_node):
    """Prueba a seleccionar preguntas basadas en parámetros."""
    payload = {
        "node_ids": [setup_node.get('id')],
        "time": 60,
        "difficulty": 3,
        "repeat": False,
        "type": "desarrollo",
        "parametrized": False,
        "question_number": 5,
        "exclude_ids": []
    }
    response = client.get(
        '/exam/select-questions',
        headers={"Authorization": f"Bearer {auth_token}"},
        query_string=payload
    )
    assert response.status_code == 200
    assert len(response.json.get("items", [])) <= 5


def test_get_exam_questions(client, auth_token, setup_subject, setup_exam):
    """Prueba a obtener preguntas de un examen específico."""
    payload = {
        "subject_id": setup_subject.get('id'),
        "exam_ids": [setup_exam.get('id')]
    }
    response = client.get(
        '/exam/exam-questions',
        headers={"Authorization": f"Bearer {auth_token}"},
        query_string=payload
    )
    assert response.status_code == 200
    assert len(response.json.get("items", [])) > 0