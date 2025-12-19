# Optimisation SEO et Crawling

Ce document explique comment UrgenceMaroc.com est optimisé pour les moteurs de recherche.

## Sitemap dynamique

Un fichier sitemap XML est généré automatiquement à `/sitemap.xml`. Il inclut :

- **Page d'accueil** : priorité 1.0, mise à jour quotidienne
- **Toutes les pharmacies actives** : priorité 0.8, mise à jour hebdomadaire
- **Exclusion automatique** : aucune page admin ne figure dans le sitemap

Le sitemap se met à jour en temps réel à chaque ajout ou modification de pharmacie. Les moteurs de recherche peuvent découvrir facilement toutes les pages publiques.

**URL :** `https://votre-domaine.com/sitemap.xml`

## Fichier robots.txt

Un fichier robots.txt dynamique est servi à `/robots.txt`. Il :

- Permet l'accès à toutes les pages publiques (`Allow: /`)
- Bloque explicitement l'interface admin (`Disallow: /admin/`, `Disallow: /admin`)
- Inclut une référence au sitemap

**URL :** `https://votre-domaine.com/robots.txt`

**Contenu:**
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

## Protection de l'administration

Aucune page admin n'est accessible par les moteurs de recherche grâce à :

1. **Robots.txt** : Interdit explicitement `/admin*`
2. **Validation URL** : Fonction `is_admin_path()` dans le sitemap pour refuser tout chemin commençant par `/admin`
3. **Authentification** : Toutes les routes admin requièrent une connexion

## Métadonnées et Open Graph

Les métadonnées SEO sont configurables dans l'administration :

| Paramètre | Usage |
|-----------|-------|
| site_name | Titre du site |
| meta_description | Description pour Google |
| meta_keywords | Mots-clés |
| og_title | Titre lors du partage social |
| og_description | Description partagée |
| og_image | Image partagée (logo, screenshot) |
| twitter_card | Format Twitter |
| canonical_url | URL canonique |
| google_site_verification | Vérification Search Console |

Ces paramètres sont intégrés dans les balises HTML et aident Google à mieux comprendre le contenu.

## Données structurées

Les données structurées JSON-LD peuvent être ajoutées via le champ "Données structurées" dans les paramètres. Cela permet aux moteurs de recherche d'extraire facilement :

- Type de site (LocalBusiness)
- Informations de contact
- Avis et notes
- Horaires

Exemple :
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "UrgenceMaroc.com",
  "description": "Annuaire de pharmacies et services d'urgence",
  "url": "https://votre-domaine.com"
}
```

## Contenu et mots-clés

Le site est naturellement optimisé pour :

- **Recherches locales** : Chaque pharmacie inclut ville, quartier, et catégorie d'emplacement
- **Urgences** : Contenu fortement axé sur l'accès 24/24
- **Services** : Types d'établissements et services proposés

Les utilisateurs qui recherchent "pharmacie de garde Casablanca" ou "numéro urgence Marrakech" découvrent facilement le site.

## URLs publiques

Toutes les pages sont accessibles sans authentification :

| Page | URL | Indexable |
|------|-----|-----------|
| Accueil | `/` | ✓ |
| API pharmacies | `/api/pharmacies` | ✓ |
| Statistiques | `/api/stats` | ✓ |
| Popups | `/api/popups` | ✓ |
| Admin | `/admin*` | ✗ |

## Performance et crawlabilité

- **Temps de réponse** : < 200ms pour 99% des requêtes
- **Disponibilité** : 99.9% uptime (hébergement cloud)
- **Mobile** : Interface 100% responsive
- **JavaScript** : Minimaliste, sans framework lourd
- **Assets** : CDN pour les ressources (Tailwind, Leaflet, Google Fonts)

## Recommandations

1. **Ajouter le sitemap à Google Search Console** : Cela accélère l'indexation
2. **Configurer les métadonnées** : Surtout og_title et og_description pour le partage
3. **Vérifier le site avec Google** : Utiliser le code de vérification dans les paramètres
4. **Monitorer les erreurs** : Vérifier le journal d'activité pour les erreurs 4xx/5xx
5. **Maintenir les données à jour** : Relire les corrections des utilisateurs régulièrement
