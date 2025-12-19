"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

routes/admin/settings.py - Paramètres du site
Ce fichier gère les paramètres globaux du site (logo, favicon, SEO)
et les popups/messages d'accueil.
"""

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from models.site_settings import SiteSettings, PopupMessage
from extensions import db, csrf
from routes.admin import admin_bp, allowed_file, get_upload_path, safe_delete_upload, save_upload_file


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def site_settings():
    if request.method == 'POST':
        settings_keys = [
            'site_name', 'site_description',
            'site_timezone', 'contact_email', 'contact_phone',
            'og_title', 'og_description', 'og_type', 'og_locale',
            'meta_description', 'meta_keywords', 'meta_author',
            'twitter_card', 'twitter_handle', 'twitter_title', 'twitter_description',
            'canonical_url', 'google_site_verification', 'bing_site_verification',
            'robots_txt', 'structured_data',
            'google_analytics_id', 'header_code', 'footer_code'
        ]
        
        for key in settings_keys:
            value = request.form.get(key, '')
            SiteSettings.set(key, value)
        
        if request.form.get('remove_logo') == 'on':
            old_filename = SiteSettings.get('site_logo_filename')
            if old_filename:
                safe_delete_upload(old_filename, 'settings')
                SiteSettings.set('site_logo_filename', '')
        
        if request.form.get('remove_favicon') == 'on':
            old_filename = SiteSettings.get('site_favicon_filename')
            if old_filename:
                safe_delete_upload(old_filename, 'settings')
                SiteSettings.set('site_favicon_filename', '')
        
        if request.form.get('remove_og_image') == 'on':
            old_filename = SiteSettings.get('og_image_filename')
            if old_filename:
                safe_delete_upload(old_filename, 'settings')
                SiteSettings.set('og_image_filename', '')
        
        if 'site_logo_file' in request.files:
            file = request.files['site_logo_file']
            if file and file.filename and allowed_file(file.filename):
                old_filename = SiteSettings.get('site_logo_filename')
                if old_filename:
                    safe_delete_upload(old_filename, 'settings')
                new_filename = save_upload_file(file, 'settings', 'logo_')
                if new_filename:
                    SiteSettings.set('site_logo_filename', new_filename)
        
        if 'site_favicon_file' in request.files:
            file = request.files['site_favicon_file']
            if file and file.filename and allowed_file(file.filename):
                old_filename = SiteSettings.get('site_favicon_filename')
                if old_filename:
                    safe_delete_upload(old_filename, 'settings')
                new_filename = save_upload_file(file, 'settings', 'favicon_')
                if new_filename:
                    SiteSettings.set('site_favicon_filename', new_filename)
        
        if 'og_image_file' in request.files:
            file = request.files['og_image_file']
            if file and file.filename and allowed_file(file.filename):
                old_filename = SiteSettings.get('og_image_filename')
                if old_filename:
                    safe_delete_upload(old_filename, 'settings')
                new_filename = save_upload_file(file, 'settings', 'og_image_')
                if new_filename:
                    SiteSettings.set('og_image_filename', new_filename)
        
        flash('Paramètres enregistrés avec succès', 'success')
        return redirect(url_for('admin.site_settings'))
    
    settings = SiteSettings.get_all()
    return render_template('admin/settings.html', settings=settings)


@admin_bp.route('/popups')
@login_required
def list_popups():
    popups = PopupMessage.query.order_by(PopupMessage.ordering, PopupMessage.created_at.desc()).all()
    return render_template('admin/popups.html', popups=popups)


@admin_bp.route('/popup/add', methods=['GET', 'POST'])
@login_required
def add_popup():
    if request.method == 'POST':
        image_filename = None
        if 'image_file' in request.files:
            file = request.files['image_file']
            image_filename = save_upload_file(file, 'popups', '')
        
        popup = PopupMessage(
            title=request.form.get('title'),
            description=request.form.get('description', ''),
            warning_text=request.form.get('warning_text', ''),
            image_url='',
            image_filename=image_filename,
            is_active=request.form.get('is_active') == 'on',
            show_once=request.form.get('show_once') == 'on',
            ordering=int(request.form.get('ordering', 0))
        )
        db.session.add(popup)
        db.session.commit()
        flash('Popup ajouté avec succès', 'success')
        return redirect(url_for('admin.list_popups'))
    
    return render_template('admin/popup_form.html', popup=None)


@admin_bp.route('/popup/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_popup(id):
    popup = PopupMessage.query.get_or_404(id)
    
    if request.method == 'POST':
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename and allowed_file(file.filename):
                if popup.image_filename:
                    safe_delete_upload(popup.image_filename, 'popups')
                popup.image_filename = save_upload_file(file, 'popups', '')
        
        if request.form.get('remove_image') == 'on':
            if popup.image_filename:
                safe_delete_upload(popup.image_filename, 'popups')
                popup.image_filename = None
            popup.image_url = ''
        
        popup.title = request.form.get('title')
        popup.description = request.form.get('description', '')
        popup.warning_text = request.form.get('warning_text', '')
        popup.is_active = request.form.get('is_active') == 'on'
        popup.show_once = request.form.get('show_once') == 'on'
        popup.ordering = int(request.form.get('ordering', 0))
        
        db.session.commit()
        flash('Popup mis à jour', 'success')
        return redirect(url_for('admin.list_popups'))
    
    return render_template('admin/popup_form.html', popup=popup)


@admin_bp.route('/popup/<int:id>/toggle', methods=['POST'])
@login_required
@csrf.exempt
def toggle_popup(id):
    popup = PopupMessage.query.get_or_404(id)
    popup.is_active = not popup.is_active
    db.session.commit()
    return jsonify({'success': True, 'is_active': popup.is_active})


@admin_bp.route('/popup/<int:id>/delete', methods=['POST'])
@login_required
def delete_popup(id):
    popup = PopupMessage.query.get_or_404(id)
    db.session.delete(popup)
    db.session.commit()
    flash('Popup supprimé', 'success')
    return redirect(url_for('admin.list_popups'))
