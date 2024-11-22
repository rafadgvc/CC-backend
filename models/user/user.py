from sqlalchemy import Integer, String, select
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Set

from secret import PASSWORD_SALT

import bcrypt

from db.versions.db import Base
from models.user.user_schema import FullUserSchema


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)


    # Relaciones
    subjects: Mapped[Set["Subject"]] = relationship(
        back_populates="created",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    questions: Mapped[Set["Question"]] = relationship(
        back_populates="created",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    answers: Mapped[Set["Answer"]] = relationship(
        back_populates="created",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    nodes: Mapped[Set["Node"]] = relationship(
        back_populates="created",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    question_parameters: Mapped[Set["QuestionParameter"]] = relationship(
        back_populates="created",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    exams: Mapped[Set["Exam"]] = relationship(
        back_populates="created",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    results: Mapped[Set["Result"]] = relationship(
        back_populates="created",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


    def __repr__(self):
     return "<User(id='%s', email='%s')>" % (self.id, self.email)

    @staticmethod
    def insert_user(
            session,
            email: str,
            name: str,
            password: str,
    ) -> FullUserSchema:

        # Password is hashed to increase security
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), PASSWORD_SALT).decode('utf-8')

        # A new user instance is created and added to the database
        new_user = User(email=email, name=name, password=hashed_password)
        session.add(new_user)
        session.commit()
        schema = FullUserSchema().dump(new_user)
        return schema

    @staticmethod
    def get_user(
            session,
            id: int
    ) -> FullUserSchema:

        # The user is obtained by its ID
        query = select(User).where(User.id == id)
        res = session.execute(query).first()
        return res[0]

    @staticmethod
    def get_user_by_email(
            session,
            email: str
    ) -> FullUserSchema:

        # The user is obtained by its email
        query = select(User).where(User.email == email)
        res = session.execute(query).first()
        if res is not None:
            return res[0]
        else:
            return FullUserSchema().dump(User(email=email, password='0'))
