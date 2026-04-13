#!/usr/bin/env python3
"""
Script de migration pour ajouter les colonnes 'priority' et 'deadline' à la table Todo.
Compatible avec SQLite (développement) et PostgreSQL (production).
"""

import sys
import os
from sqlalchemy import inspect, text

# Ajouter le répertoire parent au chemin pour importer l'application
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db

def check_column_exists(table_name, column_name, connection):
    """Vérifie si une colonne existe déjà dans une table"""
    inspector = inspect(connection)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def migrate_sqlite(connection):
    """Migration pour SQLite (ALTER TABLE ADD COLUMN)"""
    # SQLite ne supporte pas la vérification de colonnes existantes via INFORMATION_SCHEMA
    # On utilise une approche try-except
    try:
        # Vérifier si la colonne 'priority' existe déjà
        connection.execute(text("SELECT priority FROM todo LIMIT 1"))
        print("  → Colonne 'priority' existe déjà")
    except Exception:
        # Ajouter la colonne 'priority'
        connection.execute(text("ALTER TABLE todo ADD COLUMN priority VARCHAR(10) DEFAULT 'medium'"))
        print("  + Colonne 'priority' ajoutée (VARCHAR(10), default='medium')")

    try:
        # Vérifier si la colonne 'deadline' existe déjà
        connection.execute(text("SELECT deadline FROM todo LIMIT 1"))
        print("  → Colonne 'deadline' existe déjà")
    except Exception:
        # Ajouter la colonne 'deadline'
        connection.execute(text("ALTER TABLE todo ADD COLUMN deadline TIMESTAMP"))
        print("  + Colonne 'deadline' ajoutée (TIMESTAMP, nullable)")

def migrate_postgresql(connection):
    """Migration pour PostgreSQL"""
    # Vérifier et ajouter 'priority'
    if not check_column_exists('todo', 'priority', connection):
        connection.execute(text("""
            ALTER TABLE todo
            ADD COLUMN priority VARCHAR(10) DEFAULT 'medium'
        """))
        print("  + Colonne 'priority' ajoutée (VARCHAR(10), default='medium')")
    else:
        print("  → Colonne 'priority' existe déjà")

    # Vérifier et ajouter 'deadline'
    if not check_column_exists('todo', 'deadline', connection):
        connection.execute(text("""
            ALTER TABLE todo
            ADD COLUMN deadline TIMESTAMP
        """))
        print("  + Colonne 'deadline' ajoutée (TIMESTAMP, nullable)")
    else:
        print("  → Colonne 'deadline' existe déjà")

def main():
    """Exécute la migration"""
    print("🚀 Démarrage de la migration: ajout des colonnes priority et deadline")

    # Créer l'application Flask
    app = create_app()

    with app.app_context():
        # Obtenir la connexion à la base de données
        connection = db.engine.connect()

        # Détecter le type de base de données
        dialect = db.engine.dialect.name
        print(f"  Base de données détectée: {dialect}")

        # Exécuter la migration appropriée
        if dialect == 'sqlite':
            migrate_sqlite(connection)
        elif dialect == 'postgresql':
            migrate_postgresql(connection)
        else:
            print(f"  ⚠️  Dialecte non supporté: {dialect}")
            print("  Tentative d'utilisation de la syntaxe SQL standard...")
            # Essayer la syntaxe PostgreSQL (la plus commune)
            migrate_postgresql(connection)

        # Valider les changements
        print("\n  ✅ Migration terminée!")
        print("  Vérification des colonnes dans la table 'todo':")

        inspector = inspect(connection)
        columns = inspector.get_columns('todo')
        for col in columns:
            print(f"    - {col['name']}: {col['type']}")

        connection.close()

    print("\n🎉 Migration réussie! Les nouvelles fonctionnalités sont prêtes.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        sys.exit(1)