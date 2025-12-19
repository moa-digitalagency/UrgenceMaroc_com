# Documentation de l'API

Cette API permet d'accéder aux données des pharmacies et des services d'urgence au Maroc. Toutes les réponses sont au format JSON.

## Accès

**URL de base :** `https://votre-domaine.com`

Les endpoints publics sont accessibles sans authentification. Les endpoints admin nécessitent une connexion préalable via `/admin/login`.

---

## Endpoints publics

### Liste des pharmacies

Récupère la liste des pharmacies avec possibilité de filtrer.

**Requête :** `GET /api/pharmacies`

**Paramètres (optionnels) :**

| Paramètre | Type | Description |
|-----------|------|-------------|
| search | string | Recherche dans le nom, quartier ou services |
| ville | string | Filtrer par ville |
| garde | string | "true" pour les pharmacies de garde uniquement |
| gare | string | "true" pour les pharmacies proches de la gare |

**Exemple :**
```
GET /api/pharmacies?ville=Casablanca&garde=true
```

**Réponse :**
```json
[
  {
    "id": 1,
    "code": "LBV001",
    "nom": "Grande Pharmacie des Forestiers",
    "ville": "Casablanca",
    "quartier": "Galerie de Mbolo",
    "telephone": "011 72 23 52",
    "bp": "2",
    "horaires": "Lun-Sam: 8h-19h30, Dim: 8h-18h",
    "services": "Parapharmacie, Conseil pharmaceutique",
    "proprietaire": "",
    "type_etablissement": "pharmacie_generale",
    "categorie_emplacement": "centre_commercial",
    "is_garde": false,
    "lat": 0.4162,
    "lng": 9.4673,
    "location_validated": false,
    "is_verified": false,
    "garde_end_date": null
  }
]
```

---

### Statistiques

Récupère les statistiques générales de la plateforme.

**Requête :** `GET /api/stats`

**Réponse :**
```json
{
  "total": 89,
  "pharmacies_garde": 15,
  "pharmacies_gare": 1,
  "locations_validated": 10,
  "par_ville": {
    "Casablanca": 70,
    "Fès": 8,
    "Marrakech": 2,
    "Rabat": 1
  }
}
```

---

### Popups actifs

Récupère les messages popup à afficher.

**Requête :** `GET /api/popups`

**Réponse :**
```json
[
  {
    "id": 1,
    "title": "Bienvenue sur UrgenceMaroc.com",
    "description": "Découvrez la première plateforme...",
    "warning_text": "Le projet est encore en construction...",
    "image_url": "/static/uploads/popups/abc123.jpg",
    "is_active": true,
    "show_once": true,
    "ordering": 0
  }
]
```

---

### Enregistrer une consultation

Comptabilise une vue sur une pharmacie (pour les statistiques).

**Requête :** `POST /api/pharmacy/<id>/view`

**Réponse :**
```json
{
  "success": true
}
```

---

### Soumettre une localisation GPS

Propose des coordonnées pour une pharmacie.

**Requête :** `POST /api/pharmacy/<id>/submit-location`

**En-têtes :**
```
Content-Type: application/json
```

**Corps de la requête :**
```json
{
  "latitude": 0.4162,
  "longitude": 9.4673,
  "name": "Jean Dupont",
  "phone": "+241 06 00 00 00",
  "comment": "Coordonnées exactes du bâtiment"
}
```

**Champs :**

| Champ | Obligatoire | Type | Description |
|-------|-------------|------|-------------|
| latitude | oui | float | Latitude GPS (-90 à 90) |
| longitude | oui | float | Longitude GPS (-180 à 180) |
| name | non | string | Nom du contributeur |
| phone | non | string | Téléphone du contributeur |
| comment | non | string | Commentaire libre |

**Réponse :**
```json
{
  "success": true,
  "message": "Localisation soumise avec succès"
}
```

---

### Soumettre une correction

Propose une modification d'information.

**Requête :** `POST /api/pharmacy/<id>/submit-info`

**Corps de la requête :**
```json
{
  "field_name": "telephone",
  "proposed_value": "011 72 00 00",
  "name": "Marie Martin",
  "phone": "+241 06 00 00 00",
  "comment": "Nouveau numéro depuis janvier 2024"
}
```

**Champs modifiables :** telephone, horaires, services, quartier, bp, proprietaire

**Réponse :**
```json
{
  "success": true,
  "message": "Information soumise avec succès"
}
```

---

### Envoyer une suggestion

Envoie un commentaire ou une idée.

**Requête :** `POST /api/suggestions`

**Corps de la requête :**
```json
{
  "category": "amelioration",
  "subject": "Ajout de fonctionnalité",
  "message": "Il serait utile d'avoir une fonction de recherche par médicament...",
  "name": "Pierre Obame",
  "email": "pierre@exemple.com",
  "phone": "+241 06 00 00 00"
}
```

