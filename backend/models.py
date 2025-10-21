from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Task(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # Using string for UUID
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.TODO)
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
