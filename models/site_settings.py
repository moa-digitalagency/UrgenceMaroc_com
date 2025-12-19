"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

models/site_settings.py - Modèles Paramètres du site
Ce fichier définit les modèles SiteSettings pour la configuration du site
(logo, favicon, SEO) et PopupMessage pour les messages d'accueil.
"""

from extensions import db
from datetime import datetime


class SiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @staticmethod
    def get(key, default=None):
        setting = SiteSettings.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    @staticmethod
    def set(key, value):
        setting = SiteSettings.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = SiteSettings(key=key, value=value)
            db.session.add(setting)
        db.session.commit()
        return setting
    
    @staticmethod
    def get_all():
        settings = SiteSettings.query.all()
        return {s.key: s.value for s in settings}
    
    @staticmethod
    def get_logo_url():
        filename = SiteSettings.get('site_logo_filename')
        if filename:
            return f'/static/uploads/settings/{filename}'
        return None
    
    @staticmethod
    def get_favicon_url():
        filename = SiteSettings.get('site_favicon_filename')
        if filename:
            return f'/static/uploads/settings/{filename}'
        return '/static/favicon.svg'
    
    @staticmethod
    def get_og_image_url():
        filename = SiteSettings.get('og_image_filename')
        if filename:
            return f'/static/uploads/settings/{filename}'
        return None


class PopupMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    warning_text = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    image_filename = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    show_once = db.Column(db.Boolean, default=True)
    ordering = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_image_url(self):
        if self.image_filename:
            return f'/static/uploads/popups/{self.image_filename}'
        return self.image_url or ''
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description or '',
            'warning_text': self.warning_text or '',
            'image_url': self.get_image_url(),
            'is_active': self.is_active,
            'show_once': self.show_once,
            'ordering': self.ordering
        }
