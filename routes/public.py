"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

routes/public.py - Routes publiques
Ce fichier définit les routes accessibles au public: page d'accueil, API pharmacies,
soumissions de localisation/info, suggestions, popups et publicités.
"""

from flask import Blueprint, render_template, jsonify, request, abort, Response, url_for
from markupsafe import Markup
from services.pharmacy_service import PharmacyService
from models.submission import LocationSubmission, InfoSubmission, PharmacyView, Suggestion, PharmacyProposal
from models.pharmacy import Pharmacy
from models.emergency_contact import EmergencyContact
from models.site_settings import PopupMessage, SiteSettings
from models.advertisement import Advertisement, AdSettings
from extensions import db, csrf
from datetime import datetime

public_bp = Blueprint('public', __name__)


def get_json_or_400():
    """Safely get JSON from request, return 400 if invalid."""
    try:
        data = request.get_json(force=False, silent=True)
        if data is None:
            abort(400, description='Invalid JSON data')
        return data
    except Exception:
        abort(400, description='Invalid JSON data')


def is_admin_path(url_path):
    """Check if URL path is an admin page (blocks /admin and all its subpages)."""
    path = url_path.lower()
    return path.startswith('/admin/') or path == '/admin'


def generate_sitemap():
    """
    Generate dynamic sitemap with all public pages and active pharmacies.
    Automatically excludes ALL admin pages and their subpages:
    - /admin
    - /admin/
    - /admin/auth
    - /admin/dashboard
    - /admin/pharmacy
    - /admin/submissions
    - /admin/emergency
    - /admin/settings
    - /admin/ads
    - /admin/logs
    And all their subpages...
    """
    try:
        base_url = request.url_root.rstrip('/')
        
        sitemap_entries = []
        
        # Add home page (public)
        sitemap_entries.append({
            'url': base_url + '/',
            'lastmod': datetime.utcnow().isoformat(),
            'priority': '1.0',
            'changefreq': 'daily'
        })
        
        # Add all active pharmacies (public pages - linked from home)
        try:
            pharmacies = Pharmacy.query.filter_by(is_active=True).all()
            for pharmacy in pharmacies:
                lastmod = pharmacy.updated_at or pharmacy.created_at or datetime.utcnow()
                pharmacy_url = base_url + f'/#pharmacy-{pharmacy.id}'
                
                # Double-check: ensure no admin paths are added
                if not is_admin_path(pharmacy_url):
                    sitemap_entries.append({
                        'url': pharmacy_url,
                        'lastmod': lastmod.isoformat() if hasattr(lastmod, 'isoformat') else str(lastmod),
                        'priority': '0.8',
                        'changefreq': 'weekly'
                    })
        except Exception:
            pass  # Continue without pharmacies if database fails
        
        # Generate XML with all public pages only
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        ]
        
        for entry in sitemap_entries:
            xml_lines.append('  <url>')
            xml_lines.append(f'    <loc>{entry["url"]}</loc>')
            xml_lines.append(f'    <lastmod>{entry["lastmod"]}</lastmod>')
            xml_lines.append(f'    <changefreq>{entry["changefreq"]}</changefreq>')
            xml_lines.append(f'    <priority>{entry["priority"]}</priority>')
            xml_lines.append('  </url>')
        
        xml_lines.append('</urlset>')
        
        return '\n'.join(xml_lines)
    except Exception:
        # Fallback: return empty sitemap with home page only
        return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'


def generate_robots_txt():
    """
    Generate dynamic robots.txt blocking ALL admin pages and their subpages.
    Blocks:
    - /admin (the admin page itself)
    - /admin/ (all admin subpages including auth, dashboard, pharmacy, etc.)
    
    Allows all other public pages.
    References the sitemap for search engines.
    """
    try:
        base_url = request.url_root.rstrip('/')
        sitemap_url = base_url + '/sitemap.xml'
        
        robots_lines = [
            '# UrgenceMaroc.com - Robots.txt Configuration',
            '# Generated dynamically to manage search engine crawling',
            '',
            'User-agent: *',
            'Allow: /',
            '',
            '# Disallow all admin pages and their subpages',
            '# This includes: /admin/auth, /admin/dashboard, /admin/pharmacy,',
            '# /admin/submissions, /admin/emergency, /admin/settings, /admin/ads, /admin/logs',
            'Disallow: /admin/',
            'Disallow: /admin',
            '',
            '# Reference to the sitemap containing all public pages',
            f'Sitemap: {sitemap_url}'
        ]
        
        return '\n'.join(robots_lines)
    except Exception:
        # Fallback
        return 'User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /admin'


@public_bp.route('/sitemap.xml')
def sitemap():
    """Serve dynamic sitemap XML (excluding /admin)."""
    sitemap_xml = generate_sitemap()
    return Response(sitemap_xml, mimetype='application/xml')


@public_bp.route('/robots.txt')
def robots():
    """Serve dynamic robots.txt (excluding /admin)."""
    robots_txt = generate_robots_txt()
    return Response(robots_txt, mimetype='text/plain')


@public_bp.route('/')
def index():
    villes = PharmacyService.get_distinct_cities()
    total_pharmacies = Pharmacy.query.count()
    
    national_contacts = EmergencyContact.query.filter_by(is_national=True, is_active=True).order_by(EmergencyContact.ordering).all()
    city_contacts = EmergencyContact.query.filter_by(is_national=False, is_active=True).order_by(EmergencyContact.ordering).all()
    
    contacts_by_city = {}
    for contact in city_contacts:
        if contact.ville not in contacts_by_city:
            contacts_by_city[contact.ville] = []
        contacts_by_city[contact.ville].append(contact)
    
    header_code = SiteSettings.get('header_code', '')
    footer_code = SiteSettings.get('footer_code', '')
    favicon_url = SiteSettings.get_favicon_url()
    logo_url = SiteSettings.get_logo_url()
    og_image_url = SiteSettings.get_og_image_url()
    site_name = SiteSettings.get('site_name', 'UrgenceMaroc.com')
    og_title = SiteSettings.get('og_title', 'UrgenceMaroc.com - Trouvez votre pharmacie')
    og_description = SiteSettings.get('og_description', 'Annuaire complet des pharmacies au Maroc')
    og_type = SiteSettings.get('og_type', 'website')
    og_locale = SiteSettings.get('og_locale', 'fr_FR')
    meta_description = SiteSettings.get('meta_description', og_description)
    meta_keywords = SiteSettings.get('meta_keywords', 'pharmacie maroc, pharmacie garde, urgence maroc')
    meta_author = SiteSettings.get('meta_author', 'MOA Digital Agency LLC')
    twitter_card = SiteSettings.get('twitter_card', 'summary_large_image')
    twitter_handle = SiteSettings.get('twitter_handle', '')
    twitter_title = SiteSettings.get('twitter_title', og_title)
    twitter_description = SiteSettings.get('twitter_description', og_description)
    canonical_url = SiteSettings.get('canonical_url', '')
    google_site_verification = SiteSettings.get('google_site_verification', '')
    structured_data = SiteSettings.get('structured_data', '')
    
    return render_template('index.html', 
                          villes=villes, 
                          total_pharmacies=total_pharmacies,
                          national_contacts=national_contacts,
                          contacts_by_city=contacts_by_city,
                          header_code=Markup(header_code) if header_code else '',
                          footer_code=Markup(footer_code) if footer_code else '',
                          favicon_url=favicon_url,
                          logo_url=logo_url,
                          og_image_url=og_image_url,
                          site_name=site_name,
                          og_title=og_title,
                          og_description=og_description,
                          og_type=og_type,
                          og_locale=og_locale,
                          meta_description=meta_description,
                          meta_keywords=meta_keywords,
                          meta_author=meta_author,
                          twitter_card=twitter_card,
                          twitter_handle=twitter_handle,
                          twitter_title=twitter_title,
                          twitter_description=twitter_description,
                          canonical_url=canonical_url,
                          google_site_verification=google_site_verification,
                          structured_data=Markup(structured_data) if structured_data else '')


@public_bp.route('/api/pharmacies')
def get_pharmacies():
    search = request.args.get('search', '').lower()
    ville = request.args.get('ville', '')
    garde_only = request.args.get('garde', '') == 'true'
    gare_only = request.args.get('gare', '') == 'true'
    
    pharmacies = PharmacyService.get_all_pharmacies(
        search=search,
        ville=ville,
        garde_only=garde_only,
        gare_only=gare_only
    )
    
    return jsonify([p.to_dict() for p in pharmacies])


@public_bp.route('/api/stats')
def get_stats():
    return jsonify(PharmacyService.get_stats())


@public_bp.route('/api/pharmacy/<int:id>/view', methods=['POST'])
@csrf.exempt
def record_view(id):
    pharmacy = Pharmacy.query.get_or_404(id)
    try:
        view = PharmacyView(pharmacy_id=pharmacy.id)
        db.session.add(view)
        db.session.commit()
        return jsonify({'success': True})
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Erreur lors de l\'enregistrement'}), 500


@public_bp.route('/api/pharmacy/<int:id>/submit-location', methods=['POST'])
@csrf.exempt
def submit_location(id):
    pharmacy = Pharmacy.query.get_or_404(id)
    data = get_json_or_400()
    
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if latitude is None or longitude is None:
        return jsonify({'success': False, 'error': 'Coordonnées manquantes'}), 400
    
    try:
        submission = LocationSubmission(
            pharmacy_id=pharmacy.id,
            latitude=float(latitude),
            longitude=float(longitude),
            submitted_by_name=data.get('name', ''),
            submitted_by_phone=data.get('phone', ''),
            comment=data.get('comment', '')
        )
        db.session.add(submission)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Localisation soumise avec succès'})
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Coordonnées invalides'}), 400
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Erreur lors de la soumission'}), 500


@public_bp.route('/api/pharmacy/<int:id>/submit-info', methods=['POST'])
@csrf.exempt
def submit_info(id):
    pharmacy = Pharmacy.query.get_or_404(id)
    data = get_json_or_400()
    
    field_name = data.get('field_name')
    proposed_value = data.get('proposed_value')
    
    if not field_name or not proposed_value:
        return jsonify({'success': False, 'error': 'Informations manquantes'}), 400
    
    try:
        current_value = getattr(pharmacy, field_name, '') or ''
        
        submission = InfoSubmission(
            pharmacy_id=pharmacy.id,
            field_name=field_name,
            current_value=str(current_value),
            proposed_value=proposed_value,
            submitted_by_name=data.get('name', ''),
            submitted_by_phone=data.get('phone', ''),
            comment=data.get('comment', '')
        )
        db.session.add(submission)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Information soumise avec succès'})
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Erreur lors de la soumission'}), 500


@public_bp.route('/api/suggestions', methods=['POST'])
@csrf.exempt
def submit_suggestion():  # Rate limited: 100/hour
    data = get_json_or_400()
    
    category = data.get('category')
    subject = data.get('subject')
    message = data.get('message')
    
    if not category or not subject or not message:
        return jsonify({'success': False, 'error': 'Veuillez remplir tous les champs obligatoires'}), 400
    
    try:
        suggestion = Suggestion(
            category=category,
            subject=subject,
            message=message,
            submitted_by_name=data.get('name', ''),
            submitted_by_email=data.get('email', ''),
            submitted_by_phone=data.get('phone', '')
        )
        db.session.add(suggestion)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Suggestion envoyée avec succès'})
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Erreur lors de l\'envoi'}), 500


@public_bp.route('/api/pharmacy-proposal', methods=['POST'])
@csrf.exempt
def submit_pharmacy_proposal():
    data = get_json_or_400()
    
    nom = data.get('nom')
    ville = data.get('ville')
    
    if not nom or not ville:
        return jsonify({'success': False, 'error': 'Le nom et la ville sont obligatoires'}), 400
    
    try:
        proposal = PharmacyProposal(
            nom=nom,
            ville=ville,
            quartier=data.get('quartier', ''),
            telephone=data.get('telephone', ''),
            bp=data.get('bp', ''),
            horaires=data.get('horaires', ''),
            services=data.get('services', ''),
            proprietaire=data.get('proprietaire', ''),
            type_etablissement=data.get('type_etablissement', 'pharmacie_generale'),
            categorie_emplacement=data.get('categorie_emplacement', 'standard'),
            is_garde=data.get('is_garde', False),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            submitted_by_name=data.get('name', ''),
            submitted_by_email=data.get('email', ''),
            submitted_by_phone=data.get('phone', ''),
            comment=data.get('comment', '')
        )
        db.session.add(proposal)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Proposition de pharmacie envoyée avec succès'})
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Erreur lors de l\'envoi'}), 500


@public_bp.route('/api/popups')
def get_active_popups():
    popups = PopupMessage.query.filter_by(is_active=True).order_by(PopupMessage.ordering).all()
    return jsonify([p.to_dict() for p in popups])


@public_bp.route('/api/ads/settings')
def get_ad_settings():
    settings = AdSettings.get_settings()
    return jsonify(settings.to_dict())


@public_bp.route('/api/ads/random')
def get_random_ad():
    import random
    from datetime import datetime
    
    now = datetime.utcnow()
    active_ads = Advertisement.query.filter(
        Advertisement.is_active == True,
        db.or_(Advertisement.start_date == None, Advertisement.start_date <= now),
        db.or_(Advertisement.end_date == None, Advertisement.end_date >= now)
    ).all()
    
    if not active_ads:
        return jsonify(None)
    
    weighted_ads = []
    for ad in active_ads:
        weight = max(1, ad.priority + 1)
        weighted_ads.extend([ad] * weight)
    
    selected_ad = random.choice(weighted_ads)
    
    settings = AdSettings.get_settings()
    skip_delay = selected_ad.skip_delay if selected_ad.skip_delay > 0 else settings.default_skip_delay
    
    ad_data = selected_ad.to_dict()
    ad_data['skip_delay'] = skip_delay
    
    return jsonify(ad_data)


@public_bp.route('/api/ads/<int:id>/view', methods=['POST'])
@csrf.exempt
def record_ad_view(id):
    ad = Advertisement.query.get_or_404(id)
    try:
        ad.view_count = (ad.view_count or 0) + 1
        db.session.commit()
        return jsonify({'success': True})
    except Exception:
        db.session.rollback()
        return jsonify({'success': False}), 500


@public_bp.route('/api/ads/<int:id>/click', methods=['POST'])
@csrf.exempt
def record_ad_click(id):
    ad = Advertisement.query.get_or_404(id)
    try:
        ad.click_count = (ad.click_count or 0) + 1
        db.session.commit()
        return jsonify({'success': True})
    except Exception:
        db.session.rollback()
        return jsonify({'success': False}), 500


@public_bp.route('/api/emergency-contacts')
def get_emergency_contacts():
    """Get all active emergency contacts, sorted by national first, then by city."""
    national_contacts = EmergencyContact.query.filter_by(is_national=True, is_active=True).order_by(EmergencyContact.ordering).all()
    city_contacts = EmergencyContact.query.filter_by(is_national=False, is_active=True).order_by(EmergencyContact.ordering).all()
    
    contacts_data = {
        'national': [c.to_dict() for c in national_contacts],
        'by_city': {}
    }
    
    for contact in city_contacts:
        ville = contact.ville or 'Unknown'
        if ville not in contacts_data['by_city']:
            contacts_data['by_city'][ville] = []
        contacts_data['by_city'][ville].append(contact.to_dict())
    
    return jsonify(contacts_data)
