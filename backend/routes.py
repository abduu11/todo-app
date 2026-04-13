from flask import request, jsonify
from models import db, Todo

def init_routes(app):
    """Initialiser les routes de l'API"""

    @app.route('/api/todos', methods=['GET'])
    def get_todos():
        """Récupérer toutes les todos"""
        todos = Todo.query.order_by(Todo.created_at.desc()).all()
        return jsonify([todo.to_dict() for todo in todos])

    @app.route('/api/todos', methods=['POST'])
    def create_todo():
        """Créer une nouvelle todo"""
        data = request.get_json()

        if not data or not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400

        todo = Todo(title=data['title'])
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
        """Mettre à jour une todo"""
        todo = Todo.query.get_or_404(todo_id)
        data = request.get_json()

        if 'title' in data:
            todo.title = data['title']
        if 'completed' in data:
            todo.completed = data['completed']

        db.session.commit()
        return jsonify(todo.to_dict())

    @app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
    def delete_todo(todo_id):
        """Supprimer une todo"""
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return '', 204

    @app.route('/api/todos/<int:todo_id>/toggle', methods=['PUT'])
    def toggle_todo(todo_id):
        """Basculer l'état complété d'une todo"""
        todo = Todo.query.get_or_404(todo_id)
        todo.completed = not todo.completed
        db.session.commit()
        return jsonify(todo.to_dict())