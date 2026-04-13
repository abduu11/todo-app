from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

db = SQLAlchemy()

class Todo(db.Model):
    """Modèle pour les todos"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Nouveaux champs pour les fonctionnalités avancées
    priority = db.Column(db.String(10), default='medium', nullable=True)  # 'low', 'medium', 'high'
    deadline = db.Column(db.DateTime, nullable=True)  # Date limite en UTC

    def to_dict(self):
        """Convertir l'objet en dictionnaire pour JSON"""
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'priority': self.priority,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'is_overdue': self.is_overdue() if self.deadline else False,
            'days_until_deadline': self.days_until_deadline() if self.deadline else None
        }

    def is_overdue(self):
        """Vérifier si la deadline est dépassée (comparaison en UTC)"""
        if not self.deadline:
            return False
        return self.deadline < datetime.utcnow()

    def days_until_deadline(self):
        """Nombre de jours jusqu'à la deadline (négatif si dépassée)"""
        if not self.deadline:
            return None
        delta = self.deadline - datetime.utcnow()
        return delta.days

    def __repr__(self):
        return f'<Todo {self.id}: {self.title}>'