from marshmallow import Schema, fields, post_dump, EXCLUDE

from models.answer.answer_schema import AnswerListSchema, AnswerAddListSchema
from models.question_parameter.question_parameter_schema import QuestionParameterListSchema, QuestionParameterSchema


class QuestionExtendedSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    subject_id = fields.Integer()
    node_ids = fields.List(fields.Integer())
    active = fields.Boolean()
    connected = fields.Boolean()
    time = fields.Integer()
    difficulty = fields.Integer()
    type = fields.String()
    parametrized = fields.Boolean(nullable=True)
    exam_id = fields.Integer(nullable=True)
    question_parameters = fields.Nested(QuestionParameterListSchema, allow_none=True, nullable=True)
    class Meta:
        unknown = EXCLUDE

class QuestionSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    subject_id = fields.Integer()
    node_ids = fields.List(fields.Integer())
    active = fields.Boolean()
    connected = fields.Boolean()
    time = fields.Integer()
    difficulty = fields.Integer()
    type = fields.String()
    parametrized = fields.Boolean(nullable=True)
    exam_id = fields.Integer(nullable=True)
    class Meta:
        unknown = EXCLUDE

class QuestionReducedSchema(Schema):
    title = fields.String()
    subject_id = fields.Integer()
    node_ids = fields.List(fields.Integer())
    active = fields.Boolean()
    time = fields.Integer()
    difficulty = fields.Integer()
    type = fields.String()
    section_number = fields.Integer(nullable=True)
    question_parameters = fields.Nested(QuestionParameterListSchema, nullable=True)
    answers = fields.Nested(AnswerAddListSchema, nullable=True)
    class Meta:
        unknown = EXCLUDE

class QuestionListSchema(Schema):
    items = fields.List(fields.Nested(QuestionSchema))
    total = fields.Integer()

    @post_dump(pass_many=True)
    def add_total_questions(self, data, many, **kwargs):
        data['total'] = len(data['items'])
        return data

class QuestionExtendedListSchema(Schema):
    items = fields.List(fields.Nested(QuestionExtendedSchema))
    total = fields.Integer()

    @post_dump(pass_many=True)
    def add_total_questions(self, data, many, **kwargs):
        data['total'] = len(data['items'])
        return data

class FullQuestionSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    subject_id = fields.Integer()
    node_ids = fields.List(fields.Integer())
    active = fields.Boolean()
    connected = fields.Boolean()
    time = fields.Integer()
    difficulty = fields.Integer()
    type = fields.String()
    section_number = fields.Integer()
    group = fields.Integer(nullable=True)
    answers = fields.Nested(AnswerListSchema)
    question_parameters = fields.Nested(QuestionParameterListSchema, nullable=True)
    class Meta:
        unknown = EXCLUDE

class FullQuestionListSchema(Schema):
    items = fields.List(fields.Nested(FullQuestionSchema))
    total = fields.Integer()

    @post_dump(pass_many=True)
    def add_total_questions(self, data, many, **kwargs):
        data['total'] = len(data['items'])
        return data


class ImportQuestionSchema(Schema):
    subject_id = fields.Integer()
    time = fields.Integer()
    difficulty = fields.Integer()

