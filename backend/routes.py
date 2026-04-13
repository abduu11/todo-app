from flask import request, jsonify
from datetime import datetime, timedelta
from models import db, Todo

def init_routes(app):
    """Initialiser les routes de l'API"""

    @app.route('/api/todos', methods=['GET'])
    def get_todos():
        """Récupérer toutes les todos triées par priorité et deadline"""
        # Tri personnalisé: priorité (high > medium > low), puis deadline proche, puis date création
        from sqlalchemy import case
        todos = Todo.query.order_by(
            case(
                (Todo.priority == 'high', 1),
                (Todo.priority == 'medium', 2),
                (Todo.priority == 'low', 3),
                else_=4
            ),
            case(
                (Todo.deadline.is_(None), 1),
                else_=0
            ),
            Todo.deadline.asc(),
            Todo.created_at.desc()
        ).all()
        return jsonify([todo.to_dict() for todo in todos])

    @app.route('/api/todos', methods=['POST'])
    def create_todo():
        """Créer une nouvelle todo avec priorité et deadline optionnelles"""
        data = request.get_json()

        if not data or not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400

        # Validation et parsing de la priorité
        valid_priorities = ['low', 'medium', 'high', None]
        priority = data.get('priority', 'medium')
        if priority not in valid_priorities:
            priority = 'medium'  # Valeur par défaut si invalide

        # Conversion de la deadline (format ISO 8601 attendu)
        deadline = None
        if data.get('deadline'):
            try:
                # Supprimer le 'Z' final si présent et convertir en UTC
                deadline_str = data['deadline'].replace('Z', '+00:00')
                deadline = datetime.fromisoformat(deadline_str)
            except ValueError:
                return jsonify({'error': 'Invalid deadline format. Use ISO 8601 (e.g., 2024-12-31T23:59:59)'}), 400

        todo = Todo(
            title=data['title'],
            priority=priority,
            deadline=deadline
        )

        if 'completed' in data:
            todo.completed = data['completed']

        db.session.add(todo)
        db.session.commit()

        return jsonify(todo.to_dict()), 201

    @app.route('/api/todos/<int:todo_id>', methods=['GET'])
    def get_todo(todo_id):
        """Récupérer une todo spécifique"""
        todo = Todo.query.get_or_404(todo_id)
        return jsonify(todo.to_dict())

    @app.route('/api/todos/<int:todo_id>', methods=['PUT'])
    def update_todo(todo_id):
        """Mettre à jour une todo (incluant priorité et deadline)"""
        todo = Todo.query.get_or_404(todo_id)
        data = request.get_json()

        if 'title' in data:
            todo.title = data['title']
        if 'completed' in data:
            todo.completed = data['completed']
        if 'priority' in data:
            # Validation de la priorité
            if data['priority'] in ['low', 'medium', 'high', None]:
                todo.priority = data['priority']
            # Si valeur invalide, on ignore (ne pas changer)
        if 'deadline' in data:
            if data['deadline'] is None:
                todo.deadline = None
            else:
                try:
                    deadline_str = data['deadline'].replace('Z', '+00:00')
                    todo.deadline = datetime.fromisoformat(deadline_str)
                except ValueError:
                    return jsonify({'error': 'Invalid deadline format. Use ISO 8601 (e.g., 2024-12-31T23:59:59)'}), 400

        db.session.commit()
        return jsonify(todo.to_dict())

    @app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
    def delete_todo(todo_id):
        """Supprimer une todo"""
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return '', 204

    @app.route('/api/test-mail', methods=['GET'])
    def test_mail():
        """Route de test pour vérifier l'envoi d'email"""
        from mail_service import send_deadline_email
        from datetime import datetime, timedelta

        # Créer une todo fictive pour le test
        class FakeTodo:
            title = "Tâche de test"
            priority = "high"
            deadline = datetime.utcnow() + timedelta(hours=12)
            def is_overdue(self): return False

        success = send_deadline_email([FakeTodo()])
        if success:
            return jsonify({'status': 'Email envoyé avec succès'})
        return jsonify({'status': 'Échec envoi email'}), 500

    @app.route('/api/todos/upcoming', methods=['GET'])
    def get_upcoming_todos():
        """
        Récupérer les todos avec deadlines proches pour les notifications.
        Retourne les tâches non complétées dont la deadline est dans les 2 jours
        et les tâches en retard.
        """
        now = datetime.utcnow()
        next_48h = now + timedelta(days=2)

        # Tâches avec deadline dans les 2 jours (non complétées)
        upcoming = Todo.query.filter(
            Todo.deadline.between(now, next_48h),
            Todo.completed == False
        ).all()

        # Tâches en retard (non complétées)
        overdue = Todo.query.filter(
            Todo.deadline < now,
            Todo.completed == False
        ).all()

        return jsonify({
            'upcoming': [todo.to_dict() for todo in upcoming],
            'overdue': [todo.to_dict() for todo in overdue],
            'timestamp': now.isoformat()
        })

    @app.route('/api/todos/<int:todo_id>/toggle', methods=['PUT'])
    def toggle_todo(todo_id):
        """Basculer l'état complété d'une todo"""
        todo = Todo.query.get_or_404(todo_id)
        todo.completed = not todo.completed
        db.session.commit()
        return jsonify(todo.to_dict())