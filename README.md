# MomentList

Application CLI en Python pour gérer des moments (événements) avec participation automatique ou sur demande.

## Prérequis

- Python 3.8+
- Compte Supabase (gratuit)

## Installation

1. Cloner ou télécharger le projet

2. Créer un environnement virtuel et l'activer:
```bash
python3 -m venv venv
source venv/bin/activate  # Sur Mac/Linux
# OU
venv\Scripts\activate  # Sur Windows
```

3. Installer les dépendances:
```bash
pip install supabase python-dotenv
```

4. Configurer les variables d'environnement:
   - Créer un fichier `.env` à la racine
   - Ajouter vos clés Supabase:
```
SUPABASE_URL=votre_url_supabase
SUPABASE_KEY=votre_clé_publishable
```

5. Créer les tables dans Supabase:
   - Ouvrir le SQL Editor dans Supabase
   - Exécuter le contenu du fichier `schema.sql`

## Utilisation

### Créer un moment
```bash
python main.py create-moment --title "Pizza Party" --description "Soirée pizza!" --mode auto --user "Alice"
```

### Lister tous les moments
```bash
python main.py list-moments
```

### Rejoindre un moment
```bash
python main.py join-moment --moment-id 1 --user "Bob"
```

### Lister les demandes en attente (pour mode "request")
```bash
python main.py list-requests --moment-id 1
```

### Approuver une demande
```bash
python main.py approve-request --participation-id 1
```

### Rejeter une demande
```bash
python main.py reject-request --participation-id 1
```

### Lister les participants d'un moment
```bash
python main.py list-participants --moment-id 1
```

## Structure du projet
```
MomentList/
├── .env                 # Configuration (non versionné)
├── main.py             # Point d'entrée
├── schema.sql          # Schéma de base de données
├── README.md           # Documentation
└── src/
    ├── __init__.py
    ├── database.py     # Connexion Supabase
    ├── models.py       # Classes Moment et Participation
    └── cli.py          # Interface CLI
```

## Technologies utilisées

- **Python 3** - Langage
- **Supabase** - Base de données PostgreSQL
- **argparse** - Parsing des arguments CLI
- **python-dotenv** - Gestion des variables d'environnement