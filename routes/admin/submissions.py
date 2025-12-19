"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

routes/admin/submissions.py - Gestion des soumissions
Ce fichier gère l'approbation/rejet des soumissions utilisateurs:
localisations GPS, corrections d'info, suggestions et propositions de pharmacies.
"""

from flask import jsonify
from flask_login import login_required, current_user
from models.pharmacy import Pharmacy
from models.submission import LocationSubmission, InfoSubmission, Suggestion, PharmacyProposal
from extensions import db, csrf
from datetime import datetime
from routes.admin import admin_bp, get_json_or_400
import random
import string


@admin_bp.route('/location-submission/<int:id>/approve', methods=['POST'])
@login_required
@csrf.exempt
def approve_location_submission(id):
    submission = LocationSubmission.query.get_or_404(id)
    pharmacy = submission.pharmacy
    
    pharmacy.latitude = submission.latitude
    pharmacy.longitude = submission.longitude
    pharmacy.location_validated = True
    pharmacy.validated_at = datetime.utcnow()
    pharmacy.validated_by_admin_id = current_user.id
    
    submission.status = 'approved'
    submission.reviewed_at = datetime.utcnow()
    submission.reviewed_by_admin_id = current_user.id
    
    db.session.commit()
    
    return jsonify({'success': True})


@admin_bp.route('/location-submission/<int:id>/reject', methods=['POST'])
@login_required
@csrf.exempt
def reject_location_submission(id):
    submission = LocationSubmission.query.get_or_404(id)
    
    submission.status = 'rejected'
    submission.reviewed_at = datetime.utcnow()
    submission.reviewed_by_admin_id = current_user.id
    
    db.session.commit()
    
    return jsonify({'success': True})


@admin_bp.route('/info-submission/<int:id>/approve', methods=['POST'])
@login_required
@csrf.exempt
def approve_info_submission(id):
    submission = InfoSubmission.query.get_or_404(id)
    pharmacy = submission.pharmacy
    
    if hasattr(pharmacy, submission.field_name):
        setattr(pharmacy, submission.field_name, submission.proposed_value)
    
    submission.status = 'approved'
    submission.reviewed_at = datetime.utcnow()
    submission.reviewed_by_admin_id = current_user.id
    
    db.session.commit()
    
    return jsonify({'success': True})


@admin_bp.route('/info-submission/<int:id>/reject', methods=['POST'])
@login_required
@csrf.exempt
def reject_info_submission(id):
    submission = InfoSubmission.query.get_or_404(id)
    
    submission.status = 'rejected'
    submission.reviewed_at = datetime.utcnow()
    submission.reviewed_by_admin_id = current_user.id
    
    db.session.commit()
    
    return jsonify({'success': True})


@admin_bp.route('/suggestion/<int:id>/respond', methods=['POST'])
@login_required
@csrf.exempt
def respond_suggestion(id):
    suggestion = Suggestion.query.get_or_404(id)
    data = get_json_or_400()
    
    try:
        suggestion.admin_response = data.get('response', '')
        suggestion.status = 'resolved'
        suggestion.reviewed_at = datetime.utcnow()
        suggestion.reviewed_by_admin_id = current_user.id
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Erreur lors de la mise à jour'}), 500


@admin_bp.route('/suggestion/<int:id>/archive', methods=['POST'])
@login_required
@csrf.exempt
def archive_suggestion(id):
    suggestion = Suggestion.query.get_or_404(id)
    
    suggestion.status = 'archived'
    suggestion.reviewed_at = datetime.utcnow()
    suggestion.reviewed_by_admin_id = current_user.id
    
    db.session.commit()
    
    return jsonify({'success': True})


@admin_bp.route('/pharmacy-proposal/<int:id>/approve', methods=['POST'])
@login_required
@csrf.exempt
def approve_pharmacy_proposal(id):
    proposal = PharmacyProposal.query.get_or_404(id)
    
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    pharmacy = Pharmacy(
        code=f"NEW{code}",
        nom=proposal.nom,
        ville=proposal.ville,
        quartier=proposal.quartier,
        telephone=proposal.telephone,
        bp=proposal.bp,
        horaires=proposal.horaires,
        services=proposal.services,
        proprietaire=proposal.proprietaire,
        type_etablissement=proposal.type_etablissement or 'pharmacie_generale',
        categorie_emplacement=proposal.categorie_emplacement or 'standard',
        is_garde=proposal.is_garde,
        latitude=proposal.latitude,
        longitude=proposal.longitude,
        is_verified=False
    )
    
    db.session.add(pharmacy)
    
    proposal.status = 'approved'
    proposal.reviewed_at = datetime.utcnow()
    proposal.reviewed_by_admin_id = current_user.id
    
    db.session.commit()
    
    return jsonify({'success': True, 'pharmacy_id': pharmacy.id})


@admin_bp.route('/pharmacy-proposal/<int:id>/reject', methods=['POST'])
@login_required
@csrf.exempt
def reject_pharmacy_proposal(id):
    proposal = PharmacyProposal.query.get_or_404(id)
    
    proposal.status = 'rejected'
    proposal.reviewed_at = datetime.utcnow()
    proposal.reviewed_by_admin_id = current_user.id
    
    db.session.commit()
    
    return jsonify({'success': True})
