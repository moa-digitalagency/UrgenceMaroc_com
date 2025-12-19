"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

routes/admin/logs.py - Routes admin pour les logs
Ce fichier affiche la page des logs d'activité avec filtres et pagination.
"""

from flask import render_template, request
from flask_login import login_required
from models.activity_log import ActivityLog
from extensions import db
from sqlalchemy import desc
from routes.admin import admin_bp


@admin_bp.route('/logs')
@login_required
def view_logs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    log_type = request.args.get('type', '')
    log_level = request.args.get('level', '')
    search_ip = request.args.get('ip', '')
    search_path = request.args.get('path', '')
    
    query = ActivityLog.query
    
    if log_type:
        query = query.filter(ActivityLog.log_type == log_type)
    if log_level:
        query = query.filter(ActivityLog.log_level == log_level)
    if search_ip:
        query = query.filter(ActivityLog.ip_address.ilike(f'%{search_ip}%'))
    if search_path:
        query = query.filter(ActivityLog.path.ilike(f'%{search_path}%'))
    
    logs = query.order_by(desc(ActivityLog.timestamp)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    log_types = db.session.query(ActivityLog.log_type).distinct().all()
    log_types = [t[0] for t in log_types if t[0]]
    
    stats = {
        'total': ActivityLog.query.count(),
        'success': ActivityLog.query.filter(ActivityLog.log_level == 'success').count(),
        'errors': ActivityLog.query.filter(ActivityLog.log_level == 'error').count(),
        'warnings': ActivityLog.query.filter(ActivityLog.log_level == 'warning').count(),
        'requests': ActivityLog.query.filter(ActivityLog.log_type == 'request').count(),
        'auth': ActivityLog.query.filter(ActivityLog.log_type == 'auth').count(),
    }
    
    return render_template('admin/logs.html',
                         logs=logs,
                         log_types=log_types,
                         stats=stats,
                         current_type=log_type,
                         current_level=log_level,
                         current_ip=search_ip,
                         current_path=search_path)


@admin_bp.route('/logs/clear', methods=['POST'])
@login_required
def clear_logs():
    from flask import flash, redirect, url_for
    from flask_login import current_user
    
    days = request.form.get('days', 30, type=int)
    from datetime import datetime, timedelta
    cutoff = datetime.utcnow() - timedelta(days=days)
    
    try:
        count = ActivityLog.query.filter(ActivityLog.timestamp < cutoff).delete()
        db.session.commit()
        
        ActivityLog.log_action(
            'admin_action',
            f'Logs nettoyés: {count} entrées supprimées (plus de {days} jours)',
            admin_id=current_user.id if current_user.is_authenticated else None,
            ip_address=request.headers.get('X-Forwarded-For', request.remote_addr)
        )
        
        flash(f'{count} logs supprimés avec succès', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression: {str(e)}', 'error')
    
    return redirect(url_for('admin.view_logs'))
