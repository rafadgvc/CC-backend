from typing import Set
from sqlalchemy import Integer, String, select
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.versions.db import Base
from models.subject.subject_schema import SubjectSchema


class Subject(Base):
    __tablename__ = "subject"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    questions: Mapped[Set["Question"]] = relationship(
        back_populates="subject",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __repr__(self):
     return "<Subject(id='%s', name='%s')>" % (self.id, self.name)

    @staticmethod
    def insert_subject(
            session,
            name: str,
            user_id: int,
    ) -> SubjectSchema:
        new_subject = Subject(user_id=user_id, name=name)
        session.add(new_subject)
        session.commit()
        schema = SubjectSchema().dump(new_subject)
        return schema

    @staticmethod
    def get_subject(
            session,
            id: int
    ) -> SubjectSchema:
        query = select(Subject).where(Subject.id == id)
        res = session.execute(query).first()
        return res[0]