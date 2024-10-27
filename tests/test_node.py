from conftest import db, example_subject, example_node
from models.node.node import Node


# Test para crear un Nodo
def test_add_node(db, example_subject, example_node):
    node_data = {
        "name": "Porcelana",
        "subject_id": example_subject.get("id"),
        "parent_id": example_node.get("id")
    }
    node = Node.insert_node(
        session=db,
        name=node_data.get('name'),
        subject_id=node_data.get('subject_id'),
        parent_id=node_data.get('parent_id'),
    )

    assert node.get("name") == node_data.get("name")
    assert node.get("subject_id") == node_data.get("subject_id")
    assert node.get("parent_id") == node_data.get("parent_id")


# Test para obtener los nodos del usuario autenticado
def test_get_subject_nodes(db, example_node, example_subject):
    nodes = Node.get_subject_nodes(
        session=db,
        subject_id=example_subject.get("id")
    )

    assert nodes.get("total") > 0
    assert nodes.get("items")[1].get("name") == example_node.get("name")


# Test para editar un nodo existente
def test_edit_node(db, example_node):
    updated_data = {
        "name": "Unova"
    }
    node = Node.update_node(
        session=db,
        name=updated_data.get('name'),
        id=example_node.get('id')
    )
    assert node.get('name') == updated_data.get('name')
    assert node.get('name') != example_node.get('name')


# Test para eliminar un nodo
def test_delete_node(db, example_node):
    node = Node.delete_node(
        session=db,
        id=example_node.get("id")
    )
    assert node is None
