"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

models/emergency_contact.py - Modèle Contacts d'urgence
Ce fichier définit le modèle EmergencyContact pour les numéros d'urgence
(police, pompiers, hôpitaux, etc.) nationaux et par ville.
"""

from extensions import db
from datetime import datetime


EMERGENCY_SERVICE_TYPES = [
    ('police', 'Police'),
    ('pompiers', 'Pompiers'),
    ('ambulance', 'Ambulance / SAMU'),
    ('hopital', 'Hôpital'),
    ('clinique', 'Clinique'),
    ('sos_medecins', 'SOS Médecins'),
    ('protection_civile', 'Protection Civile'),
    ('autre', 'Autre'),
]


class EmergencyContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ville = db.Column(db.String(100), nullable=True)
    service_type = db.Column(db.String(50), nullable=False)
    label = db.Column(db.String(200), nullable=False)
    phone_numbers = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300))
    notes = db.Column(db.Text)
    is_national = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    ordering = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ville': self.ville or 'National',
            'service_type': self.service_type,
            'label': self.label,
            'phone_numbers': self.phone_numbers,
            'address': self.address or '',
            'notes': self.notes or '',
            'is_national': self.is_national,
            'is_active': self.is_active,
            'ordering': self.ordering
        }
