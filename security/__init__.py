"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

security/__init__.py - Module de sécurité
Ce fichier exporte les fonctions de sécurité et d'authentification.
"""

from security.auth import init_login_manager, create_default_admin

__all__ = ['init_login_manager', 'create_default_admin']
