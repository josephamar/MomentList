import sys
import os

# Ajouter le dossier parent au path pour pouvoir importer flask_app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from flask_app.app import create_app

# Créer l'app pour Vercel
app = create_app()