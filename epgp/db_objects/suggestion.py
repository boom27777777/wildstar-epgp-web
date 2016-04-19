from epgp.database import Base
from sqlalchemy import Column, Integer, String


class Suggestion(Base):
    __tablename__ = "suggestions"
    _id = Column(Integer, primary_key=True, unique=True)
    body = Column(String(10240))

    def __init__(self, suggestion):
        self.body = suggestion
