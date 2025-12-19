"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

services/pharmacy_service.py - Service Pharmacie
Ce fichier contient la logique métier pour la gestion des pharmacies:
recherche, filtrage, CRUD et statistiques.
"""

from datetime import datetime
from extensions import db
from models.pharmacy import Pharmacy


class PharmacyService:
    @staticmethod
    def get_all_pharmacies(search=None, ville=None, garde_only=False, gare_only=False, categorie=None):
        query = Pharmacy.query
        
        if search:
            search_lower = f'%{search.lower()}%'
            query = query.filter(
                db.or_(
                    Pharmacy.nom.ilike(search_lower),
                    Pharmacy.quartier.ilike(search_lower),
                    Pharmacy.services.ilike(search_lower)
                )
            )
        
        if ville:
            query = query.filter(Pharmacy.ville == ville)
        
        if garde_only:
            query = query.filter(Pharmacy.is_garde == True)
        
        if gare_only:
            query = query.filter(Pharmacy.categorie_emplacement == 'gare')
        
        if categorie:
            query = query.filter(Pharmacy.categorie_emplacement == categorie)
        
        return query.order_by(Pharmacy.nom).all()
    
    @staticmethod
    def get_pharmacy_by_id(pharmacy_id):
        return Pharmacy.query.get_or_404(pharmacy_id)
    
    @staticmethod
    def get_stats():
        total = Pharmacy.query.count()
        garde = Pharmacy.query.filter(Pharmacy.is_garde == True).count()
        gare = Pharmacy.query.filter(Pharmacy.categorie_emplacement == 'gare').count()
        validated = Pharmacy.query.filter(Pharmacy.location_validated == True).count()
        
        villes = db.session.query(
            Pharmacy.ville, 
            db.func.count(Pharmacy.id)
        ).group_by(Pharmacy.ville).all()
        
        return {
            'total': total,
            'pharmacies_garde': garde,
            'pharmacies_gare': gare,
            'locations_validated': validated,
            'par_ville': {v: c for v, c in villes}
        }
    
    @staticmethod
    def get_distinct_cities():
        villes = db.session.query(Pharmacy.ville).distinct().order_by(Pharmacy.ville).all()
        return [v[0] for v in villes]
    
    @staticmethod
    def create_pharmacy(data):
        pharmacy = Pharmacy(
            code=data.get('code'),
            nom=data.get('nom'),
            ville=data.get('ville'),
            quartier=data.get('quartier'),
            telephone=data.get('telephone'),
            bp=data.get('bp'),
            horaires=data.get('horaires'),
            services=data.get('services'),
            proprietaire=data.get('proprietaire'),
            type_etablissement=data.get('type_etablissement', 'pharmacie_generale'),
            categorie_emplacement=data.get('categorie_emplacement', 'standard'),
            is_garde=data.get('is_garde', False),
            is_verified=data.get('is_verified', False),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            location_validated=data.get('location_validated', False)
        )
        db.session.add(pharmacy)
        db.session.commit()
        return pharmacy
    
    @staticmethod
    def update_pharmacy(pharmacy, data):
        pharmacy.code = data.get('code', pharmacy.code)
        pharmacy.nom = data.get('nom', pharmacy.nom)
        pharmacy.ville = data.get('ville', pharmacy.ville)
        pharmacy.quartier = data.get('quartier', pharmacy.quartier)
        pharmacy.telephone = data.get('telephone', pharmacy.telephone)
        pharmacy.bp = data.get('bp', pharmacy.bp)
        pharmacy.horaires = data.get('horaires', pharmacy.horaires)
        pharmacy.services = data.get('services', pharmacy.services)
        pharmacy.proprietaire = data.get('proprietaire', pharmacy.proprietaire)
        pharmacy.type_etablissement = data.get('type_etablissement', pharmacy.type_etablissement)
        pharmacy.categorie_emplacement = data.get('categorie_emplacement', pharmacy.categorie_emplacement)
        pharmacy.is_garde = data.get('is_garde', pharmacy.is_garde)
        pharmacy.is_verified = data.get('is_verified', pharmacy.is_verified)
        
        if 'latitude' in data:
            pharmacy.latitude = data['latitude']
        if 'longitude' in data:
            pharmacy.longitude = data['longitude']
        
        db.session.commit()
        return pharmacy
    
    @staticmethod
    def delete_pharmacy(pharmacy):
        db.session.delete(pharmacy)
        db.session.commit()
    
    @staticmethod
    def toggle_garde(pharmacy):
        pharmacy.is_garde = not pharmacy.is_garde
        db.session.commit()
        return pharmacy.is_garde
    
    @staticmethod
    def validate_location(pharmacy, admin_id):
        pharmacy.location_validated = True
        pharmacy.validated_at = datetime.utcnow()
        pharmacy.validated_by_admin_id = admin_id
        db.session.commit()
        return pharmacy
    
    @staticmethod
    def invalidate_location(pharmacy):
        pharmacy.location_validated = False
        pharmacy.validated_at = None
        pharmacy.validated_by_admin_id = None
        db.session.commit()
        return pharmacy
    
    @staticmethod
    def update_coordinates(pharmacy, latitude, longitude):
        pharmacy.latitude = latitude
        pharmacy.longitude = longitude
        pharmacy.location_validated = False
        pharmacy.validated_at = None
        pharmacy.validated_by_admin_id = None
        db.session.commit()
        return pharmacy
