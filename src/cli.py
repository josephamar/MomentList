import argparse
from src.database import Database
from src.models import Moment, Participation


class CLI:
    """Interface en ligne de commande pour MomentList"""
    
    def __init__(self):
        self.db = Database()
        self.moment = Moment(self.db)
        self.participation = Participation(self.db)
        self.parser = self.create_parser()
    
    def create_parser(self):
        """Créer le parser de commandes"""
        parser = argparse.ArgumentParser(description="MomentList - Gérer vos moments")
        subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")
        
        # Commande: create-moment
        create_parser = subparsers.add_parser("create-moment", help="Créer un nouveau moment")
        create_parser.add_argument("--title", required=True, help="Titre du moment")
        create_parser.add_argument("--description", required=True, help="Description du moment")
        create_parser.add_argument("--mode", choices=["auto", "request"], default="auto", help="Mode de participation")
        create_parser.add_argument("--user", required=True, help="Nom de l'utilisateur créateur")
        
        # Commande: list-moments
        subparsers.add_parser("list-moments", help="Lister tous les moments")
        
        # Commande: join-moment
        join_parser = subparsers.add_parser("join-moment", help="Rejoindre un moment")
        join_parser.add_argument("--moment-id", type=int, required=True, help="ID du moment")
        join_parser.add_argument("--user", required=True, help="Nom de l'utilisateur")
        
        # Commande: list-requests
        requests_parser = subparsers.add_parser("list-requests", help="Lister les demandes en attente")
        requests_parser.add_argument("--moment-id", type=int, required=True, help="ID du moment")
        
        # Commande: approve-request
        approve_parser = subparsers.add_parser("approve-request", help="Approuver une demande")
        approve_parser.add_argument("--participation-id", type=int, required=True, help="ID de la participation")
        
        # Commande: reject-request
        reject_parser = subparsers.add_parser("reject-request", help="Rejeter une demande")
        reject_parser.add_argument("--participation-id", type=int, required=True, help="ID de la participation")
        
        # Commande: list-participants
        participants_parser = subparsers.add_parser("list-participants", help="Lister les participants")
        participants_parser.add_argument("--moment-id", type=int, required=True, help="ID du moment")
        
        return parser
    
    def run(self):
        """Exécuter la commande CLI"""
        args = self.parser.parse_args()
        
        if args.command == "create-moment":
            self.create_moment(args)
        elif args.command == "list-moments":
            self.list_moments()
        elif args.command == "join-moment":
            self.join_moment(args)
        elif args.command == "list-requests":
            self.list_requests(args)
        elif args.command == "approve-request":
            self.approve_request(args)
        elif args.command == "reject-request":
            self.reject_request(args)
        elif args.command == "list-participants":
            self.list_participants(args)
        else:
            self.parser.print_help()
    
    def create_moment(self, args):
        """Créer un nouveau moment"""
        result = self.moment.create(args.title, args.description, args.mode, args.user)
        print(f"✅ Moment créé avec succès! ID: {result[0]['id']}")
    
    def list_moments(self):
        """Lister tous les moments"""
        moments = self.moment.list_all()
        if not moments:
            print("Aucun moment trouvé.")
            return
        
        print("\n📋 Liste des moments:")
        for m in moments:
            print(f"  ID: {m['id']} | {m['title']} ({m['mode']}) - par {m['created_by']}")

    def join_moment(self, args):
        """Rejoindre un moment"""
        # Récupérer le moment pour vérifier son mode
        moment = self.moment.get_by_id(args.moment_id)
        if not moment:
            print("❌ Moment introuvable.")
            return
        
        # Définir le statut selon le mode
        status = "approved" if moment['mode'] == "auto" else "pending"
        
        try:
            result = self.participation.join(args.moment_id, args.user, status)
            if status == "approved":
                print(f"✅ Vous avez rejoint le moment '{moment['title']}'!")
            else:
                print(f"📨 Demande envoyée pour rejoindre '{moment['title']}'. En attente d'approbation.")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def list_requests(self, args):
        """Lister les demandes en attente"""
        requests = self.participation.list_requests(args.moment_id)
        if not requests:
            print("Aucune demande en attente.")
            return
        
        print("\n📨 Demandes en attente:")
        for req in requests:
            print(f"  ID: {req['id']} | Utilisateur: {req['user_name']}")
    
    def approve_request(self, args):
        """Approuver une demande"""
        result = self.participation.approve(args.participation_id)
        print("✅ Demande approuvée!")
    
    def reject_request(self, args):
        """Rejeter une demande"""
        result = self.participation.reject(args.participation_id)
        print("❌ Demande rejetée.")
    
    def list_participants(self, args):
        """Lister les participants approuvés"""
        participants = self.participation.list_participants(args.moment_id)
        if not participants:
            print("Aucun participant.")
            return
        
        print("\n👥 Participants:")
        for p in participants:
            print(f"  - {p['user_name']}")