**Champs :**

| Champ | Obligatoire | Type | Description |
|-------|-------------|------|-------------|
| category | oui | string | Catégorie (suggestion, erreur, pharmacie, autre) |
| subject | oui | string | Sujet |
| message | oui | string | Contenu du message |
| name | non | string | Nom du contributeur |
| email | non | string | Email du contributeur |
| phone | non | string | Téléphone du contributeur |

**Réponse :**
```json
{
  "success": true,
  "message": "Suggestion envoyée avec succès"
}
```

---

### Proposer une pharmacie

Suggère l'ajout d'une nouvelle pharmacie.

**Requête :** `POST /api/pharmacy-proposal`

**Corps de la requête :**
```json
{
  "nom": "Pharmacie du Soleil",
  "ville": "Casablanca",
  "quartier": "Akebe",
  "telephone": "011 72 00 00",
  "bp": "1234",
  "horaires": "8h-20h",
  "services": "Service courant",
  "proprietaire": "Dr. Nzamba",
  "type_etablissement": "pharmacie_generale",
  "categorie_emplacement": "zone_residentielle",
  "is_garde": false,
  "latitude": 0.4200,
  "longitude": 9.4700,
  "name": "Jean Obiang",
  "email": "jean@exemple.com",
  "phone": "+241 06 00 00 00",
  "comment": "Pharmacie ouverte récemment"
}
```

**Champs obligatoires :** nom, ville

**Types d'établissement :** pharmacie_generale, depot_pharmaceutique, pharmacie_hospitaliere

**Catégories d'emplacement :** standard, gare, hopital, aeroport, centre_commercial, marche, centre_ville, zone_residentielle

**Réponse :**
```json
{
  "success": true,
  "message": "Proposition de pharmacie envoyée avec succès"
}
```

---

## Endpoints SEO et Crawling

### Sitemap XML

Récupère le fichier sitemap pour les moteurs de recherche.

**Requête :** `GET /sitemap.xml`

**Contenu :** Fichier XML conforme au standard sitemaps.org

**Caractéristiques :**
- Généré dynamiquement à chaque requête
- Inclut la page d'accueil avec priorité 1.0
- Inclut toutes les pharmacies actives avec priorité 0.8
- Exclut automatiquement toutes les pages admin
- Dates de modification basées sur created_at/updated_at

**Exemple :**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://votre-domaine.com/</loc>
    <lastmod>2025-12-19T14:15:00.000000</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://votre-domaine.com/#pharmacy-1</loc>
    <lastmod>2025-12-19T10:30:00.000000</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

---

### Robots.txt

Fichier de configuration pour les moteurs de recherche.

**Requête :** `GET /robots.txt`

**Contenu :** Fichier texte conforme à robots.txt standard

**Règles :**
- Tous les robots : `User-agent: *`
- Pages autorisées : `Allow: /` (toutes les pages publiques)
- Pages bloquées : `Disallow: /admin/` et `Disallow: /admin`
- Référence sitemap : `Sitemap: https://votre-domaine.com/sitemap.xml`

**Exemple :**
```
# UrgenceMaroc.com - Robots.txt Configuration
# Generated dynamically to manage search engine crawling

User-agent: *
Allow: /

# Disallow all admin pages and their subpages
# This includes: /admin/auth, /admin/dashboard, /admin/pharmacy,
# /admin/submissions, /admin/emergency, /admin/settings, /admin/ads, /admin/logs
Disallow: /admin/
Disallow: /admin

# Reference to the sitemap containing all public pages
Sitemap: https://votre-domaine.com/sitemap.xml
```

---

## Endpoints publicitaires

### Configuration des publicités

Récupère les paramètres globaux des pubs.

**Requête :** `GET /api/ads/settings`

**Réponse :**
```json
{
  "ads_enabled": true,
  "trigger_type": "time",
  "time_delay": 60,
  "time_repeat": true,
  "time_interval": 300,
  "page_count": 3,
  "refresh_show": false,
  "refresh_count": 1,
  "default_skip_delay": 5,
  "max_ads_per_session": 10,
  "cooldown_after_skip": 60,
  "cooldown_after_click": 300,
  "show_on_mobile": true,
  "show_on_desktop": true
}
```

---

### Obtenir une publicité

Récupère une publicité aléatoire (pondérée par priorité).

**Requête :** `GET /api/ads/random`

**Réponse (si disponible) :**
```json
{
  "id": 1,
  "title": "Offre spéciale",
  "description": "Visitez notre partenaire...",
  "media_type": "image",
  "image_url": "/static/uploads/ads/abc123.jpg",
  "video_url": "",
  "cta_text": "En savoir plus",
  "cta_url": "https://exemple.com/offre",
  "skip_delay": 5,
  "is_active": true,
  "priority": 10
}
```

