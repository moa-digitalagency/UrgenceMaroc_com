# Guide d'administration

Ce guide explique comment utiliser le panneau d'administration pour gérer le site UrgenceMaroc.com.

## Connexion

1. Allez sur `/admin`
2. Entrez votre identifiant et mot de passe
3. Cliquez sur "Connexion"

Les identifiants par défaut sont définis dans les variables d'environnement ADMIN_USERNAME et ADMIN_PASSWORD. Un compte administrateur est créé automatiquement au premier démarrage.

## Tableau de bord

La page d'accueil affiche :

**Statistiques principales**
- Nombre total de pharmacies
- Pharmacies de garde actives
- Soumissions en attente (localisations, corrections, suggestions, propositions)

**Graphiques**
- Fréquentation sur 7 jours et 30 jours
- Répartition des pharmacies par ville
- Répartition par type d'établissement
- Vues aujourd'hui, cette semaine, ce mois

**Listes**
- Pharmacies les plus consultées (top 10)
- Pharmacies récemment modifiées

## Gestion des pharmacies

### Ajouter une pharmacie

1. Cliquez sur "Ajouter une pharmacie"
2. Remplissez les champs obligatoires :
   - Code (identifiant court unique, ex: LBV001)
   - Nom
   - Ville
3. Complétez les champs optionnels :
   - Quartier/adresse
   - Téléphone
   - Boîte postale
   - Horaires
   - Services proposés
   - Propriétaire
   - Type d'établissement
   - Catégorie d'emplacement
4. Ajoutez les coordonnées GPS (optionnel)
5. Cochez les options :
   - "De garde" si actuellement en service de garde
   - "Vérifié" si les informations ont été contrôlées
   - "GPS validé" si la position est confirmée
6. Cliquez sur "Enregistrer"

### Modifier une pharmacie

1. Trouvez la pharmacie dans la liste du tableau de bord
2. Cliquez sur l'icône crayon (modifier)
3. Modifiez les champs souhaités
4. Enregistrez

### Supprimer une pharmacie

1. Cliquez sur l'icône poubelle
2. Confirmez la suppression

Attention : cette action est irréversible. Toutes les soumissions liées seront perdues.

### Gérer les gardes

**Activation rapide :** 
Cliquez directement sur le badge "garde" pour activer ou désactiver instantanément le statut.

**Avec période programmée :**
1. Cliquez sur "Gérer la garde"
2. Sélectionnez la date de début
3. Le système programme automatiquement une durée de 7 jours
4. Confirmez

La garde expire automatiquement à la date de fin. Le statut is_currently_garde tient compte de cette date.

### Valider une position GPS

Après qu'un utilisateur a soumis des coordonnées :
1. Comparez la position proposée avec la position actuelle sur la carte
2. Approuvez pour mettre à jour les coordonnées
3. La pharmacie est marquée "GPS validé"

Vous pouvez aussi mettre à jour manuellement les coordonnées depuis le formulaire de modification.

## Soumissions des utilisateurs

Les visiteurs peuvent soumettre des corrections. Chaque soumission apparaît dans le tableau de bord avec un statut "pending".

### Localisations GPS

Un utilisateur propose des coordonnées pour une pharmacie.

1. Allez dans la section "Localisations en attente"
2. Comparez sur la carte la position actuelle (si existante) et celle proposée
3. Si correct : cliquez sur "Approuver"
   - Les coordonnées sont mises à jour automatiquement
   - La pharmacie est marquée "GPS validé"
4. Si incorrect : cliquez sur "Rejeter"

### Corrections d'informations

Un utilisateur signale qu'un numéro de téléphone ou un horaire est erroné.

1. Allez dans la section "Corrections en attente"
2. Comparez la valeur actuelle et la valeur proposée
3. Vérifiez l'information si possible
4. Approuvez pour appliquer la modification
5. Ou rejetez si incorrect

Champs modifiables par les utilisateurs : téléphone, horaires, services, quartier, boîte postale, propriétaire.

### Suggestions

Un utilisateur envoie une idée ou un commentaire.

1. Lisez le message
2. Répondez si vous le souhaitez (le champ réponse admin est visible)
3. Archivez une fois traité

Catégories possibles : suggestion d'amélioration, signalement d'erreur, autre.

### Propositions de pharmacies

Un utilisateur propose d'ajouter une pharmacie non référencée.

