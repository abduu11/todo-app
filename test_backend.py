#!/usr/bin/env python
"""Script pour tester le backend Flask"""

import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

def test_backend():
    """Tester les endpoints de l'API"""
    print("Test du backend TodoApp...")

    # Attendre que le serveur démarre
    time.sleep(2)

    try:
        # 1. Créer une todo
        print("1. Création d'une todo...")
        todo_data = {"title": "Première tâche de test"}
        response = requests.post(f"{BASE_URL}/todos", json=todo_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            todo1 = response.json()
            print(f"   Todo créée: {todo1['title']} (ID: {todo1['id']})")
        else:
            print(f"   Erreur: {response.text}")
            return

        # 2. Récupérer toutes les todos
        print("\n2. Récupération de toutes les todos...")
        response = requests.get(f"{BASE_URL}/todos")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            todos = response.json()
            print(f"   {len(todos)} todo(s) trouvée(s)")

        # 3. Basculer l'état complété
        print("\n3. Basculer l'état complété...")
        response = requests.put(f"{BASE_URL}/todos/{todo1['id']}/toggle")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            updated = response.json()
            print(f"   Todo mise à jour: completed={updated['completed']}")

        # 4. Modifier le titre
        print("\n4. Modification du titre...")
        update_data = {"title": "Tâche modifiée"}
        response = requests.put(f"{BASE_URL}/todos/{todo1['id']}", json=update_data)
        print(f"   Status: {response.status_code}")

        # 5. Supprimer la todo
        print("\n5. Suppression de la todo...")
        response = requests.delete(f"{BASE_URL}/todos/{todo1['id']}")
        print(f"   Status: {response.status_code}")

        print("\n✅ Tous les tests ont réussi !")

    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur. Assurez-vous que le serveur Flask est en cours d'exécution.")
        print("   Exécutez: python backend/app.py")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_backend()