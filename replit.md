# UrgenceMaroc.com - Notes techniques

Ce fichier contient les informations utiles pour travailler sur le projet.

## Description rapide

Une application web pour trouver des pharmacies au Maroc. Elle affiche 89 pharmacies réparties dans 9 villes, avec indication des pharmacies de garde (ouvertes 24h/24). Interface responsive pensée pour mobile avec onglets de navigation.

## Préférences de développement

- Communication en français, langage simple
- Code commenté quand nécessaire
- Tests manuels avant de valider

## Historique des modifications

**Décembre 2025 (Session 2 - FINAL: Security + Endpoints + Database)**

Audit complet et corrections :
- ✅ **Sécurité:** 6 headers de sécurité ajoutés + Rate Limiting (Flask-Limiter)
- ✅ **Endpoints:** 25+ endpoints testés et vérifiés (GET, POST, error handling)
- ✅ **Base de données:** Vérification d'intégrité + script de migration SÛRE
  - Toutes les 13 tables présentes et intactes
  - Script migrate_db.py pour migrations sans perte de données
  - Pas de suppression de données - Seulement création/ajout
- ✅ **Documentation:** 9 fichiers incluant DATABASE_INTEGRITY.md, SECURITY_AUDIT.md, ENDPOINT_VERIFICATION.md

**Décembre 2025 (Session 2 - ENDPOINTS & ENDPOINTS COMPLETE)**

Revue et vérification exhaustive :
- ✅ Test complet de 25+ endpoints (GET, POST, error handling)
- ✅ Tous les endpoints testés retournent les bons codes HTTP
- ✅ Aucun erreur 500 non documentée, aucun JSON mal formé
- ✅ Correction du endpoint manquant `/api/emergency-contacts`
  - Ajout de la route GET `/api/emergency-contacts` dans routes/public.py
  - Retourne JSON valide avec structure {national: [], by_city: {}}
- ✅ Création de docs/ENDPOINT_VERIFICATION.md (vérification complète)
- ✅ Création de docs/FINAL_REVIEW.md (revue détaillée)
- ✅ Documentation exhaustive: 7 fichiers documentant tous les aspects

**Décembre 2025 (Session 2 - Initial)**

Ajout de fonctionnalités SEO :
- Endpoint `/sitemap.xml` : génère dynamiquement un sitemap XML avec toutes les pharmacies actives
- Endpoint `/robots.txt` : génère dynamiquement un fichier robots.txt qui bloque `/admin` et référence le sitemap
- Fonction `is_admin_path()` : valide que aucune page admin ne figure dans le sitemap ou robots.txt
- Documentation complète dans docs/SEO.md

**Décembre 2025 (Session 1)**

Ajout du système de logs d'activité :
- Nouveau modèle ActivityLog pour tracer toutes les activités (erreurs, authentification)
- Page admin `/admin/logs` avec filtres par type, niveau, IP, chemin
- Logging automatique des erreurs 400+ et événements d'authentification
- Possibilité de nettoyer les anciens logs

Refactoring du code pour une meilleure maintenabilité :
- Le fichier JS principal (1600+ lignes) a été découpé en 7 modules
- Les routes admin (970+ lignes) sont maintenant dans 8 fichiers séparés
- Ajout de gestion d'erreurs sur tous les appels asynchrones
- Protection XSS avec fonction `escapeHtml`

Fonctionnalités précédentes :
- Système publicitaire configurable (images ou vidéos, plusieurs déclencheurs, limites par session)
- Statistiques avec graphiques Chart.js (vues, répartition par ville et type)
- Upload de fichiers pour logo, favicon et images (plus d'URLs externes)
- Correction du bug de duplication admin
- Fuseau horaire configurable
- Popups personnalisables avec images
- Numéros de téléphone cliquables
- Catégorisation des pharmacies (gare, hôpital, aéroport, etc.)
- Système de vérification GPS
- Design mobile-first

## Architecture

**Frontend :**
- Templates Jinja2
- Tailwind CSS (CDN)
- Leaflet.js pour les cartes
- JavaScript modulaire :
  - `config.js` : constantes et configuration
  - `map.js` : gestion de la carte
  - `pharmacy.js` : affichage des pharmacies
  - `forms.js` : formulaires de soumission
  - `popups.js` : fenêtres modales
  - `ads.js` : système publicitaire
  - `app.js` : orchestrateur principal

**Backend :**
- Flask avec Flask-Login
- PostgreSQL via SQLAlchemy
- Authentification par session
- Routes en blueprints :
  - `routes/public.py` : accès public
  - `routes/admin/` : administration (auth, dashboard, pharmacy, submissions, emergency, settings, ads, logs)

## Modèles de données

**Admin** : id, username, password_hash

**Pharmacy** : id, code, nom, ville, quartier, telephone, bp, horaires, services, proprietaire, type_etablissement, categorie_emplacement, is_garde, is_verified, latitude, longitude, location_validated

**EmergencyContact** : ville, service_type, label, phone_numbers, address, notes, is_national, ordering

**Submission types** : LocationSubmission, InfoSubmission, PharmacyProposal, Suggestion

**Advertisement** : title, description, media_type, image/video, cta_text, cta_url, skip_delay, priority, dates, view/click counts

**ActivityLog** : timestamp, ip_address, user_agent, method, path, status_code, response_time_ms, log_type, log_level, message, details, admin_id

## Dépendances externes

CDN :
- Tailwind CSS
- Leaflet.js 1.9.4
- Google Fonts (Inter)
- Chart.js

Python :
- Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF
- psycopg2-binary
- gunicorn
- werkzeug

## Points d'accès API

**Public :**
- `GET /` : page principale
- `GET /sitemap.xml` : sitemap dynamique (SEO)
- `GET /robots.txt` : fichier robots (SEO, crawling)
- `GET /api/pharmacies` : liste (filtres: search, ville, garde)
- `GET /api/stats` : statistiques
- `GET /api/popups` : popups actifs
- `GET /api/emergency-contacts` : contacts d'urgence
- `POST /api/pharmacy/<id>/view` : enregistrer une vue
- `POST /api/pharmacy/<id>/submit-location` : soumettre GPS
- `POST /api/pharmacy/<id>/submit-info` : soumettre correction
- `POST /api/suggestions` : envoyer suggestion
- `POST /api/pharmacy-proposal` : proposer pharmacie

**Admin (authentification requise) :**
- `/admin/login`, `/admin/logout`
- `/admin` : tableau de bord
- `/admin/pharmacy/add`, `/admin/pharmacy/<id>/edit`, `/admin/pharmacy/<id>/delete`
- `/admin/pharmacy/<id>/toggle-garde`
- Gestion des soumissions, contacts d'urgence, paramètres, publicités

## Scripts d'initialisation

`init_db.py` : crée les tables de la base

`init_demo.py` : charge les données de démonstration (pharmacies, contacts, popup)

```bash
python init_demo.py        # charge les données
python init_demo.py --force  # efface et recharge
```

## Variables d'environnement

Obligatoires :
- `DATABASE_URL` : connexion PostgreSQL
- `SESSION_SECRET` : clé de session Flask
- `ADMIN_USERNAME` : identifiant admin
- `ADMIN_PASSWORD` : mot de passe admin

Automatiques (Replit) :
- `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`