**Réponse (si aucune pub disponible) :**
```json
null
```

---

### Enregistrer une vue de pub

**Requête :** `POST /api/ads/<id>/view`

**Réponse :**
```json
{
  "success": true
}
```

---

### Enregistrer un clic de pub

**Requête :** `POST /api/ads/<id>/click`

**Réponse :**
```json
{
  "success": true
}
```

---

## Endpoints admin

Tous ces endpoints nécessitent une authentification préalable via session.

### Authentification

**Connexion :** `POST /admin/login`

| Champ | Type | Description |
|-------|------|-------------|
| username | string | Nom d'utilisateur |
| password | string | Mot de passe |

**Déconnexion :** `GET /admin/logout`

---

### Pharmacies

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | /admin/ | Tableau de bord |
| GET/POST | /admin/pharmacy/add | Ajouter |
| GET/POST | /admin/pharmacy/<id>/edit | Modifier |
| POST | /admin/pharmacy/<id>/delete | Supprimer |
| POST | /admin/pharmacy/<id>/toggle-garde | Activer/désactiver garde |
| POST | /admin/pharmacy/<id>/set-garde | Définir garde avec dates |
| POST | /admin/pharmacy/<id>/toggle-verified | Activer/désactiver vérifié |
| POST | /admin/pharmacy/<id>/validate-location | Valider GPS |
| POST | /admin/pharmacy/<id>/invalidate-location | Invalider GPS |
| POST | /admin/pharmacy/<id>/update-coordinates | Mettre à jour GPS |

---

### Soumissions

| Méthode | URL | Description |
|---------|-----|-------------|
| POST | /admin/location-submission/<id>/approve | Approuver localisation |
| POST | /admin/location-submission/<id>/reject | Refuser localisation |
| POST | /admin/info-submission/<id>/approve | Approuver correction |
| POST | /admin/info-submission/<id>/reject | Refuser correction |
| POST | /admin/suggestion/<id>/respond | Répondre à suggestion |
| POST | /admin/suggestion/<id>/archive | Archiver suggestion |
| POST | /admin/pharmacy-proposal/<id>/approve | Approuver proposition |
| POST | /admin/pharmacy-proposal/<id>/reject | Refuser proposition |

---

### Contacts d'urgence

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | /admin/emergency-contacts | Liste |
| GET/POST | /admin/emergency-contact/add | Ajouter |
| GET/POST | /admin/emergency-contact/<id>/edit | Modifier |
| POST | /admin/emergency-contact/<id>/delete | Supprimer |

---

### Paramètres et popups

| Méthode | URL | Description |
|---------|-----|-------------|
| GET/POST | /admin/settings | Paramètres du site |
| GET | /admin/popups | Liste des popups |
| GET/POST | /admin/popup/add | Ajouter popup |
| GET/POST | /admin/popup/<id>/edit | Modifier popup |
| POST | /admin/popup/<id>/delete | Supprimer popup |
| POST | /admin/popup/<id>/toggle | Activer/désactiver popup |

---

### Publicités

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | /admin/ads | Liste des pubs |
| GET/POST | /admin/ad/add | Ajouter pub |
| GET/POST | /admin/ad/<id>/edit | Modifier pub |
| POST | /admin/ad/<id>/delete | Supprimer pub |
| POST | /admin/ad/<id>/toggle | Activer/désactiver pub |
| GET/POST | /admin/ads/settings | Configuration globale |

---

### Journal d'activité

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | /admin/logs | Liste des logs |

---

## Gestion des erreurs

Toutes les erreurs suivent ce format :

```json
{
  "success": false,
  "error": "Description de l'erreur"
}
```

**Codes HTTP utilisés :**

| Code | Description |
|------|-------------|
| 200 | Succès |
| 400 | Paramètres manquants ou invalides |
| 401 | Authentification requise |
| 404 | Ressource introuvable |
| 500 | Erreur serveur |

**Exemples d'erreurs :**

```json
{
  "success": false,
  "error": "Coordonnées manquantes"
}
```

```json
{
  "success": false,
  "error": "Invalid JSON data"
}
```

```json
{
  "success": false,
  "error": "Ressource non trouvée"
}
```

---

## Notes d'implémentation

### Protection CSRF

Les endpoints POST publics sont exemptés de la protection CSRF pour permettre les appels depuis le frontend JavaScript.

Les endpoints admin sont protégés par CSRF via Flask-WTF.

### Validation des données

- Les coordonnées GPS sont validées (conversion en float)
- Les champs requis retournent une erreur 400 si absents
- Les données JSON invalides retournent une erreur 400

### Pagination

Les endpoints de liste ne sont pas paginés actuellement. Pour de grands volumes de données, une pagination pourrait être ajoutée ultérieurement.

### Caching

Aucun cache n'est implémenté côté API. Les données sont toujours fraîches depuis la base de données.
