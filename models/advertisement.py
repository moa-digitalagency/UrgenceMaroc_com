"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

models/advertisement.py - Modèles Publicités
Ce fichier définit les modèles Advertisement pour les publicités (image/vidéo)
et AdSettings pour la configuration du système publicitaire.
"""

from extensions import db
from datetime import datetime
import json


class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    media_type = db.Column(db.String(20), default='image')
    image_filename = db.Column(db.String(255))
    video_url = db.Column(db.String(500))

    cta_text = db.Column(db.String(100), default='En savoir plus')
    cta_url = db.Column(db.String(500))

    skip_delay = db.Column(db.Integer, default=5)

    is_active = db.Column(db.Boolean, default=True)
    priority = db.Column(db.Integer, default=0)

    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    view_count = db.Column(db.Integer, default=0)
    click_count = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_image_url(self):
        if self.image_filename:
            return f'/static/uploads/ads/{self.image_filename}'
        return None

    def is_currently_active(self):
        if not self.is_active:
            return False
        now = datetime.utcnow()
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description or '',
            'media_type': self.media_type,
            'image_url': self.get_image_url(),
            'video_url': self.video_url or '',
            'cta_text': self.cta_text or 'En savoir plus',
            'cta_url': self.cta_url or '',
            'skip_delay': self.skip_delay or 5,
            'is_active': self.is_active,
            'priority': self.priority
        }


class AdSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    ads_enabled = db.Column(db.Boolean, default=True)

    trigger_type = db.Column(db.String(50), default='time')

    time_delay = db.Column(db.Integer, default=60)
    time_repeat = db.Column(db.Boolean, default=True)
    time_interval = db.Column(db.Integer, default=300)

    page_count = db.Column(db.Integer, default=3)

    refresh_show = db.Column(db.Boolean, default=False)
    refresh_count = db.Column(db.Integer, default=1)

    default_skip_delay = db.Column(db.Integer, default=5)

    max_ads_per_session = db.Column(db.Integer, default=10)

    cooldown_after_skip = db.Column(db.Integer, default=60)
    cooldown_after_click = db.Column(db.Integer, default=300)

    show_on_mobile = db.Column(db.Boolean, default=True)
    show_on_desktop = db.Column(db.Boolean, default=True)

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def get_settings():
        settings = AdSettings.query.first()
        if not settings:
            settings = AdSettings()
            db.session.add(settings)
            db.session.commit()
        return settings

    def to_dict(self):
        return {
            'ads_enabled': self.ads_enabled,
            'trigger_type': self.trigger_type,
            'time_delay': self.time_delay,
            'time_repeat': self.time_repeat,
            'time_interval': self.time_interval,
            'page_count': self.page_count,
            'refresh_show': self.refresh_show,
            'refresh_count': self.refresh_count,
            'default_skip_delay': self.default_skip_delay,
            'max_ads_per_session': self.max_ads_per_session,
            'cooldown_after_skip': self.cooldown_after_skip,
            'cooldown_after_click': self.cooldown_after_click,
            'show_on_mobile': self.show_on_mobile,
            'show_on_desktop': self.show_on_desktop
        }
