#!/usr/bin/env python3
"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

init_db.py - Initialisation de la base de données
Ce fichier crée les tables de la base de données et initialise le compte
administrateur à partir des variables d'environnement.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

env_file = Path('.env')
if env_file.exists():
    load_dotenv(env_file)

from app import app
from extensions import db


def init_database():
    with app.app_context():
        from models.pharmacy import Pharmacy
        from models.admin import Admin
        from models.submission import LocationSubmission, InfoSubmission, PharmacyView, Suggestion, PharmacyProposal
        from models.emergency_contact import EmergencyContact
        from models.site_settings import SiteSettings, PopupMessage
        from models.advertisement import Advertisement, AdSettings
        from models.activity_log import ActivityLog
        
        db.create_all()
        print("Database tables created successfully!")
        print("Tables created:")
        print("  - pharmacy")
        print("  - admin")
        print("  - location_submission")
        print("  - info_submission")
        print("  - pharmacy_view")
        print("  - suggestion")
        print("  - pharmacy_proposal")
        print("  - emergency_contact")
        print("  - site_settings")
        print("  - popup_message")
        print("  - advertisement")
        print("  - ad_settings")
        print("  - activity_log")


def init_admin_from_env():
    with app.app_context():
        from models.admin import Admin
        
        username = os.environ.get('ADMIN_USERNAME')
        password = os.environ.get('ADMIN_PASSWORD')
        
        if not username or not password:
            print("ADMIN_USERNAME and ADMIN_PASSWORD environment variables are required.")
            print("Add them to your .env file or export them.")
            return False
        
        existing_admin = Admin.query.filter_by(username=username).first()
        if existing_admin:
            existing_admin.set_password(password)
            db.session.commit()
            print(f"Admin '{username}' password updated successfully!")
        else:
            admin = Admin(username=username)
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            print(f"Admin '{username}' created successfully!")
        
        return True


def init_default_seo_settings():
    """Initialize default SEO settings if not present."""
    with app.app_context():
        from models.site_settings import SiteSettings
        
        defaults = {
            'site_name': 'UrgenceMaroc.com',
            'og_title': 'UrgenceMaroc.com - Trouvez votre pharmacie au Maroc',
            'og_description': 'Annuaire complet des pharmacies au Maroc. Trouvez les pharmacies de garde, numéros d\'urgence et informations de contact.',
            'meta_description': 'Annuaire des pharmacies au Maroc. Pharmacies de garde 24h/24, numéros d\'urgence, carte interactive. Trouvez la pharmacie la plus proche.',
            'meta_keywords': 'pharmacie maroc, pharmacie garde casablanca, urgence maroc, pharmacie 24h, samu maroc, pompiers maroc',
            'twitter_handle': '',
            'canonical_url': '',
            'google_site_verification': '',
            'robots_txt': 'User-agent: *\nAllow: /',
        }
        
        for key, value in defaults.items():
            existing = SiteSettings.query.filter_by(key=key).first()
            if not existing:
                SiteSettings.set(key, value)
                print(f"SEO setting '{key}' initialized.")
        
        print("Default SEO settings initialized!")


if __name__ == '__main__':
    init_database()
    init_admin_from_env()
    init_default_seo_settings()
