#!/usr/bin/env python3
"""
Service de notifications email pour TodoApp.
Envoie des rappels pour les tâches avec deadlines proches via Gmail SMTP.
"""

import os
import sys
import smtplib
import logging
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('notifications.log')
    ]
)
logger = logging.getLogger(__name__)

# Variables d'environnement pour SMTP (Gmail)
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
EMAIL_FROM = os.getenv('EMAIL_FROM', SMTP_USER)
EMAIL_TO = os.getenv('EMAIL_TO', SMTP_USER)  # Par défaut, s'envoyer à soi-même
APP_URL = os.getenv('APP_URL', 'http://localhost:5000')
DRY_RUN = os.getenv('DRY_RUN', 'false').lower() == 'true'

def create_email_message(todos_upcoming, todos_overdue, total_count):
    """Crée le contenu de l'email"""
    now = datetime.utcnow().strftime('%d/%m/%Y %H:%M')

    # Construction du message HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #4caf50; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
            .content {{ background: #f9f9f9; padding: 20px; border-radius: 0 0 5px 5px; }}
            .section {{ margin-bottom: 25px; }}
            .section-title {{ color: #4caf50; border-bottom: 2px solid #4caf50; padding-bottom: 5px; }}
            .todo-list {{ list-style: none; padding: 0; }}
            .todo-item {{ background: white; margin: 10px 0; padding: 15px; border-left: 4px solid #4caf50; border-radius: 3px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .todo-title {{ font-weight: bold; font-size: 16px; }}
            .todo-meta {{ color: #666; font-size: 14px; margin-top: 5px; }}
            .priority {{ display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 12px; font-weight: bold; }}
            .priority-high {{ background: #ffebee; color: #c62828; }}
            .priority-medium {{ background: #fff3e0; color: #ef6c00; }}
            .priority-low {{ background: #e8f5e9; color: #2e7d32; }}
            .deadline {{ color: #f44336; font-weight: bold; }}
            .stats {{ background: #e3f2fd; padding: 15px; border-radius: 5px; text-align: center; }}
            .footer {{ text-align: center; margin-top: 20px; color: #888; font-size: 12px; }}
            .app-link {{ color: #4caf50; text-decoration: none; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📋 Rappel TodoApp</h1>
                <p>Vos tâches à ne pas oublier</p>
            </div>

            <div class="content">
                <div class="stats">
                    <p><strong>{total_count}</strong> tâche(s) à surveiller |
                       <strong>{len(todos_upcoming)}</strong> tâche(s) à venir |
                       <strong>{len(todos_overdue)}</strong> tâche(s) en retard</p>
                </div>
    """

    # Section des tâches en retard
    if todos_overdue:
        html_content += """
                <div class="section">
                    <h2 class="section-title">⚠️ Tâches en retard</h2>
                    <ul class="todo-list">
        """
        for todo in todos_overdue:
            priority_class = f"priority-{todo.priority}" if todo.priority else "priority-medium"
            days_overdue = -todo.days_until_deadline if todo.days_until_deadline else 0
            html_content += f"""
                        <li class="todo-item">
                            <div class="todo-title">{todo.title}</div>
                            <div class="todo-meta">
                                <span class="priority {priority_class}">{todo.priority or 'medium'}</span>
                                • En retard depuis {days_overdue} jour(s)
                                • Deadline: {todo.deadline.strftime('%d/%m/%Y')}
                            </div>
                        </li>
            """
        html_content += """
                    </ul>
                </div>
        """

    # Section des tâches à venir (dans les 2 jours)
    if todos_upcoming:
        html_content += """
                <div class="section">
                    <h2 class="section-title">📅 Tâches à venir (dans les 2 jours)</h2>
                    <ul class="todo-list">
        """
        for todo in todos_upcoming:
            priority_class = f"priority-{todo.priority}" if todo.priority else "priority-medium"
            days_left = todo.days_until_deadline if todo.days_until_deadline else 0
            html_content += f"""
                        <li class="todo-item">
                            <div class="todo-title">{todo.title}</div>
                            <div class="todo-meta">
                                <span class="priority {priority_class}">{todo.priority or 'medium'}</span>
                                • Dans {days_left} jour(s)
                                • Deadline: {todo.deadline.strftime('%d/%m/%Y')}
                            </div>
                        </li>
            """
        html_content += """
                    </ul>
                </div>
        """

    # Fin du message
    html_content += f"""
                <div class="footer">
                    <p>Gérez vos tâches sur <a href="{APP_URL}" class="app-link">TodoApp</a></p>
                    <p>Notification générée le {now} (UTC)</p>
                    <p><small>Vous recevez cet email car vous avez activé les notifications dans TodoApp.</small></p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    # Version texte simple (fallback)
    text_content = f"Rappel TodoApp - {now}\n\n"
    if todos_overdue:
        text_content += f"Tâches en retard ({len(todos_overdue)}):\n"
        for todo in todos_overdue:
            days_overdue = -todo.days_until_deadline if todo.days_until_deadline else 0
            text_content += f"- {todo.title} (Priorité: {todo.priority}, En retard depuis {days_overdue} jours)\n"
        text_content += "\n"

    if todos_upcoming:
        text_content += f"Tâches à venir dans les 2 jours ({len(todos_upcoming)}):\n"
        for todo in todos_upcoming:
            days_left = todo.days_until_deadline if todo.days_until_deadline else 0
            text_content += f"- {todo.title} (Priorité: {todo.priority}, Dans {days_left} jours)\n"

    text_content += f"\nTotal: {total_count} tâche(s) à surveiller\n"
    text_content += f"Accédez à l'application: {APP_URL}\n"

    return text_content, html_content

def send_email(subject, text_content, html_content):
    """Envoie un email via SMTP"""
    if DRY_RUN:
        logger.info(f"[DRY RUN] Email non envoyé - Sujet: {subject}")
        logger.info(f"Destinataire: {EMAIL_TO}")
        logger.info(f"Contenu texte:\n{text_content}")
        return True

    if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM, EMAIL_TO]):
        logger.error("Configuration SMTP incomplète. Vérifiez les variables d'environnement.")
        return False

    try:
        # Création du message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO

        # Ajout des versions texte et HTML
        part1 = MIMEText(text_content, 'plain', 'utf-8')
        part2 = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(part1)
        msg.attach(part2)

        # Connexion et envoi
        logger.info(f"Connexion à {SMTP_HOST}:{SMTP_PORT}...")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Email envoyé avec succès à {EMAIL_TO}")
        return True

    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email: {e}")
        return False

def get_todos_for_notification():
    """Récupère les tâches pour notification (à venir et en retard)"""
    try:
        # Importer ici pour éviter les dépendances circulaires
        from app import create_app
        from models import db, Todo

        app = create_app()

        with app.app_context():
            now = datetime.utcnow()
            next_48h = now + timedelta(days=2)

            # Tâches avec deadline dans les 2 jours (non complétées)
            todos_upcoming = Todo.query.filter(
                Todo.deadline.between(now, next_48h),
                Todo.completed == False
            ).all()

            # Tâches en retard (non complétées)
            todos_overdue = Todo.query.filter(
                Todo.deadline < now,
                Todo.completed == False
            ).all()

            total_count = len(todos_upcoming) + len(todos_overdue)

            logger.info(f"Tâches trouvées: {len(todos_upcoming)} à venir, {len(todos_overdue)} en retard")
            return todos_upcoming, todos_overdue, total_count

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des tâches: {e}")
        raise

def main():
    """Point d'entrée principal"""
    logger.info("=" * 60)
    logger.info("Démarrage du service de notifications TodoApp")
    logger.info(f"Mode DRY RUN: {DRY_RUN}")

    try:
        # Récupérer les tâches
        todos_upcoming, todos_overdue, total_count = get_todos_for_notification()

        if total_count == 0:
            logger.info("Aucune tâche nécessitant une notification. Fin du script.")
            return

        # Créer et envoyer l'email
        subject = f"📋 TodoApp - {total_count} tâche(s) à surveiller"
        text_content, html_content = create_email_message(todos_upcoming, todos_overdue, total_count)

        if send_email(subject, text_content, html_content):
            logger.info("Notification envoyée avec succès!")
        else:
            logger.error("Échec de l'envoi de la notification")

    except Exception as e:
        logger.error(f"Erreur critique dans le service de notifications: {e}")
        sys.exit(1)

    logger.info("Service de notifications terminé")
    logger.info("=" * 60)

if __name__ == '__main__':
    main()