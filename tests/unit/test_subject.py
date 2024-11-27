from models.subject.subject import Subject
from conftest import db, example_user, example_subject

# Test para crear una asignatura
def test_add_subject(db, example_user):
    subject_data = {
        "name": "Geografía"
    }
    subject = Subject.insert_subject(
        session=db,
        name=subject_data['name']
    )

    assert subject["name"] == subject_data["name"]

# Test para obtener las asignaturas del usuario autenticado
def test_get_user_subjects(db, example_subject, example_user):
    subjects = Subject.get_user_subjects(
        session=db
    )

    assert subjects.get("total") > 0
    assert subjects.get("items")[0].get("name") == example_subject.get("name")

# Test para editar una asignatura existente
def test_edit_subject(db, example_subject):
    updated_data = {
        "name": "Geografía Regional"
    }
    subject = Subject.update_subject(
        session=db,
        name=updated_data.get('name'),
        id=example_subject.get('id')
    )
    assert subject.get('name') == updated_data.get('name')
    assert subject.get('name') != example_subject.get('name')

# Test para eliminar una asignatura
def test_delete_subject(db, example_subject):
    subject = Subject.delete_subject(
        session=db,
        id=example_subject.get("id")
    )
    assert subject is None
