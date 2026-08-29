from sqlalchemy import Column, Integer, String

from app.database.base import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    repository = Column(String, nullable=False)
    environment = Column(String, nullable=False)
