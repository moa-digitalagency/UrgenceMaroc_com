"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

security/auth.py - Authentification et gestion utilisateurs
Ce fichier initialise le gestionnaire de connexion Flask-Login
et crée le compte administrateur par défaut.
"""

import os
import logging
from extensions import login_manager, db
from models.admin import Admin

logger = logging.getLogger(__name__)


def init_login_manager(app):
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


def create_default_admin():
    admin_username = os.environ.get('ADMIN_USERNAME')
    admin_password = os.environ.get('ADMIN_PASSWORD')
    
    if not admin_username or not admin_password:
        logger.warning("ADMIN_USERNAME or ADMIN_PASSWORD not set, skipping admin creation")
        return
    
    try:
        existing_admin = Admin.query.filter_by(username=admin_username).first()
        if existing_admin:
            existing_admin.set_password(admin_password)
            db.session.commit()
            logger.info(f"Admin password updated for user: {admin_username}")
            return
        
        admin_count = Admin.query.count()
        if admin_count == 0:
            admin = Admin()
            admin.username = admin_username
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            logger.info(f"Admin user created: {admin_username}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating/updating admin: {e}")
