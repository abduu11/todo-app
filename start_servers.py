#!/usr/bin/env python
"""Script pour démarrer les serveurs Flask et React"""

import subprocess
import sys
import time
import os
import signal

def start_flask():
    """Démarrer le serveur Flask"""
    print("Démarrage du serveur Flask...")
    flask_proc = subprocess.Popen(
        [sys.executable, "backend/app.py"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    # Attendre que Flask démarre
    time.sleep(3)

    # Vérifier si Flask est en cours d'exécution
    if flask_proc.poll() is not None:
        print("❌ Le serveur Flask a échoué à démarrer")
        for line in flask_proc.stdout:
            print(line, end='')
        return None

    print("✅ Serveur Flask démarré sur http://localhost:5000")
    return flask_proc

def start_react():
    """Démarrer le serveur React"""
    print("Démarrage du serveur React...")

    # Vérifier si les dépendances sont installées
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
    node_modules = os.path.join(frontend_dir, "node_modules")

    if not os.path.exists(node_modules):
        print("Installation des dépendances React...")
        install_proc = subprocess.run(
            ["npm", "install"],
            cwd=frontend_dir,
            capture_output=True,
            text=True
        )
        if install_proc.returncode != 0:
            print("❌ Échec de l'installation des dépendances React")
            print(install_proc.stderr)
            return None

    # Démarrer React
    react_proc = subprocess.Popen(
        ["npm", "start"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    # Attendre que React démarre
    time.sleep(5)

    # Vérifier si React est en cours d'exécution
    if react_proc.poll() is not None:
        print("❌ Le serveur React a échoué à démarrer")
        for line in react_proc.stdout:
            print(line, end='')
        return None

    print("✅ Serveur React démarré sur http://localhost:3000")
    return react_proc

def main():
    """Fonction principale"""
    print("=" * 50)
    print("Démarrage de TodoApp - Flask + React")
    print("=" * 50)

    flask_proc = None
    react_proc = None

    try:
        flask_proc = start_flask()
        if not flask_proc:
            return 1

        react_proc = start_react()
        if not react_proc:
            return 1

        print("\n" + "=" * 50)
        print("Les deux serveurs sont en cours d'exécution:")
        print("- Backend Flask:  http://localhost:5000")
        print("- Frontend React: http://localhost:3000")
        print("\nAppuyez sur Ctrl+C pour arrêter les serveurs")
        print("=" * 50)

        # Attendre l'interruption
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nArrêt des serveurs...")

    finally:
        # Arrêter les processus
        if flask_proc:
            flask_proc.terminate()
            flask_proc.wait()
            print("✅ Serveur Flask arrêté")

        if react_proc:
            react_proc.terminate()
            react_proc.wait()
            print("✅ Serveur React arrêté")

    return 0

if __name__ == "__main__":
    sys.exit(main())