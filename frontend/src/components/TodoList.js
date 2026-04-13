import React from 'react';
import TodoItem from './TodoItem';
import './TodoList.css';

function TodoList({ todos, onToggle, onDelete, onUpdate }) {
  if (todos.length === 0) {
    return (
      <div className="todo-list empty">
        <p>Aucune tâche pour le moment. Ajoutez votre première todo !</p>
      </div>
    );
  }

  // Séparer les todos complétées et actives
  const completedTodos = todos.filter(todo => todo.completed);
  const activeTodos = todos.filter(todo => !todo.completed);

  return (
    <div className="todo-list">
      {activeTodos.length > 0 && (
        <div className="todo-section">
          <h3>Tâches actives ({activeTodos.length})</h3>
          <ul className="todo-items">
            {activeTodos.map(todo => (
              <TodoItem
                key={todo.id}
                todo={todo}
                onToggle={onToggle}
                onDelete={onDelete}
                onUpdate={onUpdate}
              />
            ))}
          </ul>
        </div>
      )}

      {completedTodos.length > 0 && (
        <div className="todo-section">
          <h3>Tâches complétées ({completedTodos.length})</h3>
          <ul className="todo-items completed">
            {completedTodos.map(todo => (
              <TodoItem
                key={todo.id}
                todo={todo}
                onToggle={onToggle}
                onDelete={onDelete}
                onUpdate={onUpdate}
              />
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default TodoList;