1. Vérifiez que la pharmacie n'existe pas déjà (recherche par nom ou adresse)
2. Contrôlez les informations fournies
3. Si valide : approuvez
   - La pharmacie est créée automatiquement avec un code généré (NEW + 6 caractères)
   - Elle apparaît dans la liste avec le statut "non vérifié"
4. Sinon : rejetez

Après approbation, vous pouvez modifier la pharmacie pour compléter les informations manquantes.

## Contacts d'urgence

### Consulter la liste

Menu "Contacts d'urgence" : affiche tous les numéros triés par ordre d'affichage. Les services nationaux apparaissent en premier.

### Ajouter un contact

1. Cliquez sur "Ajouter un contact"
2. Choisissez le type de service :
   - Police
   - Pompiers
   - Ambulance / SAMU
   - Hôpital
   - Clinique
   - SOS Médecins
   - Protection Civile
   - Autre
3. Renseignez le libellé (ex: "Hôpital Régional de Marrakech")
4. Entrez le(s) numéro(s) de téléphone (séparés par / si plusieurs)
5. Ajoutez l'adresse (optionnel)
6. Ajoutez des notes (optionnel)
7. Indiquez si c'est un service national ou local (avec ville)
8. Définissez l'ordre d'affichage (1 = premier)
9. Cochez "Actif" pour l'afficher
10. Enregistrez

### Modifier ou supprimer

Utilisez les icônes crayon (modifier) ou poubelle (supprimer) sur chaque ligne.

## Paramètres du site

### Informations générales

