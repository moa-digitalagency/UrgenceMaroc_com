# Architecture technique

Ce document décrit l'organisation du code et le fonctionnement interne de la plateforme UrgenceMaroc.com.

## Vue d'ensemble

L'application repose sur une architecture web classique :

```
Navigateur (HTML/CSS/JS)
        ↓
Serveur Gunicorn (port 5000)
        ↓
Application Flask
        ↓
Base PostgreSQL
```

Le frontend utilise des templates Jinja2 servis par Flask. Le JavaScript est modulaire et gère les interactions côté client sans framework lourd.

## Structure des fichiers

```
urgence-maroc/
│
├── app.py                    # Configuration Flask et factory
├── main.py                   # Point d'entrée pour Gunicorn
├── extensions.py             # Extensions Flask (db, login, csrf)
│
├── models/                   # Modèles de données SQLAlchemy
│   ├── __init__.py           # Export de tous les modèles
│   ├── admin.py              # Comptes administrateurs
│   ├── pharmacy.py           # Pharmacies
│   ├── emergency_contact.py  # Numéros d'urgence
│   ├── submission.py         # Contributions utilisateurs
│   ├── site_settings.py      # Configuration et popups
│   ├── advertisement.py      # Publicités
│   └── activity_log.py       # Journal d'activité
│
├── routes/                   # Points d'accès HTTP
│   ├── __init__.py           # Export des blueprints
│   ├── public.py             # Routes publiques et API
│   └── admin/                # Administration
│       ├── __init__.py       # Blueprint admin et utilitaires
│       ├── auth.py           # Connexion/déconnexion
│       ├── dashboard.py      # Tableau de bord
│       ├── pharmacy.py       # CRUD pharmacies
│       ├── submissions.py    # Validation soumissions
│       ├── emergency.py      # Contacts d'urgence
│       ├── settings.py       # Paramètres du site
│       ├── ads.py            # Gestion publicités
│       └── logs.py           # Journal d'activité
│
├── services/                 # Logique métier
│   └── pharmacy_service.py   # Opérations pharmacies
│
├── security/                 # Authentification
│   └── auth.py               # Configuration Flask-Login
│
├── utils/                    # Fonctions utilitaires
│   └── helpers.py            # Coordonnées GPS, conversions
│
├── templates/                # Pages HTML (Jinja2)
│   ├── index.html            # Page principale publique
│   └── admin/                # Templates administration
│
├── static/                   # Fichiers statiques
│   ├── css/style.css         # Styles personnalisés
│   ├── js/                   # JavaScript modulaire
│   │   ├── config.js         # Configuration client
│   │   ├── map.js            # Carte Leaflet
│   │   ├── pharmacy.js       # Affichage pharmacies
│   │   ├── forms.js          # Formulaires
│   │   ├── popups.js         # Fenêtres modales
│   │   ├── ads.js            # Système publicitaire
│   │   └── app.js            # Orchestrateur principal
│   ├── uploads/              # Fichiers uploadés
│   │   ├── popups/           # Images des popups
│   │   ├── ads/              # Images publicitaires
│   │   └── settings/         # Logo, favicon, etc.
│   └── favicon.svg           # Icône par défaut
│
└── docs/                     # Documentation
```

## Modèles de données

### Admin

Comptes pour accéder à l'administration.

| Champ | Type | Description |
|-------|------|-------------|
| id | Integer | Identifiant |
| username | String(64) | Nom d'utilisateur |
| password_hash | String(256) | Mot de passe hashé |
| created_at | DateTime | Date de création |

### Pharmacy

Pharmacies référencées sur la plateforme.

| Champ | Type | Description |
|-------|------|-------------|
| id | Integer | Identifiant |
| code | String(20) | Code court unique (ex: LBV001) |
| nom | String(200) | Nom de la pharmacie |
| ville | String(100) | Ville |
| quartier | String(200) | Quartier ou adresse |
| telephone | String(100) | Numéro(s) de téléphone |
| bp | String(50) | Boîte postale |
| horaires | String(200) | Horaires d'ouverture |
| services | Text | Services proposés |
| proprietaire | String(200) | Nom du propriétaire |
| type_etablissement | String(100) | Type d'établissement |
| categorie_emplacement | String(50) | Catégorie de localisation |
| is_garde | Boolean | En service de garde |
| garde_start_date | DateTime | Début de la garde |
| garde_end_date | DateTime | Fin de la garde |
| latitude | Float | Coordonnée GPS |
| longitude | Float | Coordonnée GPS |
| location_validated | Boolean | GPS validé par admin |
| is_verified | Boolean | Informations vérifiées |
| validated_at | DateTime | Date de validation |
| validated_by_admin_id | Integer | Admin valideur |
| created_at | DateTime | Date de création |
| updated_at | DateTime | Dernière modification |

