from conftest import db, example_subject, example_node
from models.question import Question


# Test para crear un Nodo
def test_add_question(db, example_subject, example_node):
    node_ids = []
    node_ids.append(example_node.get("id"))
    question_data = {
        "title": "Explique brevemente la leyenda de los dos reyes de Teselia",
        "subject_id": example_subject.get("id"),
        "difficulty": 4,
        "time": 10,
        "parametrized": False,
        "node_ids": node_ids,
        "type": "desarrollo",
        "answers": [],
        "active": True
    }
    question = Question.insert_question(
        session=db,
        title=question_data.get('title'),
        subject_id=question_data.get('subject_id'),
        difficulty=question_data.get('difficulty'),
        node_ids=question_data.get('node_ids'),
        type=question_data.get('type'),
        answers=question_data.get('answers'),
        question_parameters={"items": []},
        time=question_data.get('time'),
        active=question_data.get('active'),
        parametrized=question_data.get('parametrized')
    )

    assert question.get("title") == question_data.get("title")
    assert question.get("subject_id") == question_data.get("subject_id")
    assert question.get("difficulty") == question_data.get("difficulty")
    assert question.get("time") == question_data.get("time")
    assert question.get("type") == question_data.get("type")


# Test para obtener las preguntas de una asignatura concreta
def test_get_subject_questions(db, example_subject, example_question):
    question = example_question
    questions = Question.get_subject_questions(
        session=db,
        subject_id=example_subject.get("id")
    )

    assert questions.get("total") > 0
    assert questions.get("items")[0].get("title") == question.get("title")

# Test para obtener una pregunta concreta
def test_get_full_question(db, example_question):
    question = Question.get_full_question(
        session=db,
        id=example_question.get("id")
    )

    assert question.get("title") == example_question.get("title")
    assert question.get("time") == example_question.get("time")
    assert question.get("type") == example_question.get("type")
    assert question.get("difficulty") == example_question.get("difficulty")


# Test para editar una pregunta existente
def test_edit_question(db, example_question, example_subject):
    updated_data = {
        "title": "Explique la leyenda de los dos reyes de Unova",
        "subject_id": example_subject.get("id"),
        "difficulty": 2,
        "time": 20,
        "parametrized": False,
        "node_ids": [],
        "type": "desarrollo",
        "answers": [],
        "active": True
    }
    updated_question = Question.update_question(
        session=db,
        title=updated_data.get('title'),
        subject_id=updated_data.get('subject_id'),
        difficulty=updated_data.get('difficulty'),
        node_ids=updated_data.get('node_ids'),
        type=updated_data.get('type'),
        answers_data=updated_data.get('answers'),
        question_parameters_data=updated_data.get('question_parameters', {}).get('items', []),
        time=updated_data.get('time'),
        active=updated_data.get('active'),
        question_id=example_question.get("id")
    )
    assert updated_question.get('title') == updated_data.get('title')
    assert updated_question.get('title') != example_question.get('title')
    assert updated_question.get('difficulty') == updated_data.get('difficulty')
    assert updated_question.get('difficulty') != example_question.get('difficulty')
    assert updated_question.get('time') == updated_data.get('time')
    assert updated_question.get('time') != example_question.get('time')


# Test para desactivar una pregunta activa
def test_disable_question(db, example_question):

    disabled_question = Question.disable_question(
        session=db,
        id=example_question.get("id")
    )
    assert disabled_question.get('title') == example_question.get('title')
    assert disabled_question.get('active') != example_question.get('active')



# Test para eliminar una pregunta
def test_delete_question(db, example_question):
    question = Question.delete_question(
        session=db,
        id=example_question.get("id")
    )
    assert question is None
