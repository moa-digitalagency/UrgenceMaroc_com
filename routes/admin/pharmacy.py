"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

routes/admin/pharmacy.py - Gestion des pharmacies
Ce fichier gère le CRUD des pharmacies: ajout, modification, suppression,
gestion du statut de garde et validation des coordonnées GPS.
"""

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.pharmacy import Pharmacy
from services.pharmacy_service import PharmacyService
from utils.helpers import safe_float, CITY_COORDINATES
from extensions import db, csrf
from datetime import datetime, timedelta
from routes.admin import admin_bp, get_json_or_400


@admin_bp.route('/pharmacy/add', methods=['GET', 'POST'])
@login_required
def admin_add_pharmacy():
    if request.method == 'POST':
        data = {
            'code': request.form.get('code'),
            'nom': request.form.get('nom'),
            'ville': request.form.get('ville'),
            'quartier': request.form.get('quartier'),
            'telephone': request.form.get('telephone'),
            'bp': request.form.get('bp'),
            'horaires': request.form.get('horaires'),
            'services': request.form.get('services'),
            'proprietaire': request.form.get('proprietaire'),
            'type_etablissement': request.form.get('type_etablissement'),
            'categorie_emplacement': request.form.get('categorie_emplacement'),
            'is_garde': request.form.get('is_garde') == 'on',
            'is_verified': request.form.get('is_verified') == 'on',
            'latitude': safe_float(request.form.get('latitude')),
            'longitude': safe_float(request.form.get('longitude')),
            'location_validated': request.form.get('location_validated') == 'on'
        }
        PharmacyService.create_pharmacy(data)
        flash('Pharmacie ajoutée avec succès', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('admin/pharmacy_form.html', pharmacy=None, cities=list(CITY_COORDINATES.keys()))


@admin_bp.route('/pharmacy/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_pharmacy(id):
    pharmacy = PharmacyService.get_pharmacy_by_id(id)
    
    if request.method == 'POST':
        data = {
            'code': request.form.get('code'),
            'nom': request.form.get('nom'),
            'ville': request.form.get('ville'),
            'quartier': request.form.get('quartier'),
            'telephone': request.form.get('telephone'),
            'bp': request.form.get('bp'),
            'horaires': request.form.get('horaires'),
            'services': request.form.get('services'),
            'proprietaire': request.form.get('proprietaire'),
            'type_etablissement': request.form.get('type_etablissement'),
            'categorie_emplacement': request.form.get('categorie_emplacement'),
            'is_garde': request.form.get('is_garde') == 'on',
            'is_verified': request.form.get('is_verified') == 'on',
            'latitude': safe_float(request.form.get('latitude')),
            'longitude': safe_float(request.form.get('longitude'))
        }
        PharmacyService.update_pharmacy(pharmacy, data)
        flash('Pharmacie mise à jour avec succès', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('admin/pharmacy_form.html', pharmacy=pharmacy, cities=list(CITY_COORDINATES.keys()))


@admin_bp.route('/pharmacy/<int:id>/delete', methods=['POST'])
@login_required
def admin_delete_pharmacy(id):
    pharmacy = PharmacyService.get_pharmacy_by_id(id)
    PharmacyService.delete_pharmacy(pharmacy)
    flash('Pharmacie supprimée', 'success')
    return redirect(url_for('admin.admin_dashboard'))


@admin_bp.route('/pharmacy/<int:id>/garde', methods=['GET', 'POST'])
@login_required
def admin_pharmacy_garde(id):
    pharmacy = PharmacyService.get_pharmacy_by_id(id)
    
    if request.method == 'POST':
        start_date_str = request.form.get('start_date')
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = start_date + timedelta(days=7)
            
            pharmacy.is_garde = True
            pharmacy.garde_start_date = start_date
            pharmacy.garde_end_date = end_date
        else:
            pharmacy.is_garde = False
            pharmacy.garde_start_date = None
            pharmacy.garde_end_date = None
        
        db.session.commit()
        flash('Statut de garde mis à jour avec succès', 'success')
        tab = request.args.get('tab', 'pharmacies')
        return redirect(url_for('admin.admin_dashboard') + '#' + tab)
    
    return render_template('admin/pharmacy_garde.html', pharmacy=pharmacy)


@admin_bp.route('/pharmacy/<int:id>/toggle-garde', methods=['POST'])
@login_required
@csrf.exempt
def admin_toggle_garde(id):
    pharmacy = PharmacyService.get_pharmacy_by_id(id)
    is_garde = PharmacyService.toggle_garde(pharmacy)
    return jsonify({'success': True, 'is_garde': is_garde})


@admin_bp.route('/pharmacy/<int:id>/validate-location', methods=['POST'])
@login_required
@csrf.exempt
def admin_validate_location(id):
    pharmacy = PharmacyService.get_pharmacy_by_id(id)
    PharmacyService.validate_location(pharmacy, current_user.id)
    return jsonify({'success': True, 'location_validated': True})


@admin_bp.route('/pharmacy/<int:id>/invalidate-location', methods=['POST'])
@login_required
@csrf.exempt
def admin_invalidate_location(id):
    pharmacy = PharmacyService.get_pharmacy_by_id(id)
    PharmacyService.invalidate_location(pharmacy)
    return jsonify({'success': True, 'location_validated': False})


@admin_bp.route('/pharmacy/<int:id>/toggle-verified', methods=['POST'])
@login_required
@csrf.exempt
def admin_toggle_verified(id):
    pharmacy = PharmacyService.get_pharmacy_by_id(id)
    pharmacy.is_verified = not pharmacy.is_verified
    db.session.commit()
    return jsonify({'success': True, 'is_verified': pharmacy.is_verified})


@admin_bp.route('/pharmacy/<int:id>/update-coordinates', methods=['POST'])
@login_required
@csrf.exempt
def admin_update_coordinates(id):
    pharmacy = PharmacyService.get_pharmacy_by_id(id)
    data = get_json_or_400()
    latitude = safe_float(data.get('latitude'))
    longitude = safe_float(data.get('longitude'))
    
    if latitude is not None and longitude is not None:
        try:
            PharmacyService.update_coordinates(pharmacy, latitude, longitude)
            return jsonify({'success': True})
        except Exception:
            db.session.rollback()
            return jsonify({'success': False, 'error': 'Erreur lors de la mise à jour'}), 500
    
    return jsonify({'success': False, 'error': 'Coordonnées invalides'}), 400


@admin_bp.route('/pharmacy/<int:id>/set-garde', methods=['POST'])
@login_required
@csrf.exempt
def admin_set_garde(id):
    pharmacy = PharmacyService.get_pharmacy_by_id(id)
    data = get_json_or_400()
    
    try:
        start_date_str = data.get('start_date')
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = start_date + timedelta(days=7)
            
            pharmacy.is_garde = True
            pharmacy.garde_start_date = start_date
            pharmacy.garde_end_date = end_date
        else:
            pharmacy.is_garde = False
            pharmacy.garde_start_date = None
            pharmacy.garde_end_date = None
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'is_garde': pharmacy.is_garde,
            'garde_end_date': pharmacy.garde_end_date.isoformat() if pharmacy.garde_end_date else None
        })
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Erreur lors de la mise à jour'}), 500