### EmergencyContact

Numéros d'urgence (police, pompiers, hôpitaux, etc.).

| Champ | Type | Description |
|-------|------|-------------|
| id | Integer | Identifiant |
| ville | String(100) | Ville (null si national) |
| service_type | String(50) | Type de service |
| label | String(200) | Nom affiché |
| phone_numbers | String(200) | Numéro(s) de téléphone |
| address | String(300) | Adresse physique |
| notes | Text | Informations complémentaires |
| is_national | Boolean | Service national |
| is_active | Boolean | Actif |
| ordering | Integer | Ordre d'affichage |

### Soumissions utilisateurs

Quatre modèles pour les contributions :

**LocationSubmission** : Coordonnées GPS proposées pour une pharmacie
- pharmacy_id, latitude, longitude, submitted_by_name/phone, comment, status

**InfoSubmission** : Correction d'information
- pharmacy_id, field_name, current_value, proposed_value, submitted_by_name/phone, comment, status

**PharmacyProposal** : Proposition de nouvelle pharmacie
- Tous les champs d'une pharmacie + submitted_by_name/email/phone, comment, status

**Suggestion** : Commentaire ou idée
- category, subject, message, submitted_by_name/email/phone, admin_response, status

Statuts possibles : pending, approved, rejected, resolved, archived

### Advertisement

Publicités affichées aux visiteurs.

| Champ | Type | Description |
|-------|------|-------------|
| id | Integer | Identifiant |
| title | String(200) | Titre |
| description | Text | Texte descriptif |
| media_type | String(20) | "image" ou "video" |
| image_filename | String(255) | Fichier image |
| video_url | String(500) | URL vidéo |
| cta_text | String(100) | Texte du bouton |
| cta_url | String(500) | Lien du bouton |
| skip_delay | Integer | Délai avant "Passer" |
| is_active | Boolean | Active |
| priority | Integer | Priorité (plus haut = plus fréquent) |
| start_date | DateTime | Date de début |
| end_date | DateTime | Date de fin |
| view_count | Integer | Nombre de vues |
| click_count | Integer | Nombre de clics |

### AdSettings

Configuration globale du système publicitaire (une seule ligne).

| Champ | Type | Description |
|-------|------|-------------|
| ads_enabled | Boolean | Activer les pubs |
| trigger_type | String(50) | Déclencheur (time, page, refresh) |
| time_delay | Integer | Délai initial (secondes) |
| time_repeat | Boolean | Répéter après intervalle |
| time_interval | Integer | Intervalle de répétition |
| page_count | Integer | Nombre de pages avant pub |
| refresh_show | Boolean | Afficher au rechargement |
| refresh_count | Integer | Après combien de rechargements |
| default_skip_delay | Integer | Délai "Passer" par défaut |
| max_ads_per_session | Integer | Maximum par session |
| cooldown_after_skip | Integer | Pause après "Passer" |
| cooldown_after_click | Integer | Pause après clic |
| show_on_mobile | Boolean | Afficher sur mobile |
| show_on_desktop | Boolean | Afficher sur desktop |

### PopupMessage

Messages popup affichés aux visiteurs.

| Champ | Type | Description |
|-------|------|-------------|
| id | Integer | Identifiant |
| title | String(200) | Titre |
| description | Text | Contenu principal |
| warning_text | Text | Texte d'avertissement |
| image_url | String(500) | URL image externe |
| image_filename | String(255) | Fichier image uploadé |
| is_active | Boolean | Actif |
| show_once | Boolean | Afficher une seule fois |
| ordering | Integer | Ordre d'affichage |

### SiteSettings

Configuration du site en clé-valeur.

Clés utilisées :
- site_name, meta_description, meta_keywords, meta_author
- og_title, og_description, og_type, og_locale, og_image_filename
- twitter_card, twitter_handle, twitter_title, twitter_description
- canonical_url, google_site_verification
- site_logo_filename, site_favicon_filename
- header_code, footer_code, structured_data

### ActivityLog

Journal des requêtes et actions.

| Champ | Type | Description |
|-------|------|-------------|
| id | Integer | Identifiant |
| ip_address | String(50) | Adresse IP |
| user_agent | String(500) | Navigateur |
| method | String(10) | Méthode HTTP |
| path | String(500) | Chemin de la requête |
| status_code | Integer | Code de réponse |
| response_time_ms | Float | Temps de réponse |
| log_type | String(50) | Type de log |
| log_level | String(20) | Niveau (info, warning, error, success) |
| admin_id | Integer | Admin connecté |
| created_at | DateTime | Date |

## Types et catégories

**Types d'établissement :**
- pharmacie_generale : Pharmacie standard
- depot_pharmaceutique : Dépôt de médicaments
- pharmacie_hospitaliere : Pharmacie d'hôpital

