"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

routes/__init__.py - Module des routes
Ce fichier exporte les blueprints Flask pour les routes publiques et admin.
"""

from routes.public import public_bp
from routes.admin import admin_bp

__all__ = ['public_bp', 'admin_bp']
