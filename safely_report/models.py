from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()


class SurveyResponse(db.Model):  # type: ignore
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True)
    response = Column(String, nullable=False)  # Stringified JSON

    def __init__(self, response):
        self.response = response

    def __repr__(self):
        return f"<SurveyResponse ID: {self.id}>"


class GarblingBlock(db.Model):  # type: ignore
    __tablename__ = "garbling_blocks"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    shocks = Column(String, nullable=False)  # Stringified array
    version = Column(Integer, nullable=False)

    def __init__(self, name, shocks):
        self.name = name
        self.shocks = shocks

    def __repr__(self):
        return f"<GarblingBlock Name: {self.name}>"

    # For optimistic locking
    __mapper_args__ = {"version_id_col": version}
