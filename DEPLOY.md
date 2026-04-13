# Déploiement sur Render.com

Votre application TodoApp (Flask + React) est prête à être déployée sur Render.com gratuitement.

## 📦 Fichiers préparés

- `render.yaml` - Configuration Render (service web + base de données PostgreSQL)
- `backend/requirements.txt` - Ajout de `gunicorn` et `psycopg2-binary`
- `backend/app.py` - Configuration production (CORS, static files, port dynamique)
- `frontend/src/App.js` - URLs API dynamiques avec variable d'environnement
- `frontend/.env.example` - Exemple de configuration React
- `frontend/.env` - Configuration développement local (ignoré par git)

## 🚀 Étapes de déploiement

### 1. Créer un dépôt GitHub
```bash
git init
git add .
git commit -m "Ready for Render deployment"
# Créez un dépôt sur GitHub et poussez
git remote add origin https://github.com/votre-username/todoapp.git
git push -u origin main
```

### 2. Créer un compte Render
1. Allez sur [render.com](https://render.com)
2. Créez un compte (connexion avec GitHub recommandée)
3. Cliquez sur "New +" → "Blueprint"
4. Sélectionnez votre dépôt GitHub

### 3. Configuration automatique
Render détectera automatiquement `render.yaml` et configurera :
- ✅ Service web Python avec gunicorn
- ✅ Base de données PostgreSQL gratuite
- ✅ Variables d'environnement automatiques
- ✅ HTTPS avec certificat SSL
- ✅ Déploiement continu

### 4. Attendre le déploiement
- Premier déploiement : 5-10 minutes
- Build inclut : installation Python, installation Node.js, build React
- Base de données PostgreSQL créée automatiquement

## 🔧 Configuration technique

### Backend (Flask)
- Port : 10000 (géré par Render)
- Base de données : PostgreSQL (URL injectée via `DATABASE_URL`)
- Secret : généré automatiquement
- Environnement : `production`

### Frontend (React)
- Build produit dans `frontend/build/`
- Servi statiquement par Flask
- URLs API : relatives (`/api/todos`) en production
- Variables d'environnement : `REACT_APP_API_URL` (vide en production)

## 📊 Plan gratuit Render

- **750 heures/mois** (≈ 31 jours continus)
- **Base de données PostgreSQL** incluse
- **HTTPS automatique**
- **Limite** : service s'arrête après 15 minutes d'inactivité (redémarre à la requête suivante)

## 🔍 Test local (optionnel)

```bash
# Backend avec PostgreSQL simulé
cd backend
pip install -r requirements.txt
python app.py  # Utilise SQLite localement

# Frontend
cd frontend
npm install
npm start  # http://localhost:3000
```

## ⚠️ Notes importantes

1. **Données SQLite locales** ne seront pas migrées automatiquement
2. **Premier démarrage** peut prendre 30 secondes (base de données PostgreSQL)
3. **URLs API** : en production, utilisez des chemins relatifs (`/api/todos`)
4. **CORS** : configuré pour accepter toutes les origines en production

## 🆘 Support

- Documentation Render : https://render.com/docs
- Problèmes de build : vérifiez les logs dans le dashboard Render
- Base de données : accès via psql ou interface Render

Votre application sera disponible sur `https://todoapp.onrender.com` (ou nom similaire).