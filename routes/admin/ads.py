"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

routes/admin/ads.py - Gestion des publicités
Ce fichier gère le CRUD des publicités (images/vidéos) et les paramètres
de déclenchement du système publicitaire.
"""

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from models.advertisement import Advertisement, AdSettings
from extensions import db, csrf
from datetime import datetime
from routes.admin import admin_bp, allowed_file, get_upload_path, safe_delete_upload, save_upload_file


@admin_bp.route('/ads')
@login_required
def list_ads():
    ads = Advertisement.query.order_by(Advertisement.priority.desc(), Advertisement.created_at.desc()).all()
    return render_template('admin/ads.html', ads=ads)


@admin_bp.route('/ad/add', methods=['GET', 'POST'])
@login_required
def add_ad():
    if request.method == 'POST':
        image_filename = None
        if request.form.get('media_type') == 'image' and 'image_file' in request.files:
            file = request.files['image_file']
            image_filename = save_upload_file(file, 'ads', '')
        
        start_date = None
        end_date = None
        if request.form.get('start_date'):
            start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%dT%H:%M')
        if request.form.get('end_date'):
            end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%dT%H:%M')
        
        ad = Advertisement(
            title=request.form.get('title'),
            description=request.form.get('description', ''),
            media_type=request.form.get('media_type', 'image'),
            image_filename=image_filename,
            video_url=request.form.get('video_url', ''),
            cta_text=request.form.get('cta_text', 'En savoir plus'),
            cta_url=request.form.get('cta_url', ''),
            skip_delay=int(request.form.get('skip_delay', 5)) or 5,
            priority=int(request.form.get('priority', 0)),
            start_date=start_date,
            end_date=end_date,
            is_active=request.form.get('is_active') == 'on'
        )
        db.session.add(ad)
        db.session.commit()
        flash('Publicité ajoutée avec succès', 'success')
        return redirect(url_for('admin.list_ads'))
    
    return render_template('admin/ad_form.html', ad=None)


@admin_bp.route('/ad/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_ad(id):
    ad = Advertisement.query.get_or_404(id)
    
    if request.method == 'POST':
        if request.form.get('media_type') == 'image':
            if 'image_file' in request.files:
                file = request.files['image_file']
                if file and file.filename and allowed_file(file.filename):
                    if ad.image_filename:
                        safe_delete_upload(ad.image_filename, 'ads')
                    ad.image_filename = save_upload_file(file, 'ads', '')
            
            if request.form.get('remove_image') == 'on':
                if ad.image_filename:
                    safe_delete_upload(ad.image_filename, 'ads')
                    ad.image_filename = None
        
        start_date = None
        end_date = None
        if request.form.get('start_date'):
            start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%dT%H:%M')
        if request.form.get('end_date'):
            end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%dT%H:%M')
        
        ad.title = request.form.get('title')
        ad.description = request.form.get('description', '')
        ad.media_type = request.form.get('media_type', 'image')
        ad.video_url = request.form.get('video_url', '')
        ad.cta_text = request.form.get('cta_text', 'En savoir plus')
        ad.cta_url = request.form.get('cta_url', '')
        ad.skip_delay = int(request.form.get('skip_delay', 5)) or 5
        ad.priority = int(request.form.get('priority', 0))
        ad.start_date = start_date
        ad.end_date = end_date
        ad.is_active = request.form.get('is_active') == 'on'
        
        db.session.commit()
        flash('Publicité mise à jour', 'success')
        return redirect(url_for('admin.list_ads'))
    
    return render_template('admin/ad_form.html', ad=ad)


@admin_bp.route('/ad/<int:id>/toggle', methods=['POST'])
@login_required
@csrf.exempt
def toggle_ad(id):
    ad = Advertisement.query.get_or_404(id)
    ad.is_active = not ad.is_active
    db.session.commit()
    return jsonify({'success': True, 'is_active': ad.is_active})


@admin_bp.route('/ad/<int:id>/delete', methods=['POST'])
@login_required
def delete_ad(id):
    ad = Advertisement.query.get_or_404(id)
    if ad.image_filename:
        safe_delete_upload(ad.image_filename, 'ads')
    db.session.delete(ad)
    db.session.commit()
    flash('Publicité supprimée', 'success')
    return redirect(url_for('admin.list_ads'))


@admin_bp.route('/ads/settings', methods=['GET', 'POST'])
@login_required
def ad_settings():
    settings = AdSettings.get_settings()
    
    if request.method == 'POST':
        settings.ads_enabled = request.form.get('ads_enabled') == 'on'
        settings.trigger_type = request.form.get('trigger_type', 'time')
        settings.time_delay = int(request.form.get('time_delay', 60))
        settings.time_repeat = request.form.get('time_repeat') == 'on'
        settings.time_interval = int(request.form.get('time_interval', 300))
        settings.page_count = int(request.form.get('page_count', 3))
        settings.refresh_show = request.form.get('refresh_show') == 'on'
        settings.refresh_count = int(request.form.get('refresh_count', 1))
        settings.default_skip_delay = int(request.form.get('default_skip_delay', 5))
        settings.max_ads_per_session = int(request.form.get('max_ads_per_session', 10))
        settings.cooldown_after_skip = int(request.form.get('cooldown_after_skip', 60))
        settings.cooldown_after_click = int(request.form.get('cooldown_after_click', 300))
        settings.show_on_mobile = request.form.get('show_on_mobile') == 'on'
        settings.show_on_desktop = request.form.get('show_on_desktop') == 'on'
        
        db.session.commit()
        flash('Paramètres enregistrés avec succès', 'success')
        return redirect(url_for('admin.ad_settings'))
    
    return render_template('admin/ad_settings.html', settings=settings)
