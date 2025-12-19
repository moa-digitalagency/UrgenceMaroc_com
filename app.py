"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

app.py - Application principale Flask
Ce fichier configure et initialise l'application Flask, incluant la base de données,
l'authentification, les routes et les gestionnaires d'erreurs.
"""

import os
import logging
import time
from flask import Flask, jsonify, render_template, request, g
from flask_login import current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

from extensions import db, login_manager, csrf
from routes import public_bp, admin_bp
from security.auth import init_login_manager, create_default_admin

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)

    session_secret = os.environ.get("SESSION_SECRET")
    if not session_secret:
        raise RuntimeError("SESSION_SECRET environment variable is required")

    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is required")

    app.secret_key = session_secret
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

    is_production = os.environ.get('FLASK_ENV', 'production') == 'production'
    use_https = os.environ.get('USE_HTTPS', 'true').lower() == 'true'
    
    app.config['SESSION_COOKIE_SECURE'] = use_https
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    app.config['WTF_CSRF_TIME_LIMIT'] = 3600

    db.init_app(app)
    csrf.init_app(app)
    init_login_manager(app)
    
    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )
    app.limiter = limiter
    
    # Add security headers
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'accelerometer=(), camera=(), microphone=(), geolocation=()'
        # CSP: Allow CDN for styles/scripts but block inline
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' cdn.tailwindcss.com cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' cdn.tailwindcss.com fonts.googleapis.com; img-src 'self' data: https:; font-src 'self' fonts.gstatic.com; connect-src 'self' tile.openstreetmap.org; frame-ancestors 'none';"
        # Hide server info
        response.headers['Server'] = 'WebServer'
        return response

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    register_error_handlers(app)
    register_request_logging(app)

    with app.app_context():
        db.create_all()
        create_default_admin()

    return app


def register_request_logging(app):
    from models.activity_log import ActivityLog
    
    @app.before_request
    def before_request():
        g.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        if hasattr(g, 'start_time'):
            response_time_ms = (time.time() - g.start_time) * 1000
        else:
            response_time_ms = None
        
        skip_paths = ['/static/', '/favicon', '/api/pharmacies', '/api/stats', '/api/popups', '/api/ads/settings', '/api/ads/random']
        if any(request.path.startswith(p) for p in skip_paths):
            return response
        
        is_admin_path = request.path.startswith('/admin')
        is_post_request = request.method == 'POST'
        is_error = response.status_code >= 400
        
        should_log = is_error or (is_admin_path and is_post_request) or (is_post_request and response.status_code < 300)
        
        if not should_log:
            return response
        
        try:
            admin_id = None
            if current_user and hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
                admin_id = current_user.id
            
            if response.status_code >= 500:
                log_level = 'error'
            elif response.status_code >= 400:
                log_level = 'warning'
            elif response.status_code >= 200 and response.status_code < 300:
                log_level = 'success'
            else:
                log_level = 'info'
            
            log = ActivityLog(
                ip_address=request.headers.get('X-Forwarded-For', request.remote_addr),
                user_agent=request.headers.get('User-Agent', '')[:500] if request.headers.get('User-Agent') else None,
                method=request.method,
                path=request.path[:500],
                status_code=response.status_code,
                response_time_ms=response_time_ms,
                log_type='request',
                log_level=log_level,
                admin_id=admin_id
            )
            db.session.add(log)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.debug(f"Failed to log request: {e}")
        
        return response


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        if hasattr(error, 'description'):
            message = error.description
        else:
            message = 'Requête invalide'
        return jsonify({'success': False, 'error': message}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'error': 'Ressource non trouvée'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        logger.error(f"Internal error: {error}")
        return jsonify({'success': False, 'error': 'Erreur interne du serveur'}), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        db.session.rollback()
        logger.error(f"Unhandled exception: {error}", exc_info=True)
        return jsonify({'success': False, 'error': 'Une erreur inattendue est survenue'}), 500


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
