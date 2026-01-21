#!/usr/bin/env python3
"""
MomentList - CLI pour gérer vos moments
"""

from src.cli import CLI

def main():
    """Point d'entrée principal de l'application"""
    cli = CLI()
    cli.run()

if __name__ == "__main__":
    main()