import React, { useState } from 'react';
import './AddTodo.css';

function AddTodo({ onAdd }) {
  const [title, setTitle] = useState('');
  const [priority, setPriority] = useState('medium');
  const [deadline, setDeadline] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!title.trim() || isSubmitting) {
      return;
    }

    setIsSubmitting(true);
    try {
      // Convertir la deadline en format ISO si fournie
      let deadlineISO = null;
      if (deadline) {
        const date = new Date(deadline);
        date.setHours(23, 59, 59, 999); // Fin de journée
        deadlineISO = date.toISOString();
      }

      await onAdd(title.trim(), priority, deadlineISO);
      setTitle('');
      setPriority('medium');
      setDeadline('');
    } catch (err) {
      console.error('Erreur lors de l\'ajout:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form className="add-todo-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Quelle est votre prochaine tâche ?"
          className="todo-input"
          disabled={isSubmitting}
          autoFocus
        />
        <select
          className="priority-select"
          value={priority}
          onChange={(e) => setPriority(e.target.value)}
          disabled={isSubmitting}
        >
          <option value="low">Faible</option>
          <option value="medium">Moyenne</option>
          <option value="high">Haute</option>
        </select>
        <input
          type="date"
          className="deadline-input"
          value={deadline}
          onChange={(e) => setDeadline(e.target.value)}
          disabled={isSubmitting}
          min={new Date().toISOString().split('T')[0]}
        />
        <button
          type="submit"
          className="add-btn"
          disabled={!title.trim() || isSubmitting}
        >
          {isSubmitting ? 'Ajout...' : 'Ajouter'}
        </button>
      </div>

      {title.trim() && (
        <div className="input-hint">
          Appuyez sur Entrée pour ajouter • {title.trim().length}/200 caractères
          {deadline && ` • Deadline: ${new Date(deadline).toLocaleDateString('fr-FR')}`}
        </div>
      )}
    </form>
  );
}

export default AddTodo;