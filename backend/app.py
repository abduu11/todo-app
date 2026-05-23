from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import threading
import time

# Charger les variables d'environnement
load_dotenv()

def create_app():
    """Factory pour créer l'application Flask"""
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///todos.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialiser les extensions
    from models import db
    db.init_app(app)

    # Configurer CORS pour permettre les requêtes depuis le frontend React
    if os.getenv('FLASK_ENV') == 'production':
        CORS(app, resources={r"/api/*": {"origins": "*"}})
    else:
        CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    # Initialiser les routes
    from routes import init_routes
    init_routes(app)

    # Créer les tables de la base de données au démarrage
    with app.app_context():
        db.create_all()

    # Route pour servir les fichiers statiques React en production
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend/build')
        if path and os.path.exists(os.path.join(frontend_dir, path)):
            return send_from_directory(frontend_dir, path)
        return send_from_directory(frontend_dir, 'index.html')

    # Lancer le scheduler de notifications de manière sécurisée pour la production
    from mail_service import check_and_notify

    def notification_loop():
        time.sleep(30)  # Donne 30 secondes à Render pour valider le statut 'LIVE' de l'application
        while True:
            try:
                check_and_notify(app)
            except Exception as e:
                print(f"Erreur lors de l'exécution du service de notification: {e}")
            time.sleep(3600)  # Vérifier toutes les heures

    thread = threading.Thread(target=notification_loop, daemon=True)
    thread.start()

    return app

if __name__ == '__main__':
    # Ce bloc est utilisé uniquement pour le développement local (python app.py)
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    debug = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)
