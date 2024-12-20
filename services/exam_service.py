from flask import send_file, jsonify
from flask_jwt_extended import jwt_required

from models.exam.exam import Exam
from models.exam.exam_schema import ExamSchema, FullExamSchema, ExamListSchema, SectionSchema, CompareExamsSchema
from flask_smorest import Blueprint, abort
from db.versions.db import session
from models.question.question_schema import QuestionListSchema, QuestionExtendedListSchema
from utils.common_schema import PaginationSchema

blp = Blueprint("Exam", __name__, url_prefix="/exam")
SESSION = session


@blp.route('<int:id>', methods=["GET"])
@jwt_required()
@blp.response(200, FullExamSchema)
def get_exam(id):
    """ Returns exam
    """
    try:

        return Exam.get_exam(
            SESSION,
            id=id
        )
    except Exception as e:
        abort(400, message=str(e))


@blp.route('', methods=["POST"])
@jwt_required()
@blp.arguments(ExamSchema)
@blp.response(200, FullExamSchema)
def add_exam(exam_data):
    """ Creates an exam and adds it to the database
    """
    try:

        exam = FullExamSchema().load(exam_data)
        question_ids = exam_data.pop('question_ids', [])
        new_exam = Exam.insert_exam(
            session=SESSION,
            title=exam.get('title'),
            subject_id=exam.get('subject_id'),
            questions=exam.get('questions').get('items'),
        )

        return new_exam
    except Exception as e:
        abort(400, message=str(e))


@blp.route('/list/<int:subject_id>', methods=["GET"])
@jwt_required()
@blp.arguments(PaginationSchema, location='query')
@blp.response(200, ExamListSchema)
def get_subject_exams(pagination_params, subject_id):
    """ Returns list of exams in a subject
    """
    return Exam.get_subject_exams(
        SESSION,
        limit=pagination_params.get('limit', None),
        offset=pagination_params.get('offset', 0),
        subject_id=subject_id
    )

@blp.route('/select-questions', methods=["GET"])
@jwt_required()
@blp.arguments(SectionSchema, location='query')
@blp.response(200, QuestionExtendedListSchema)
def select_nodes_questions(section_data):
    """ Returns questions depending on a few parameters
    """
    return Exam.get_questions_to_select(
        SESSION,
        node_ids=section_data.get('node_ids'),
        time=section_data.get('time', None),
        difficulty=section_data.get('difficulty', None),
        repeat=section_data.get('repeat', None),
        type=section_data.get('type', None),
        parametrized=section_data.get('parametrized', None),
        question_number=section_data.get('question_number', None),
        exclude_ids=section_data.get('exclude_ids', None),

    )


@blp.route('<int:id>', methods=["DELETE"])
@jwt_required()
@blp.response(204)
def delete_exam(id):
    """ Deletes exam
    """
    try:

        Exam.delete_exam(
            SESSION,
            exam_id=id
        )
    except Exception as e:
        abort(400, message=str(e))


@blp.route('/<int:id>/export_aiken', methods=["GET"])
@jwt_required()
def export_exam_to_aiken(id):
    try:
        output_file = f"exam_{id}_aiken.txt"
        Exam.export_exam_to_aiken(SESSION, id, output_file)

        return send_file(output_file, as_attachment=True)
    except Exception as e:
        abort(400, message=str(e))

@blp.route('/<int:id>/export_pdf', methods=["GET"])
@jwt_required()
def export_exam_to_pdf(id):
    try:
        exam_data = Exam.get_exam(SESSION, id)
        if not exam_data:
            abort(404, message='El examen no existe')
        output_file = f"{exam_data['title']}.pdf"
        Exam.export_exam_to_pdf(SESSION, id, output_file)
        return send_file(output_file, as_attachment=True)
    except Exception as e:
        abort(400, message=str(e))

@blp.route('/<int:id>/export_gift', methods=["GET"])
@jwt_required()
def export_exam_to_gift(id):
    try:
        output_file = f"exam_{id}_gift.txt"
        Exam.export_exam_to_gift(SESSION, id, output_file)

        return send_file(output_file, as_attachment=True)
    except Exception as e:
        abort(400, message=str(e))

@blp.route('/<int:id>/export_moodlexml', methods=["GET"])
@jwt_required()
def export_exam_to_moodlexml(id):
    try:
        output_file = f"exam_{id}_moodlexml.xml"
        Exam.export_exam_to_moodlexml(SESSION, id, output_file)

        return send_file(output_file, as_attachment=True)
    except Exception as e:
        abort(400, message=str(e))


@blp.route('/<int:id>/export_odt', methods=["GET"])
@jwt_required()
def export_exam_to_odt(id):
    try:
        output_file = f"exam_{id}.odt"
        Exam.export_exam_to_odt(SESSION, id, output_file)

        return send_file(output_file, as_attachment=True)
    except Exception as e:
        abort(400, message=str(e))



@blp.route('<int:exam_id>', methods=["PUT"])
@jwt_required()
@blp.arguments(FullExamSchema)
@blp.response(200, FullExamSchema)
def edit_exam(exam_data, exam_id):
    """ Updates an exam and returns the updated exam
    """
    try:

        exam = FullExamSchema().load(exam_data)
        updated_exam = Exam.edit_exam(
            session=SESSION,
            exam_id=exam_id,
            title=exam.get('title'),
            questions=exam.get('questions').get('items'),
        )
        return updated_exam
    except Exception as e:
        abort(400, message=str(e))

@blp.route('/exam-questions', methods=["GET"])
@jwt_required()
@blp.arguments(CompareExamsSchema, location='query')
@blp.response(200, QuestionListSchema)
def get_exam_questions(params):
    """ Returns questions from selected exams for a specific subject """
    try:
        return Exam.get_exam_questions(
            SESSION,
            subject_id=params.get('subject_id'),
            exam_ids=params.get('exam_ids')
        )
    except Exception as e:
        abort(400, message=str(e))