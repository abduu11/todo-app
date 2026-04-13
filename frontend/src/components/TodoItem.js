import React, { useState } from 'react';
import './TodoItem.css';

function TodoItem({ todo, onToggle, onDelete, onUpdate }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [isDeleting, setIsDeleting] = useState(false);

  // Fonctions utilitaires pour formater les données
  const getPriorityLabel = (priority) => {
    switch (priority) {
      case 'high': return 'Haute';
      case 'medium': return 'Moyenne';
      case 'low': return 'Faible';
      default: return 'Moyenne';
    }
  };

  const getPriorityClass = (priority) => {
    switch (priority) {
      case 'high': return 'priority-high';
      case 'medium': return 'priority-medium';
      case 'low': return 'priority-low';
      default: return 'priority-medium';
    }
  };

  const formatDeadline = (deadlineISO) => {
    if (!deadlineISO) return null;

    const deadline = new Date(deadlineISO);
    const now = new Date();
    const diffTime = deadline - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays < 0) {
      return { text: `En retard (${Math.abs(diffDays)}j)`, class: 'deadline-overdue' };
    } else if (diffDays === 0) {
      return { text: "Aujourd'hui", class: 'deadline-today' };
    } else if (diffDays === 1) {
      return { text: 'Demain', class: 'deadline-tomorrow' };
    } else if (diffDays <= 7) {
      return { text: `Dans ${diffDays} jours`, class: 'deadline-upcoming' };
    } else {
      return { text: deadline.toLocaleDateString('fr-FR'), class: 'deadline-future' };
    }
  };

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

  // Données formatées pour l'affichage
  const priorityLabel = getPriorityLabel(todo.priority);
  const priorityClass = getPriorityClass(todo.priority);
  const deadlineInfo = formatDeadline(todo.deadline);
  const isOverdue = deadlineInfo && deadlineInfo.class === 'deadline-overdue';

  return (
    <li className={`todo-item ${todo.completed ? 'completed' : ''} ${isDeleting ? 'deleting' : ''} ${isOverdue ? 'overdue' : ''}`}>
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
          {/* Badge de priorité */}
          {todo.priority && (
            <span className={`priority-badge ${priorityClass}`}>
              {priorityLabel}
            </span>
          )}

          {/* Badge de deadline */}
          {deadlineInfo && (
            <span className={`deadline-badge ${deadlineInfo.class}`}>
              📅 {deadlineInfo.text}
            </span>
          )}

          {/* Date de création */}
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