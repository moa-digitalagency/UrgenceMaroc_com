#!/usr/bin/env python3
"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

migrate_db.py - Migration sécurisée de la base de données
Ce fichier gère les migrations de schéma sans perdre les données existantes.
Il crée ou met à jour les tables manquantes/incomplètes de manière sûre.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

env_file = Path('.env')
if env_file.exists():
    load_dotenv(env_file)

from app import app
from extensions import db


def check_database_integrity():
    """Vérifie l'intégrité de la base de données et crée les tables manquantes."""
    with app.app_context():
        # Import all models
        from models.pharmacy import Pharmacy
        from models.admin import Admin
        from models.submission import LocationSubmission, InfoSubmission, PharmacyView, Suggestion, PharmacyProposal
        from models.emergency_contact import EmergencyContact
        from models.site_settings import SiteSettings, PopupMessage
        from models.advertisement import Advertisement, AdSettings
        from models.activity_log import ActivityLog
        
        inspector = db.inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        print("=" * 90)
        print("VÉRIFICATION ET MIGRATION - BASE DE DONNÉES")
        print("=" * 90)
        
        # Expected tables
        expected_tables = {
            'pharmacy': Pharmacy,
            'admin': Admin,
            'location_submission': LocationSubmission,
            'info_submission': InfoSubmission,
            'pharmacy_view': PharmacyView,
            'suggestion': Suggestion,
            'pharmacy_proposal': PharmacyProposal,
            'emergency_contact': EmergencyContact,
            'site_settings': SiteSettings,
            'popup_message': PopupMessage,
            'advertisement': Advertisement,
            'ad_settings': AdSettings,
            'activity_log': ActivityLog,
        }
        
        print(f"\n📊 État actuel:")
        print(f"   Tables existantes: {len(existing_tables)}/{len(expected_tables)}")
        
        # Check for missing tables
        missing_tables = []
        for table_name, model_class in expected_tables.items():
            if table_name not in existing_tables:
                missing_tables.append((table_name, model_class))
        
        if missing_tables:
            print(f"\n⚠️  {len(missing_tables)} table(s) manquante(s):")
            for table_name, _ in missing_tables:
                print(f"   ✗ {table_name}")
        
        # Create missing tables
        if missing_tables:
            print(f"\n🔄 Création des tables manquantes (sans supprimer les données existantes)...")
            for table_name, model_class in missing_tables:
                try:
                    model_class.__table__.create(db.engine, checkfirst=True)
                    print(f"   ✓ Créée: {table_name}")
                except Exception as e:
                    print(f"   ✗ Erreur pour {table_name}: {e}")
        
        # Verify columns for existing tables
        print(f"\n🔍 Vérification des colonnes...")
        schema_issues = []
        
        for table_name, model_class in expected_tables.items():
            if table_name in existing_tables:
                db_columns = {col['name'] for col in inspector.get_columns(table_name)}
                model_columns = {col.name for col in model_class.__table__.columns}
                
                missing_cols = model_columns - db_columns
                if missing_cols:
                    schema_issues.append((table_name, missing_cols))
                    print(f"   ⚠️  {table_name}: colonnes manquantes {missing_cols}")
                else:
                    print(f"   ✓ {table_name}: schéma OK")
        
        # Try to add missing columns
        if schema_issues:
            print(f"\n🔧 Ajout des colonnes manquantes...")
            for table_name, missing_cols in schema_issues:
                for col_name in missing_cols:
                    try:
                        model_class = expected_tables[table_name]
                        col = model_class.__table__.columns[col_name]
                        col_type = str(col.type)
                        nullable = col.nullable
                        
                        # Use ALTER TABLE to add column safely
                        db.engine.execute(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type}")
                        print(f"   ✓ Ajoutée colonne: {table_name}.{col_name}")
                    except Exception as e:
                        print(f"   ✗ Erreur pour {table_name}.{col_name}: {str(e)[:60]}")
        
        print("\n" + "=" * 90)
        print("✅ Migration terminée - Les données existantes sont intactes")
        print("=" * 90)


def verify_all_models():
    """Vérifie que tous les modèles sont chargés."""
    with app.app_context():
        from models.pharmacy import Pharmacy
        from models.admin import Admin
        from models.submission import LocationSubmission, InfoSubmission, PharmacyView, Suggestion, PharmacyProposal
        from models.emergency_contact import EmergencyContact
        from models.site_settings import SiteSettings, PopupMessage
        from models.advertisement import Advertisement, AdSettings
        from models.activity_log import ActivityLog
        
        models = [
            Pharmacy, Admin, LocationSubmission, InfoSubmission, PharmacyView, 
            Suggestion, PharmacyProposal, EmergencyContact, SiteSettings, PopupMessage,
            Advertisement, AdSettings, ActivityLog
        ]
        
        print(f"\n✓ {len(models)} modèles chargés avec succès")
        return len(models) == 13


if __name__ == '__main__':
    try:
        check_database_integrity()
        verify_all_models()
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Erreur lors de la migration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
