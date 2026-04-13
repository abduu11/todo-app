import React, { useState } from 'react';
import './AddTodo.css';

function AddTodo({ onAdd }) {
  const [title, setTitle] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!title.trim() || isSubmitting) {
      return;
    }

    setIsSubmitting(true);
    try {
      await onAdd(title.trim());
      setTitle('');
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
        </div>
      )}
    </form>
  );
}

export default AddTodo;