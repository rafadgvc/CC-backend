import csv

import pandas as pd
from flask import abort
from sqlalchemy import Integer, String, select, ForeignKey, and_, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
from db.versions.db import Base
from models.result.result_schema import ResultSchema

from utils.utils import get_current_user_id


class Result(Base):
    __tablename__ = "result"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("question.id"))
    exam_id: Mapped[int] = mapped_column(Integer, ForeignKey("exam.id"))
    time: Mapped[int] = mapped_column(String, nullable=False)
    taker: Mapped[int] = mapped_column(String, nullable=False)
    points: Mapped[int] = mapped_column(Integer, CheckConstraint('points >= -1 AND points <= 1'), nullable=False)

    # Relaciones
    created: Mapped["User"] = relationship(back_populates="results")
    question: Mapped["Question"] = relationship(back_populates="results")
    exam: Mapped["Exam"] = relationship(back_populates="results")

    def __repr__(self):
        return "<Result(id='%s', taker='%s')>" % (self.id, self.taker)

    @staticmethod
    def insert_result(
            session,
            question_id: int,
            exam_id: int,
            time: int,
            points: int,
            taker: int,
    ) -> ResultSchema:
        from models.associations.associations import exam_question_association
        from models.result.result_schema import ResultSchema
        from models.exam.exam import Exam

        user_id = get_current_user_id()
        query = select(Exam).join(exam_question_association).where(
            and_(
                exam_question_association.c.question_id == question_id,
                exam_question_association.c.exam_id == exam_id
            )
        )
        association = session.execute(query).first()

        if not association:
            abort(400, "La pregunta no pertenece al examen.")

        new_result = Result(
            created_by=user_id,
            question_id=question_id,
            exam_id=exam_id,
            points=points,
            time=time,
            taker=taker
        )

        session.add(new_result)
        session.commit()
        schema = ResultSchema()

        return schema.dump(
            {
                "id": new_result.id,
                "question_id": new_result.question_id,
                "exam_id": new_result.exam_id,
                "time": new_result.time,
                "taker": new_result.taker,
                "points": new_result.points,
            }
        )

    @staticmethod
    def insert_results_from_csv(session, file) -> List[ResultSchema]:

        try:

            df = pd.read_csv(file, dtype='object')

            results = []
            for index, row in df.iterrows():

                question_id = int(row['question_id'])
                exam_id = int(row['exam_id'])
                points = int(row['points'])
                taker = int(row['taker'])
                time = int(row['time'])

                result = Result.insert_result(
                    session=session,
                    question_id=question_id,
                    exam_id=exam_id,
                    points=points,
                    taker=taker,
                    time=time
                )
                results.append(result)
            return results
        except Exception as e:
            abort(400, message=str(e))
