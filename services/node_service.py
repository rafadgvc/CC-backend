from flask_jwt_extended import jwt_required
from models.node.node import Node
from models.node.node_schema import NodeSchema, NodeReducedSchema, NodeListSchema
from flask_smorest import Blueprint, abort
from db.versions.db import session
from models.question.question_schema import FullQuestionListSchema

blp = Blueprint("Node", __name__, url_prefix="/node")
SESSION = session


@blp.route('<int:id>', methods=["GET"])
@jwt_required()
@blp.response(200, NodeSchema)
def get_node(id):
    """ Returns node
    """
    try:

        return Node.get_node(
            SESSION,
            id=id
        )
    except Exception as e:
        if e.code == 404:
            abort(404, message=str(e))
        else:
            abort(400, message=str(e))


@blp.route('', methods=["POST"])
@jwt_required()
@blp.arguments(NodeReducedSchema)
@blp.response(200, NodeSchema)
def add_node(node_data):
    """ Creates a node and adds it to the database
    """
    try:
        return Node.insert_node(
            session=SESSION,
            name=node_data.get('name'),
            subject_id=node_data.get('subject_id', None),
            parent_id=node_data.get('parent_id', None),
        )
    except Exception as e:
        abort(400, message=str(e))


@blp.route('/list/<int:id>', methods=["GET"])
@jwt_required()
@blp.response(200, NodeListSchema)
def get_subjects_nodes(id):
    """ Returns the list of nodes that a subject has
    """
    return Node.get_subject_nodes(
        session=SESSION,
        subject_id=id,
        )


@blp.route('<int:id>', methods=["PUT"])
@jwt_required()
@blp.arguments(NodeSchema)
@blp.response(204, NodeSchema)
def edit_node(node_data, id):
    """ Edits node name
    """
    return Node.update_node(
        SESSION,
        id=id,
        name=node_data.get('name')

    )

@blp.route('<int:id>', methods=["DELETE"])
@jwt_required()
@blp.response(204)
def delete_node(id):
    """ Deletes node
    """
    try:
        Node.delete_node(
            SESSION,
            id=id
        )
    except Exception as e:
        abort(400, message=str(e))
