import React, { useState, useEffect } from 'react';
import TodoList from './components/TodoList';
import AddTodo from './components/AddTodo';
import './App.css';

// URL de base de l'API - utilise une variable d'environnement en production
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Charger les todos au démarrage
  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/api/todos`);
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }
      const data = await response.json();
      setTodos(data);
      setError(null);
    } catch (err) {
      setError(`Impossible de charger les todos: ${err.message}`);
      console.error('Erreur:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = async (title, priority = 'medium', deadline = null) => {
    try {
      const response = await fetch(`${API_BASE}/api/todos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, priority, deadline }),
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const newTodo = await response.json();
      setTodos([newTodo, ...todos]);
    } catch (err) {
      setError(`Impossible d'ajouter la todo: ${err.message}`);
      console.error('Erreur:', err);
    }
  };

  const handleToggleTodo = async (id) => {
    try {
      const response = await fetch(`${API_BASE}/api/todos/${id}/toggle`, {
        method: 'PUT',
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const updatedTodo = await response.json();
      setTodos(todos.map(todo =>
        todo.id === id ? updatedTodo : todo
      ));
    } catch (err) {
      setError(`Impossible de mettre à jour la todo: ${err.message}`);
      console.error('Erreur:', err);
    }
  };

  const handleDeleteTodo = async (id) => {
    try {
      const response = await fetch(`${API_BASE}/api/todos/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      setTodos(todos.filter(todo => todo.id !== id));
    } catch (err) {
      setError(`Impossible de supprimer la todo: ${err.message}`);
      console.error('Erreur:', err);
    }
  };

  const handleUpdateTodo = async (id, newTitle) => {
    try {
      const response = await fetch(`${API_BASE}/api/todos/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: newTitle }),
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const updatedTodo = await response.json();
      setTodos(todos.map(todo =>
        todo.id === id ? updatedTodo : todo
      ));
    } catch (err) {
      setError(`Impossible de modifier la todo: ${err.message}`);
      console.error('Erreur:', err);
    }
  };

  // Statistiques supplémentaires
  const overdueCount = todos.filter(t => t.is_overdue && !t.completed).length;
  const highPriorityCount = todos.filter(t => t.priority === 'high' && !t.completed).length;

  return (
    <div className="app">
      <header className="app-header">
        <h1>TodoApp</h1>
        <p className="app-subtitle">Gestionnaire de tâches avec Flask et React</p>
      </header>

      <main className="app-main">
        <AddTodo onAdd={handleAddTodo} />

        {error && (
          <div className="error-message">
            {error}
            <button onClick={() => setError(null)}>×</button>
          </div>
        )}

        {loading ? (
          <div className="loading">Chargement des todos...</div>
        ) : (
          <TodoList
            todos={todos}
            onToggle={handleToggleTodo}
            onDelete={handleDeleteTodo}
            onUpdate={handleUpdateTodo}
          />
        )}

        <div className="app-footer">
          <p>Total: {todos.length} tâche(s) |
            Complétées: {todos.filter(t => t.completed).length} |
            Actives: {todos.filter(t => !t.completed).length} |
            En retard: <span className={overdueCount > 0 ? 'stat-warning' : ''}>{overdueCount}</span> |
            Haute priorité: <span className={highPriorityCount > 0 ? 'stat-highlight' : ''}>{highPriorityCount}</span>
          </p>
          <button onClick={fetchTodos} className="refresh-btn">
            Actualiser
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;