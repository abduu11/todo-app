import os
import resend
from datetime import datetime, timedelta
from models import Todo


def send_deadline_email(todos):
    """Envoyer un email de rappel via Resend"""
    resend.api_key = os.getenv('RESEND_API_KEY')
    recipient = os.getenv('MAIL_RECIPIENT')

    if not resend.api_key or not recipient:
        print("Variables d'environnement Resend manquantes")
        return False

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

    params = {
        "from": "onboarding@resend.dev",
        "to": [recipient],
        "subject": subject,
        "html": body,
    }

    response = resend.Emails.send(params)
    print(f"Email envoyé: {response}")
    return True


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
