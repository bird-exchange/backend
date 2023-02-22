from sqlalchemy import Column, Integer, String

from backend.db import Base


class Bird(Base):
    __tablename__ = 'birds'

    uid = Column(Integer, primary_key=True)
    name = Column(String(), unique=True, nullable=False)
    type = Column(Integer)
    was_fitted = Column(Integer, default=0)

    def __str__(self) -> str:
        return 'Bird {uid}, {name}'.format(
            uid=self.uid,
            name=self.name,
        )
