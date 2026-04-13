# TodoApp - Flask + React

Une application Todo complète avec backend Flask et frontend React.

## Structure du projet

```
├── backend/           # Application Flask
│   ├── app.py        # Point d'entrée principal
│   ├── models.py     # Modèles de données
│   ├── routes.py     # Routes API
│   ├── requirements.txt # Dépendances Python
│   └── .env          # Variables d'environnement
├── frontend/         # Application React
│   ├── package.json  # Dépendances Node.js
│   ├── public/       # Fichiers statiques
│   └── src/          # Code source React
└── README.md         # Ce fichier
```

## Installation et exécution

### Prérequis

- Python 3.8+ avec pip
- Node.js 16+ avec npm
- Git (optionnel)

### Méthode 1: Script de démarrage (recommandé)

Utilisez le script Python pour démarrer les deux serveurs automatiquement:

```bash
# Installer les dépendances Python d'abord
cd backend
pip install -r requirements.txt

# Revenir au dossier racine et exécuter le script
cd ..
python start_servers.py
```

Le script démarrera automatiquement:
- Backend Flask sur `http://localhost:5000`
- Frontend React sur `http://localhost:3000`

### Méthode 2: Manuellement

#### Backend (Flask)

1. Naviguer dans le dossier backend:
   ```bash
   cd backend
   ```

2. Installer les dépendances Python:
   ```bash
   pip install -r requirements.txt
   ```

3. Configurer l'environnement (optionnel):
   ```bash
   cp .env.example .env  # Linux/Mac
   copy .env.example .env  # Windows
   ```

4. Lancer le serveur Flask:
   ```bash
   python app.py
   ```
   Le serveur démarrera sur `http://localhost:5000`

#### Frontend (React)

1. Naviguer dans le dossier frontend:
   ```bash
   cd frontend
   ```

2. Installer les dépendances Node.js:
   ```bash
   npm install
   ```

3. Lancer l'application React:
   ```bash
   npm start
   ```
   L'application démarrera sur `http://localhost:3000`

## API Endpoints

- `GET /api/todos` - Récupérer toutes les todos
- `POST /api/todos` - Créer une nouvelle todo
- `GET /api/todos/:id` - Récupérer une todo spécifique
- `PUT /api/todos/:id` - Mettre à jour une todo
- `DELETE /api/todos/:id` - Supprimer une todo
- `PUT /api/todos/:id/toggle` - Basculer l'état complété

## Fonctionnalités

- ✅ Ajouter de nouvelles todos
- ✅ Marquer les todos comme complétées
- ✅ Modifier les todos existantes
- ✅ Supprimer les todos
- ✅ Persistance des données (SQLite)
- ✅ Interface React moderne

## Technologies utilisées

- **Backend**: Flask, Flask-CORS, Flask-SQLAlchemy, SQLite
- **Frontend**: React, JavaScript moderne
- **Communication**: API REST, CORS