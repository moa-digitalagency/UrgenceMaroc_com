"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

main.py - Point d'entrée de l'application
Ce fichier charge les variables d'environnement et importe l'application Flask
pour le démarrage du serveur.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

env_file = Path('.env')
if env_file.exists():
    load_dotenv(env_file)

from app import app  # noqa: F401
