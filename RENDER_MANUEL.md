# Déploiement manuel sur Render (sans Blueprint)

Guide étape par étape pour déployer votre TodoApp sur Render sans utiliser Blueprint.

## 📋 Prérequis

1. **Compte GitHub** avec votre code poussé
2. **Compte Render** (peut demander une carte pour vérification, mais utilisera le plan gratuit)

## 🚀 Étapes de déploiement

### Étape 1 : Préparer le code sur GitHub

```bash
# 1. Initialiser git (si pas déjà fait)
git init

# 2. Ajouter tous les fichiers
git add .

# 3. Commiter
git commit -m "Ready for Render deployment"

# 4. Créer un dépôt sur GitHub (github.com → New repository)
# 5. Ajouter le remote et pousser
git remote add origin https://github.com/VOTRE-USERNAME/todoapp.git
git branch -M main
git push -u origin main
```

### Étape 2 : Créer la base de données PostgreSQL sur Render

1. **Connectez-vous** à [dashboard.render.com](https://dashboard.render.com)
2. Cliquez sur **"New +"** en haut à droite
3. Sélectionnez **"PostgreSQL"**
4. Configurez :
   - **Name** : `todoapp-db` (ou autre nom)
   - **Database** : `todoapp` (optionnel)
   - **User** : Laisser par défaut
   - **Region** : Choix le plus proche (ex: Frankfurt)
   - **PostgreSQL Version** : Laisser par défaut (15)
   - **Plan** : **Free** (vérifiez bien!)
5. Cliquez **"Create Database"**
6. **ATTENDEZ** 2-3 minutes que la base de données soit créée
7. **Notez** l'**Internal Database URL** (ex: `postgresql://user:password@host:port/dbname`)

### Étape 3 : Créer le service Web sur Render

1. Retournez au dashboard Render
2. Cliquez sur **"New +"** → **"Web Service"**
3. **Connectez votre compte GitHub** si ce n'est pas déjà fait
4. Sélectionnez votre dépôt `todoapp`
5. Configurez le service :

#### Section "Basics"
- **Name** : `todoapp` (ou autre)
- **Environment** : **Python 3**
- **Region** : Même que la base de données
- **Branch** : `main`
- **Root Directory** : Laisser vide (racine du dépôt)
- **Plan** : **Free**

#### Section "Build & Deploy"
- **Build Command** : Copiez-collez exactement :
  ```bash
  pip install -r backend/requirements.txt && cd frontend && npm install && npm run build
  ```
- **Start Command** : Copiez-collez exactement :
  ```bash
  gunicorn backend.app:create_app
  ```

#### Section "Environment"
Cliquez sur **"Add Environment Variable"** et ajoutez :

1. **DATABASE_URL**
   - Key : `DATABASE_URL`
   - Value : **Copiez l'Internal Database URL** de l'étape 2
   - Important : Ne modifiez pas cette URL!

2. **SECRET_KEY**
   - Key : `SECRET_KEY`
   - Value : `render-secret-key-$(date +%s)` (ou une chaîne aléatoire)
   - Exemple : `render-secret-key-1744579200`

3. **FLASK_ENV**
   - Key : `FLASK_ENV`
   - Value : `production`

4. **PORT**
   - Key : `PORT`
   - Value : `10000`

### Étape 4 : Déployer

1. **Vérifiez** toutes les configurations
2. Cliquez **"Create Web Service"**
3. **ATTENDEZ** 5-10 minutes pour le premier déploiement

## 🔍 Vérification du déploiement

### Pendant le déploiement :
1. **Logs** : Cliquez sur "Logs" dans le dashboard
2. **Étapes attendues** :
   - ✅ Clonage du dépôt
   - ✅ Installation Python (`pip install`)
   - ✅ Installation Node.js (`npm install`)
   - ✅ Build React (`npm run build`)
   - ✅ Démarrage gunicorn
   - ✅ Connexion à PostgreSQL

### Après déploiement :
1. **URL** : Votre app est sur `https://todoapp.onrender.com` (ou nom similaire)
2. **Test API** : `https://todoapp.onrender.com/api/todos`
3. **Test frontend** : `https://todoapp.onrender.com/`

## ⚠️ Problèmes courants

### "Build failed"
1. **Logs** : Vérifiez les erreurs dans les logs
2. **Python** : `backend/requirements.txt` doit exister
3. **Node.js** : `frontend/package.json` doit exister
4. **Dépendances** : Assurez-vous que `gunicorn` et `psycopg2-binary` sont dans requirements.txt

### "Database connection failed"
1. **URL** : Vérifiez que `DATABASE_URL` est correcte
2. **Wait** : La base de données peut mettre 2-3 minutes à être prête
3. **Plan free** : La base free a des limites de connexion

### "Application error"
1. **Logs** : Regardez les logs d'exécution (pas build)
2. **Port** : Vérifiez que `PORT=10000` est défini
3. **Import** : Vérifiez que `backend/app.py` s'importe correctement

## 🔄 Mises à jour futures

Pour mettre à jour votre application :
1. Poussez vos changements sur GitHub
2. Render détectera automatiquement et redéploiera
3. Suivez les logs dans le dashboard

## 📊 Plan gratuit Render

- **750 heures/mois** (≈ 31 jours continus)
- **Base de données PostgreSQL** incluse (limité)
- **HTTPS automatique**
- **Limite** : Service s'arrête après 15 min d'inactivité
- **Redémarrage** : Automatique à la prochaine requête

## 🗄️ Migration de base de données

Après avoir déployé les nouvelles fonctionnalités (priorités et deadlines), vous devez exécuter une migration pour ajouter les colonnes à la table existante.

### Migration en développement (local)

1. **Activer l'environnement virtuel** :
   ```bash
   cd backend
   source venv/bin/activate  # Linux/Mac
   # ou venv\Scripts\activate  # Windows
   ```

2. **Exécuter le script de migration** :
   ```bash
   python migrations/add_priority_deadline.py
   ```

3. **Vérifier le résultat** :
   - Le script affiche les colonnes ajoutées
   - Vérifiez avec un outil SQL que les colonnes `priority` et `deadline` existent

### Migration en production (Render)

Sur Render, la migration s'exécute automatiquement car le modèle SQLAlchemy crée les colonnes manquantes au démarrage (si `db.create_all()` est utilisé). Cependant, pour une migration explicite :

1. **Exécuter le script via le shell Render** :
   - Allez dans le dashboard Render → votre service web
   - Cliquez sur "Shell" dans le menu de gauche
   - Exécutez :
     ```bash
     cd backend && python migrations/add_priority_deadline.py
     ```

2. **Vérification** :
   - Les logs du shell affichent le résultat
   - L'application fonctionnera avec les nouvelles colonnes

### Notes importantes

- **Compatibilité ascendante** : Les anciennes tâches auront `priority=NULL` (affiché "Moyenne") et `deadline=NULL`
- **Sauvegarde** : Avant toute migration en production, faites une sauvegarde de la base de données
- **Test** : Testez toujours la migration en environnement de développement d'abord

## 📧 Notifications Email (Gmail)

Pour activer les notifications email (rappels 2 jours avant les deadlines) :

### Configuration Gmail SMTP

1. **Créer un mot de passe d'application Gmail** :
   - Allez sur [g.co/apppasswords](https://g.co/apppasswords)
   - Connectez-vous avec votre compte Gmail
   - Sélectionnez "Mail" et "Autre (Nom personnalisé)" → entrez "TodoApp"
   - Copiez le mot de passe généré (16 caractères)

2. **Configurer les variables d'environnement sur Render** :
   - Allez dans le dashboard Render → votre service **todoapp-notifications** (cron)
   - Cliquez sur "Environment" dans le menu de gauche
   - Ajoutez les variables suivantes :

| Variable | Valeur | Description |
|----------|--------|-------------|
| `SMTP_USER` | votre@gmail.com | Votre adresse Gmail |
| `SMTP_PASSWORD` | mot-de-passe-app | Mot de passe d'application généré |
| `EMAIL_FROM` | votre@gmail.com | Expéditeur (optionnel, défaut: SMTP_USER) |
| `EMAIL_TO` | destinataire@email.com | Destinataire (optionnel, défaut: SMTP_USER) |

3. **Activer les notifications** :
   - Assurez-vous que `DRY_RUN` est défini à `false` (défaut)
   - Le cron s'exécute toutes les 6 heures (configurable dans `render.yaml`)

### Test des notifications

1. **Mode test (DRY_RUN)** :
   - Définissez `DRY_RUN=true` pour voir les logs sans envoyer d'email
   - Les logs apparaissent dans le dashboard Render (service cron)

2. **Créer une tâche de test** :
   - Ajoutez une tâche avec une deadline dans 2 jours
   - Attendez l'exécution du cron (ou déclenchez-le manuellement)

### Dépannage

- **Erreurs SMTP** : Vérifiez le mot de passe d'application et que "Accès moins sécurisé" est activé (optionnel)
- **Logs** : Consultez les logs du service cron dans Render
- **Base de données** : Assurez-vous que le service cron a accès à la même base de données

## 🆘 Support

- **Logs Render** : Dashboard → votre service → "Logs"
- **Statut base de données** : Dashboard → votre base → "Status"
- **Variables d'environnement** : Dashboard → votre service → "Environment"

Votre application est maintenant en production avec une base de données PostgreSQL persistante et des notifications email automatiques !