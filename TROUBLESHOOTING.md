# Dépannage - TodoApp Flask + React

## Problème: "react-scripts n'est pas reconnu"

### Solution 1: Installation complète des dépendances
```bash
cd frontend
# Supprimer node_modules s'il existe
rm -rf node_modules package-lock.json

# Réinstaller toutes les dépendances
npm install
```

### Solution 2: Utiliser Yarn (alternative à npm)
```bash
cd frontend
# Installer Yarn si ce n'est pas déjà fait
npm install -g yarn

# Installer les dépendances avec Yarn
yarn install
```

### Solution 3: Installer react-scripts globalement
```bash
# Installer react-scripts globalement
npm install -g react-scripts

cd frontend
npm start
```

### Solution 4: Vérifier les versions de Node.js/npm
```bash
# Vérifier les versions
node --version  # Doit être >= 16
npm --version   # Doit être >= 8

# Mettre à jour npm si nécessaire
npm install -g npm@latest
```

## Problème: Erreurs de connexion CORS

### Solution: Vérifier les ports
- Backend Flask: http://localhost:5000
- Frontend React: http://localhost:3000

Vérifier que les deux serveurs sont en cours d'exécution:
```bash
# Terminal 1: Backend
cd backend
python app.py

# Terminal 2: Frontend  
cd frontend
npm start
```

## Problème: Base de données SQLite ne persiste pas

### Solution: Vérifier les permissions d'écriture
```bash
cd backend
ls -la *.db  # Vérifier si todos.db existe
```

Si la base de données ne se crée pas:
```bash
cd backend
python -c "
from app import create_app
app = create_app()
with app.app_context():
    from models import db
    db.create_all()
    print('Base de données créée')
"
```

## Problème: Erreurs d'importation Python

### Solution: Vérifier l'environnement Python
```bash
cd backend
# Vérifier que les dépendances sont installées
pip install -r requirements.txt

# Tester l'application
python app.py
```

## Démarrage rapide
```bash
# 1. Backend
cd backend
pip install -r requirements.txt
python app.py

# 2. Frontend (dans un autre terminal)
cd frontend
npm install  # ou yarn install
npm start    # ou yarn start
```

## Tests
```bash
# Tester l'API Flask
python test_backend.py

# Tester manuellement avec curl
curl http://localhost:5000/api/todos
curl -X POST http://localhost:5000/api/todos -H "Content-Type: application/json" -d '{"title":"Test"}'
```