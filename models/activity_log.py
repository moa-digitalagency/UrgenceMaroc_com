"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

models/activity_log.py - Modèle de logs d'activité
Ce fichier définit le modèle pour enregistrer toutes les activités du site:
requêtes, erreurs, actions admin, etc.
"""

from extensions import db
from datetime import datetime


class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    method = db.Column(db.String(10))
    path = db.Column(db.String(500))
    status_code = db.Column(db.Integer)
    response_time_ms = db.Column(db.Float)
    log_type = db.Column(db.String(50), default='request', index=True)
    log_level = db.Column(db.String(20), default='info', index=True)
    message = db.Column(db.Text)
    details = db.Column(db.Text)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    
    admin = db.relationship('Admin', foreign_keys=[admin_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'ip_address': self.ip_address or '',
            'user_agent': self.user_agent or '',
            'method': self.method or '',
            'path': self.path or '',
            'status_code': self.status_code,
            'response_time_ms': self.response_time_ms,
            'log_type': self.log_type or 'request',
            'log_level': self.log_level or 'info',
            'message': self.message or '',
            'details': self.details or '',
            'admin_username': self.admin.username if self.admin else None
        }
    
    @classmethod
    def log_request(cls, request, response, response_time_ms=None, admin_id=None):
        log = cls(
            ip_address=request.headers.get('X-Forwarded-For', request.remote_addr),
            user_agent=request.headers.get('User-Agent', '')[:500],
            method=request.method,
            path=request.path[:500],
            status_code=response.status_code,
            response_time_ms=response_time_ms,
            log_type='request',
            log_level='error' if response.status_code >= 500 else ('warning' if response.status_code >= 400 else 'info'),
            admin_id=admin_id
        )
        db.session.add(log)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
        return log
    
    @classmethod
    def log_action(cls, action_type, message, details=None, ip_address=None, admin_id=None, log_level='info'):
        log = cls(
            ip_address=ip_address,
            log_type=action_type,
            log_level=log_level,
            message=message,
            details=details,
            admin_id=admin_id
        )
        db.session.add(log)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
        return log
    
    @classmethod
    def log_error(cls, message, details=None, ip_address=None, path=None, admin_id=None):
        log = cls(
            ip_address=ip_address,
            path=path,
            log_type='error',
            log_level='error',
            message=message,
            details=details,
            admin_id=admin_id
        )
        db.session.add(log)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
        return log
    
    @classmethod
    def log_auth(cls, event_type, message, ip_address=None, admin_id=None, success=True):
        log = cls(
            ip_address=ip_address,
            log_type='auth',
            log_level='info' if success else 'warning',
            message=f"{event_type}: {message}",
            admin_id=admin_id
        )
        db.session.add(log)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
        return log
