import React, { useState } from 'react';
import './TodoItem.css';

function TodoItem({ todo, onToggle, onDelete, onUpdate }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [isDeleting, setIsDeleting] = useState(false);

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = () => {
    if (editTitle.trim() && editTitle !== todo.title) {
      onUpdate(todo.id, editTitle.trim());
    }
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditTitle(todo.title);
    setIsEditing(false);
  };

  const handleDelete = () => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette tâche ?')) {
      setIsDeleting(true);
      onDelete(todo.id);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSave();
    } else if (e.key === 'Escape') {
      handleCancel();
    }
  };

  return (
    <li className={`todo-item ${todo.completed ? 'completed' : ''} ${isDeleting ? 'deleting' : ''}`}>
      <div className="todo-checkbox">
        <input
          type="checkbox"
          checked={todo.completed}
          onChange={() => onToggle(todo.id)}
          id={`todo-${todo.id}`}
        />
        <label htmlFor={`todo-${todo.id}`}></label>
      </div>

      <div className="todo-content">
        {isEditing ? (
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            onKeyDown={handleKeyDown}
            onBlur={handleSave}
            autoFocus
            className="todo-edit-input"
          />
        ) : (
          <span
            className={`todo-title ${todo.completed ? 'completed' : ''}`}
            onClick={() => !todo.completed && handleEdit()}
            title={todo.completed ? '' : 'Cliquer pour modifier'}
          >
            {todo.title}
          </span>
        )}

        <div className="todo-meta">
          <span className="todo-date">
            {new Date(todo.created_at).toLocaleDateString('fr-FR', {
              day: 'numeric',
              month: 'short',
              year: 'numeric'
            })}
          </span>
        </div>
      </div>

      <div className="todo-actions">
        {!isEditing && !todo.completed && (
          <button
            onClick={handleEdit}
            className="todo-action-btn edit-btn"
            title="Modifier"
          >
            ✏️
          </button>
        )}
        <button
          onClick={handleDelete}
          className="todo-action-btn delete-btn"
          title="Supprimer"
          disabled={isDeleting}
        >
          {isDeleting ? '...' : '🗑️'}
        </button>
      </div>
    </li>
  );
}

export default TodoItem;