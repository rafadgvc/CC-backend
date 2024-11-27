from models.exam.exam import Exam


def test_add_exam(db, example_subject, example_node, example_question, example_exam):
    node_ids = []
    node_ids.append(example_node.get("id"))
    question_data = {
        "id": example_question.get("id"),
        "title": "Explique brevemente la leyenda de los dos reyes de Teselia",
        "subject_id": example_subject.get("id"),
        "difficulty": 4,
        "time": 10,
        "parametrized": False,
        "node_ids": node_ids,
        "type": "desarrollo",
        "answers": [],
        "question_parameters": [],
        "active": True,
        "section_number": 1
    }
    questions = []
    questions.append(question_data)
    exam_data = {
        "title": "Examen de repaso de Historia",
        "questions": questions,
        "subject_id": example_subject.get("id")
    }
    exam = Exam.insert_exam(
        session=db,
        title=exam_data.get('title'),
        questions=exam_data.get('questions'),
        subject_id=exam_data.get('subject_id')
    )
    assert exam.get("title") == example_exam.get("title")
    assert exam.get("questions").get('total') == example_exam.get("questions").get('total')


# Test para obtener los exámenes de una asignatura concreta
def test_get_subject_exams(db, example_subject, example_exam):
    exam = example_exam
    exams = Exam.get_subject_exams(
        session=db,
        subject_id=example_subject.get("id")
    )
    assert exams.get("total") > 0
    assert exams.get("items")[0].get("title") == exam.get("title")

# Test para obtener un examen concreto
def test_get_exam(db, example_exam):
    exam = Exam.get_exam(
        session=db,
        id=example_exam.get("id")
    )

    assert exam.get("title") == example_exam.get("title")
    assert exam.get("questions").get('total') == example_exam.get("questions").get('total')


# Test para editar un examen existente
def test_edit_exam(db, example_exam, example_question, example_node, example_subject):
    node_ids = []
    node_ids.append(example_node.get("id"))
    question_data = {
        "id": example_question.get("id"),
        "title": "Explique brevemente la leyenda de los dos reyes de Teselia",
        "subject_id": example_subject.get("id"),
        "difficulty": 4,
        "time": 10,
        "parametrized": False,
        "node_ids": node_ids,
        "type": "desarrollo",
        "answers": [],
        "question_parameters": [],
        "active": True,
        "section_number": 1
    }
    questions = []
    questions.append(question_data)
    updated_data = {
        "title": "Examen de repaso de Historia Regional",
        "questions": questions,
        "subject_id": example_subject.get("id")
    }
    updated_exam = Exam.edit_exam(
        session=db,
        title=updated_data.get('title'),
        questions=updated_data.get('questions'),
        exam_id=example_exam.get('id')
    )
    assert updated_exam.get("title") == updated_data.get("title")
    assert updated_exam.get("title") != example_exam.get("title")


# Test para eliminar un examen
def test_delete_exam(db, example_exam):
    exam = Exam.delete_exam(
        session=db,
        exam_id=example_exam.get("id")
    )
    assert exam is None
