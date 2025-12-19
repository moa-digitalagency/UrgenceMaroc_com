"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

models/pharmacy.py - Modèle Pharmacie
Ce fichier définit le modèle Pharmacy avec les types d'établissement,
catégories d'emplacement, statut de garde et coordonnées GPS.
"""

from extensions import db
from datetime import datetime, timedelta


ETABLISSEMENT_TYPES = [
    ('pharmacie_generale', 'Pharmacie générale'),
    ('depot_pharmaceutique', 'Dépôt pharmaceutique'),
    ('pharmacie_hospitaliere', 'Pharmacie hospitalière'),
]

LOCATION_CATEGORIES = [
    ('standard', 'Emplacement standard'),
    ('gare', 'Proche de la gare'),
    ('hopital', 'Proche de l\'hôpital'),
    ('aeroport', 'Proche de l\'aéroport'),
    ('centre_commercial', 'Centre commercial'),
    ('marche', 'Proche du marché'),
    ('centre_ville', 'Centre-ville'),
    ('zone_residentielle', 'Zone résidentielle'),
]

class Pharmacy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    nom = db.Column(db.String(200), nullable=False)
    ville = db.Column(db.String(100), nullable=False)
    quartier = db.Column(db.String(200))
    telephone = db.Column(db.String(100))
    bp = db.Column(db.String(50))
    horaires = db.Column(db.String(200))
    services = db.Column(db.Text)
    proprietaire = db.Column(db.String(200))
    type_etablissement = db.Column(db.String(100), default='pharmacie_generale')
    categorie_emplacement = db.Column(db.String(50), default='standard')
    is_garde = db.Column(db.Boolean, default=False)
    garde_start_date = db.Column(db.DateTime)
    garde_end_date = db.Column(db.DateTime)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    location_validated = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    validated_at = db.Column(db.DateTime)
    validated_by_admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def is_currently_garde(self):
        if not self.is_garde:
            return False
        if self.garde_end_date is None:
            return True
        return datetime.utcnow() <= self.garde_end_date
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'nom': self.nom,
            'ville': self.ville,
            'quartier': self.quartier or '',
            'telephone': self.telephone or '',
            'bp': self.bp or '',
            'horaires': self.horaires or '',
            'services': self.services or '',
            'proprietaire': self.proprietaire or '',
            'type_etablissement': self.type_etablissement or 'pharmacie_generale',
            'categorie_emplacement': self.categorie_emplacement or 'standard',
            'is_garde': self.is_currently_garde,
            'lat': self.latitude,
            'lng': self.longitude,
            'location_validated': self.location_validated,
            'is_verified': self.is_verified,
            'garde_end_date': self.garde_end_date.isoformat() if self.garde_end_date else None
        }
