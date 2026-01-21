import os
from supabase import create_client, Client
from dotenv import load_dotenv

class Database:
    """Classe pour gérer la connexion à Supabase"""
    
    def __init__(self):
        # Charger les variables d'environnement depuis .env
        load_dotenv()
        
        # Récupérer l'URL et la clé
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        # Vérifier que les variables existent
        if not url or not key:
            raise ValueError("SUPABASE_URL et SUPABASE_KEY doivent être définis dans .env")
        
        # Créer la connexion
        self.client: Client = create_client(url, key)
    
    def get_client(self):
        """Retourne le client Supabase"""
        return self.client