from sqlalchemy import Column, Integer, String, ForeignKey

from app.database.base import Base


class Deployment(Base):
    __tablename__ = "deployments"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    version = Column(String, nullable=False)
    commit_sha = Column(String, nullable=False)
    image = Column(String, nullable=False)
    environment = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
