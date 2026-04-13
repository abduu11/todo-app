import React, { useState } from 'react';
import './AddTodo.css';

const PRIORITY_OPTIONS = [
  { value: 'high',   label: '🔴 Haute',   desc: 'Urgent, à faire maintenant' },
  { value: 'medium', label: '🟠 Moyenne', desc: 'Important, à faire bientôt' },
  { value: 'low',    label: '🟢 Faible',  desc: 'Peut attendre' },
];

function AddTodo({ onAdd }) {
  const [title, setTitle] = useState('');
  const [priority, setPriority] = useState('medium');
  const [deadline, setDeadline] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || isSubmitting) return;

    setIsSubmitting(true);
    try {
      let deadlineISO = null;
      if (deadline) {
        const date = new Date(deadline);
        date.setHours(23, 59, 59, 999);
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

  const selectedPriority = PRIORITY_OPTIONS.find(p => p.value === priority);

  return (
    <form className="add-todo-form" onSubmit={handleSubmit}>
      <div className="form-title-row">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Quelle est votre prochaine tâche ?"
          className="todo-input"
          disabled={isSubmitting}
          autoFocus
          maxLength={200}
        />
      </div>

      <div className="form-options-row">
        <div className="field-group">
          <label className="field-label">⚡ Priorité</label>
          <select
            className={`priority-select priority-select--${priority}`}
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            disabled={isSubmitting}
          >
            {PRIORITY_OPTIONS.map(opt => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
          <span className="field-hint">{selectedPriority.desc}</span>
        </div>

        <div className="field-group">
          <label className="field-label" htmlFor="deadline-input">📅 Date limite</label>
          <input
            id="deadline-input"
            type="date"
            className="deadline-input"
            value={deadline}
            onChange={(e) => setDeadline(e.target.value)}
            disabled={isSubmitting}
            min={new Date().toISOString().split('T')[0]}
          />
          <span className="field-hint">
            {deadline
              ? `Deadline : ${new Date(deadline).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long' })}`
              : 'Optionnel'}
          </span>
        </div>

        <button
          type="submit"
          className="add-btn"
          disabled={!title.trim() || isSubmitting}
        >
          {isSubmitting ? '...' : '+ Ajouter'}
        </button>
      </div>
    </form>
  );
}

export default AddTodo;
