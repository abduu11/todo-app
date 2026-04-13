import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from models import Todo


def send_deadline_email(todos):
    """Envoyer un email de rappel pour les todos avec deadline proche"""
    sender = os.getenv('MAIL_SENDER')
    password = os.getenv('MAIL_PASSWORD')
    recipient = os.getenv('MAIL_RECIPIENT')

    if not all([sender, password, recipient]):
        print("Variables d'environnement mail manquantes")
        return False

    # Construire le contenu de l'email
    overdue = [t for t in todos if t.is_overdue()]
    upcoming = [t for t in todos if not t.is_overdue()]

    subject = f"TodoApp - {len(todos)} tâche(s) nécessitent votre attention"

    body = "<h2>Rappel de tâches</h2>"

    if overdue:
        body += "<h3 style='color:red'>⚠️ Tâches en retard</h3><ul>"
        for t in overdue:
            body += f"<li><b>{t.title}</b> - Priorité: {t.priority} - Deadline: {t.deadline.strftime('%d/%m/%Y')}</li>"
        body += "</ul>"

    if upcoming:
        body += "<h3 style='color:orange'>⏰ Deadlines dans moins de 2 jours</h3><ul>"
        for t in upcoming:
            body += f"<li><b>{t.title}</b> - Priorité: {t.priority} - Deadline: {t.deadline.strftime('%d/%m/%Y')}</li>"
        body += "</ul>"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print(f"Email envoyé à {recipient}")
        return True
    except Exception as e:
        print(f"Erreur envoi email: {type(e).__name__}: {e}")
        raise e


def check_and_notify(app):
    """Vérifier les todos et envoyer des notifications si nécessaire"""
    with app.app_context():
        now = datetime.utcnow()
        in_48h = now + timedelta(hours=48)

        todos_to_notify = Todo.query.filter(
            Todo.completed == False,
            Todo.deadline.isnot(None),
            Todo.deadline <= in_48h
        ).all()

        if todos_to_notify:
            send_deadline_email(todos_to_notify)
        else:
            print("Aucune tâche urgente à notifier")
