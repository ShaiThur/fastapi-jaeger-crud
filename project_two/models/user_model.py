from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped

from models.base_db_model import BaseDbModel


class UserModel(BaseDbModel):
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String)
    age: Mapped[int] = Column(Integer)

    def __repr__(self):
        return f"<UserModel(id={self.id}, name={self.name}, age={self.age})>"
