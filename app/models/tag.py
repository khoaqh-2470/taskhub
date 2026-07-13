from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.task import task_tags


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), unique=True, index=True, nullable=False)

    tasks = relationship("Task", secondary=task_tags, back_populates="tags")