- Nom du site (affiché dans le titre et l'en-tête)
- Description meta (pour le référencement)
- Mots-clés meta
- Auteur

### Apparence

Uploadez vos fichiers :

- **Logo** : affiché dans l'en-tête (formats acceptés : PNG, JPG, SVG, WebP)
- **Favicon** : icône du navigateur (formats acceptés : ICO, PNG, SVG)
- **Image de partage** : affichée quand le lien est partagé sur les réseaux sociaux

Pour supprimer un fichier : cochez la case "Supprimer" correspondante puis enregistrez.

### Référencement (SEO)

- Titre Open Graph (titre affiché sur les réseaux sociaux)
- Description Open Graph
- Type Open Graph (website par défaut)
- Locale (fr_FR par défaut)
- URL canonique
- Vérification Google (code de vérification Search Console)
- Données structurées (JSON-LD)

### Réseaux sociaux

- Twitter Card (type de carte : summary_large_image recommandé)
- Handle Twitter (@votrecompte)
- Titre et description Twitter

### Code personnalisé

- Code en-tête : scripts ou styles à insérer dans <head>
- Code pied de page : scripts à insérer avant </body>

Utile pour Google Analytics, Facebook Pixel, ou tout autre outil de tracking.

## Popups

Les popups sont des messages affichés aux visiteurs à leur arrivée sur le site.

### Créer un popup

1. Menu "Popups" puis "Nouveau popup"
2. Renseignez :
   - **Titre** : accroche principale
   - **Description** : texte détaillé
   - **Avertissement** (optionnel) : apparaît dans un encadré jaune
   - **Image** (optionnel) : uploadez un visuel
3. Options :
   - **Actif** : afficher ou non le popup
   - **Afficher une seule fois** : le visiteur ne le verra qu'une fois (cookie)
   - **Ordre** : si plusieurs popups, lequel s'affiche en premier
4. Enregistrez

### Gérer les popups

- Cliquez sur le badge pour activer/désactiver rapidement
- Modifiez ou supprimez avec les icônes crayon/poubelle

Les popups sont affichés dans l'ordre défini. Un visiteur qui ferme un popup ne le reverra pas si "Afficher une seule fois" est coché.

## Publicités

### Créer une publicité

1. Menu "Publicités" puis "Ajouter"
2. Contenu :
   - **Titre** : nom de la campagne
   - **Description** : texte accompagnant la pub
   - **Type de média** : image ou vidéo
   - Pour une image : uploadez le fichier
   - Pour une vidéo : collez l'URL (YouTube, Facebook, etc.)
3. Appel à l'action :
   - **Texte du bouton** : "En savoir plus", "Profiter", etc.
   - **URL de destination** : lien vers votre site ou page
4. Options :
   - **Délai avant "Passer"** : secondes avant que l'utilisateur puisse fermer (0 = utiliser valeur par défaut)
   - **Priorité** : plus le chiffre est élevé, plus la pub est affichée souvent
   - **Dates de début et fin** : planification de la campagne
   - **Actif** : afficher ou non
5. Enregistrez

### Statistiques

Chaque publicité affiche :
- Nombre de vues
- Nombre de clics
- Taux de clic (clics / vues × 100)

Ces données permettent d'évaluer l'efficacité des campagnes.

### Configuration globale

Menu "Réglages pubs" :

**Activation**
- Activer/désactiver toutes les pubs d'un coup

**Déclencheur** (quand afficher la pub)
- **Temps** : après X secondes sur le site
- **Nombre de pages** : après X pages visitées
- **Rechargement** : quand la page est rafraîchie X fois

**Répétition**
- Répéter après la première pub : oui/non
- Intervalle entre les répétitions (secondes)

**Limites**
- Maximum par session : combien de pubs au total par visite
- Pause après "Passer" : secondes avant la prochaine pub
- Pause après clic : secondes avant la prochaine pub après un clic

**Affichage par appareil**
- Sur mobile : oui/non
- Sur desktop : oui/non

## Journal d'activité

Le journal enregistre les actions importantes :

- Erreurs serveur (codes 4xx et 5xx)
- Actions admin (connexion, modifications)
- Soumissions utilisateurs

Chaque entrée contient :
- Date et heure
- Adresse IP
- Navigateur
- Méthode HTTP et chemin
- Code de réponse
- Temps de traitement
- Admin connecté (si applicable)

Niveaux de log :
- **Success** (vert) : action réussie
- **Info** (bleu) : information
- **Warning** (jaune) : avertissement
- **Error** (rouge) : erreur

## Bonnes pratiques

### Qualité des données

- Vérifiez toujours les informations avant d'approuver une soumission
- Complétez un maximum de champs lors de l'ajout d'une pharmacie
- Validez les coordonnées GPS sur la carte
- Marquez "vérifié" uniquement après contrôle

### Gestion des gardes

- Planifiez les gardes en début de semaine si possible
- Assurez une couverture géographique équilibrée
- Le système désactive automatiquement les gardes expirées
- Vérifiez régulièrement les pharmacies de garde affichées

### Relations avec les utilisateurs

- Répondez aux suggestions (même brièvement)
- Traitez rapidement les corrections valides
- Utilisez les popups pour les annonces importantes
- Ne rejetez pas sans raison (les utilisateurs font l'effort de contribuer)

### Sécurité

- Utilisez un mot de passe fort (min. 12 caractères, lettres, chiffres, symboles)
- Déconnectez-vous après chaque session
- Ne partagez pas vos identifiants
- Vérifiez régulièrement le journal d'activité

## Problèmes courants

**Je ne peux pas me connecter**
- Vérifiez les variables ADMIN_USERNAME et ADMIN_PASSWORD
- Effacez les cookies du navigateur
- Assurez-vous que le serveur est démarré

**La carte ne s'affiche pas**
- Vérifiez votre connexion internet
- Rechargez la page
- Désactivez les bloqueurs de publicité (ils peuvent bloquer Leaflet)

**L'upload d'image échoue**
- Formats acceptés : PNG, JPG, JPEG, GIF, WEBP, SVG, ICO
- Taille maximale recommandée : 5 Mo
- Vérifiez les droits du dossier uploads

**Mes modifications n'apparaissent pas**
- Videz le cache du navigateur
- Rechargez la page avec Ctrl+F5
- Vérifiez que vous avez bien cliqué sur "Enregistrer"

**Les pubs ne s'affichent pas**
- Vérifiez que "Activer les publicités" est coché dans les réglages
- Vérifiez qu'au moins une pub est active
- Contrôlez les dates de diffusion
- Vérifiez le déclencheur configuré (temps, pages, rechargement)

**Les coordonnées GPS sont incorrectes**
- Cliquez sur la carte pour repositionner le marqueur
- Vérifiez le format (latitude entre -90 et 90, longitude entre -180 et 180)
- Utilisez un outil externe pour obtenir les coordonnées exactes

**Une pharmacie n'apparaît pas dans les résultats**
- Vérifiez qu'elle est bien enregistrée (visible dans le tableau de bord)
- Vérifiez les filtres actifs (ville, garde)
- Rechargez la page

## Support

Pour toute question technique ou assistance :

**MOA Digital Agency LLC**
- Email : moa@myoneart.com
- Site : www.myoneart.com
