"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

models/submission.py - Modèles de soumissions utilisateurs
Ce fichier définit les modèles pour les soumissions de localisation GPS,
corrections d'informations, suggestions et propositions de nouvelles pharmacies.
"""

from extensions import db
from datetime import datetime


class LocationSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pharmacy_id = db.Column(db.Integer, db.ForeignKey('pharmacy.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    submitted_by_name = db.Column(db.String(100))
    submitted_by_phone = db.Column(db.String(50))
    comment = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    reviewed_by_admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    
    pharmacy = db.relationship('Pharmacy', backref='location_submissions')
    reviewed_by = db.relationship('Admin', foreign_keys=[reviewed_by_admin_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'pharmacy_id': self.pharmacy_id,
            'pharmacy_name': self.pharmacy.nom if self.pharmacy else '',
            'latitude': self.latitude,
            'longitude': self.longitude,
            'submitted_by_name': self.submitted_by_name or 'Anonyme',
            'submitted_by_phone': self.submitted_by_phone or '',
            'comment': self.comment or '',
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class InfoSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pharmacy_id = db.Column(db.Integer, db.ForeignKey('pharmacy.id'), nullable=False)
    field_name = db.Column(db.String(50), nullable=False)
    current_value = db.Column(db.Text)
    proposed_value = db.Column(db.Text, nullable=False)
    submitted_by_name = db.Column(db.String(100))
    submitted_by_phone = db.Column(db.String(50))
    comment = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    reviewed_by_admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    
    pharmacy = db.relationship('Pharmacy', backref='info_submissions')
    reviewed_by = db.relationship('Admin', foreign_keys=[reviewed_by_admin_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'pharmacy_id': self.pharmacy_id,
            'pharmacy_name': self.pharmacy.nom if self.pharmacy else '',
            'field_name': self.field_name,
            'current_value': self.current_value or '',
            'proposed_value': self.proposed_value,
            'submitted_by_name': self.submitted_by_name or 'Anonyme',
            'submitted_by_phone': self.submitted_by_phone or '',
            'comment': self.comment or '',
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class PharmacyView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pharmacy_id = db.Column(db.Integer, db.ForeignKey('pharmacy.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    pharmacy = db.relationship('Pharmacy', backref='views')


class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    submitted_by_name = db.Column(db.String(100))
    submitted_by_email = db.Column(db.String(120))
    submitted_by_phone = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending')
    admin_response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    reviewed_by_admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    
    reviewed_by = db.relationship('Admin', foreign_keys=[reviewed_by_admin_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'subject': self.subject,
            'message': self.message,
            'submitted_by_name': self.submitted_by_name or 'Anonyme',
            'submitted_by_email': self.submitted_by_email or '',
            'submitted_by_phone': self.submitted_by_phone or '',
            'status': self.status,
            'admin_response': self.admin_response or '',
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class PharmacyProposal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    submitted_by_name = db.Column(db.String(100))
    submitted_by_email = db.Column(db.String(120))
    submitted_by_phone = db.Column(db.String(50))
    comment = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    reviewed_by_admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    
    reviewed_by = db.relationship('Admin', foreign_keys=[reviewed_by_admin_id])
    
    def to_dict(self):
        return {
            'id': self.id,
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
            'is_garde': self.is_garde,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'submitted_by_name': self.submitted_by_name or 'Anonyme',
            'submitted_by_email': self.submitted_by_email or '',
            'submitted_by_phone': self.submitted_by_phone or '',
            'comment': self.comment or '',
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
