# Démarrage Rapide - TodoApp Flask + React

## Méthode la plus simple

### 1. Démarrer le backend Flask
```bash
cd backend
pip install -r requirements.txt
python app.py
```
**Serveur Flask:** http://localhost:5000

### 2. Démarrer le frontend React (dans un autre terminal)
```bash
cd frontend

# Option A: Utiliser npx (recommandé)
npx react-scripts start

# Option B: Si npx ne fonctionne pas, essayer:
npm install
npm start

# Option C: Utiliser yarn
yarn install
yarn start
```
**Application React:** http://localhost:3000

## Vérification

### Tester l'API Flask
```bash
curl http://localhost:5000/api/todos
```

### Tester l'application React
Ouvrez http://localhost:3000 dans votre navigateur.

## Dépannage rapide

### Problème: "react-scripts n'est pas reconnu"
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Problème: Erreur CORS
Assurez-vous que:
- Flask tourne sur le port 5000
- React tourne sur le port 3000
- Les deux serveurs sont en cours d'exécution

### Problème: Base de données SQLite
```bash
cd backend
# Supprimer et recréer la base de données
rm -f todos.db
python app.py
```

## Fonctionnalités disponibles

1. **Ajouter une todo**: Tapez dans la zone de texte et appuyez sur Entrée
2. **Marquer comme complété**: Cochez la case
3. **Modifier une todo**: Cliquez sur le texte (seulement pour les tâches actives)
4. **Supprimer une todo**: Cliquez sur l'icône poubelle
5. **Filtrer**: Les tâches sont séparées en "Actives" et "Complétées"
6. **Compteur**: Nombre total, complétées et actives en bas de page

## Structure du projet
- `backend/` - API Flask avec SQLite
- `frontend/` - Application React
- `test_backend.py` - Tests API
- `start_servers.py` - Script pour démarrer les deux serveurs