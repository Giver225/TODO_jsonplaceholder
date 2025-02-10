from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.adapters.repositories.base import Base


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    completed = Column(Boolean)
    user_id = Column(Integer)

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "user_id": self.user_id
        }