**Catégories d'emplacement :**
- standard : Emplacement standard
- gare : Proche de la gare
- hopital : Proche de l'hôpital
- aeroport : Proche de l'aéroport
- centre_commercial : Centre commercial
- marche : Proche du marché
- centre_ville : Centre-ville
- zone_residentielle : Zone résidentielle

**Types de services d'urgence :**
- police, pompiers, ambulance, hopital, clinique, sos_medecins, protection_civile, autre

## Coordonnées GPS des villes

Centres-villes prédéfinis pour le positionnement initial :

| Ville | Latitude | Longitude |
|-------|----------|-----------|
| Casablanca | 0.4162 | 9.4673 |
| Fès | -0.7193 | 8.7815 |
| Marrakech | -1.6333 | 13.5833 |
| Rabat | 1.6167 | 11.5833 |
| Agadir | -1.8667 | 11.0500 |
| Meknes | 0.5667 | 12.8667 |
| Tangier | -1.1333 | 12.4833 |
| Moanda | -1.5500 | 13.2000 |
| Ntom | 2.0000 | 11.0000 |

## Sécurité

**Mots de passe** : Hashés avec Werkzeug (algorithme par défaut, salage automatique)

**Sessions** : Gérées par Flask avec clé secrète en variable d'environnement. Cookies sécurisés (HttpOnly, SameSite=Lax, Secure en production).

**Protection CSRF** : Flask-WTF sur tous les formulaires. Token avec expiration d'une heure.

**Injections SQL** : Impossibles grâce à SQLAlchemy (requêtes préparées)

**XSS** : Échappement automatique par Jinja2. Fonction escapeHtml en JavaScript pour les contenus dynamiques.

**Uploads** : Extensions autorisées limitées (png, jpg, jpeg, gif, webp, svg, ico). Noms de fichiers sécurisés avec UUID.

**Accès admin** : Décorateur @login_required sur toutes les routes sensibles. Création automatique d'un compte admin au démarrage.

**Logging** : Journal d'activité pour les erreurs et actions admin. IP et user-agent enregistrés.

## Configuration

Variables d'environnement requises :

| Variable | Description |
|----------|-------------|
| DATABASE_URL | URL de connexion PostgreSQL |
| SESSION_SECRET | Clé secrète Flask (min. 32 caractères) |
| ADMIN_USERNAME | Identifiant administrateur par défaut |
| ADMIN_PASSWORD | Mot de passe administrateur par défaut |

Variables optionnelles :

| Variable | Description |
|----------|-------------|
| FLASK_ENV | Environnement (production par défaut) |
| USE_HTTPS | Cookies sécurisés (true par défaut) |

## Démarrage

**Développement :**
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

**Production :**
```bash
gunicorn --bind 0.0.0.0:5000 main:app
```

## Flux de données

### Recherche de pharmacies

1. L'utilisateur tape dans la barre de recherche
2. Le JavaScript déclenche une requête vers /api/pharmacies
3. Le service PharmacyService filtre les résultats
4. Les données sont retournées en JSON
5. Le JavaScript met à jour la liste et la carte

### Soumission d'une correction

1. L'utilisateur remplit le formulaire de correction
2. Le JavaScript envoie les données vers /api/pharmacy/{id}/submit-info
3. Une entrée InfoSubmission est créée en base (status=pending)
4. L'admin voit la soumission dans son tableau de bord
5. À l'approbation, la valeur de la pharmacie est mise à jour
6. Le status passe à approved

### Affichage d'une publicité

1. Le JavaScript charge les paramètres depuis /api/ads/settings
2. Selon le trigger_type, un timer ou compteur est initialisé
3. Quand les conditions sont remplies, /api/ads/random est appelé
4. Une pub pondérée par priorité est sélectionnée
5. Le popup s'affiche avec le délai skip_delay
6. La vue est comptabilisée via /api/ads/{id}/view
7. Si clic sur le bouton, /api/ads/{id}/click est appelé

### Indexation par moteurs de recherche

1. Un moteur de recherche accède à `/robots.txt`
2. Il découvre la référence au sitemap : `/sitemap.xml`
3. Il récupère le fichier sitemap XML qui liste toutes les pages publiques
4. Chaque page est indexée avec sa date de modification
5. Les pages `/admin*` sont explicitement bloquées par robots.txt
6. Les pages publiques sont crawlées et indexables

## Dépendances principales

**Backend :**
- Flask : Framework web
- Flask-SQLAlchemy : ORM
- Flask-Login : Authentification
- Flask-WTF : Protection CSRF
- Gunicorn : Serveur WSGI
- psycopg2-binary : Driver PostgreSQL
- email-validator : Validation d'emails

**Frontend :**
- Tailwind CSS : Styles (via CDN)
- Leaflet : Carte interactive
- Inter : Police de caractères
