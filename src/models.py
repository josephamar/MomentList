class Moment:
    """Classe pour gérer les moments (événements)"""
    
    def __init__(self, db):
        self.db = db
        self.client = db.get_client()
    
    def create(self, title, description, mode, created_by):
        """Créer un nouveau moment"""
        data = {
            "title": title,
            "description": description,
            "mode": mode,
            "created_by": created_by
        }
        response = self.client.table("moments").insert(data).execute()
        return response.data
    
    def list_all(self):
        """Lister tous les moments"""
        response = self.client.table("moments").select("*").execute()
        return response.data
    
    def get_by_id(self, moment_id):
        """Récupérer un moment par son ID"""
        response = self.client.table("moments").select("*").eq("id", moment_id).execute()
        return response.data[0] if response.data else None


class Participation:
    """Classe pour gérer les participations aux moments"""
    
    def __init__(self, db):
        self.db = db
        self.client = db.get_client()
    
    def join(self, moment_id, user_name, status="approved"):
        """Rejoindre un moment (auto ou request)"""
        data = {
            "moment_id": moment_id,
            "user_name": user_name,
            "status": status
        }
        response = self.client.table("participations").insert(data).execute()
        return response.data
    
    def list_requests(self, moment_id):
        """Lister les demandes en attente pour un moment"""
        response = self.client.table("participations").select("*").eq("moment_id", moment_id).eq("status", "pending").execute()
        return response.data
    
    def approve(self, participation_id):
        """Approuver une demande de participation"""
        response = self.client.table("participations").update({"status": "approved"}).eq("id", participation_id).execute()
        return response.data
    
    def reject(self, participation_id):
        """Rejeter une demande de participation"""
        response = self.client.table("participations").delete().eq("id", participation_id).execute()
        return response.data
    
    def list_participants(self, moment_id):
        """Lister tous les participants approuvés d'un moment"""
        response = self.client.table("participations").select("*").eq("moment_id", moment_id).eq("status", "approved").execute()
        return response.data