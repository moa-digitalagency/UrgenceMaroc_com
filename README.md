# UrgenceMaroc.com

Vous cherchez une pharmacie ouverte à 2h du matin ? Un numéro d'urgence dans une ville que vous ne connaissez pas ? C'est exactement pour ça que ce projet existe.

UrgenceMaroc.com rassemble toutes les pharmacies du Maroc sur une seule plateforme. On y trouve les horaires, les numéros de téléphone, les pharmacies de garde, et même une carte pour s'y rendre directement.

## Ce que fait l'application

**Pour les visiteurs :**
- Chercher une pharmacie par nom, quartier ou ville
- Voir d'un coup d'oeil quelles pharmacies sont ouvertes 24h/24
- Appeler directement en cliquant sur un numéro
- Trouver son chemin grâce à la carte interactive
- Accéder aux numéros d'urgence (police, pompiers, hôpitaux)
- Proposer des corrections ou ajouter des pharmacies manquantes

**Pour les administrateurs :**
- Gérer l'annuaire complet des pharmacies
- Activer le mode "garde" pour les pharmacies de service
- Valider les contributions des utilisateurs
- Configurer les contacts d'urgence par ville
- Personnaliser l'apparence du site (logo, couleurs, messages)
- Gérer un système publicitaire non intrusif

## Comment ça marche

L'application tourne sur Flask (Python) avec une base PostgreSQL. Le frontend utilise Tailwind CSS pour le design et Leaflet pour la cartographie.

**Technologies principales :**
- Python 3.11 + Flask
- PostgreSQL + SQLAlchemy
- Tailwind CSS
- Leaflet.js + OpenStreetMap

## Installation

**Ce dont vous avez besoin :**
- Python 3.11 ou plus récent
- PostgreSQL
- pip

**Étapes :**

1. Récupérez le code :
```bash
git clone <url-du-repo>
cd urgence-maroc
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurez les variables d'environnement :
```bash
export DATABASE_URL="postgresql://votre_utilisateur:votre_mdp@votre_hote/votre_base"
export SESSION_SECRET="une-cle-secrete-bien-longue"
export ADMIN_USERNAME="admin"
export ADMIN_PASSWORD="un-mot-de-passe-solide"
```

4. Chargez les données de démonstration :
```bash
python init_demo.py
```

Pour tout effacer et recharger :
```bash
python init_demo.py --force
```

5. Lancez l'application :
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## Organisation du code

```
urgence-gabon/
├── app.py                 # Configuration Flask
├── main.py                # Point d'entrée
├── extensions.py          # Extensions (base de données, etc.)
├── init_demo.py           # Chargement des données de démo
│
├── models/                # Modèles de données
│   ├── pharmacy.py        # Pharmacies
│   ├── admin.py           # Administrateurs
│   ├── emergency_contact.py
│   ├── site_settings.py
│   └── ...
│
├── routes/                # Points d'accès
│   ├── public.py          # Pages et API publiques
│   └── admin/             # Administration
│
├── templates/             # Pages HTML
├── static/                # CSS, JS, images
└── docs/                  # Documentation
```

## Données incluses

Le script de démonstration charge :
- 89 pharmacies dans 9 villes gabonaises
- 18 contacts d'urgence (nationaux et locaux)
- Un message de bienvenue

**Villes couvertes :** Libreville, Port-Gentil, Franceville, Oyem, Mouila, Moanda, Makokou, Koulamoutou, Ntom

## Administration

Accès : `/admin` avec les identifiants configurés dans les variables d'environnement.

L'interface permet de :
- Voir les statistiques de fréquentation
- Gérer les pharmacies (ajouter, modifier, supprimer)
- Activer les gardes avec dates de début et fin
- Traiter les soumissions des utilisateurs
- Configurer les paramètres du site

## Documentation

- [Présentation commerciale](docs/COMMERCIAL.md) - Pour comprendre la valeur du projet
- [Guide utilisateur commercial](docs/USER_COMMERCIAL.md) - Fonctionnalités détaillées
- [Documentation API](docs/API.md) - Référence technique
- [Architecture](docs/ARCHITECTURE.md) - Structure du code
- [Guide administrateur](docs/ADMIN_GUIDE.md) - Utilisation du panneau admin

## Contribuer

Vous pouvez aider directement depuis l'application :
- Signaler une erreur dans les informations
- Proposer les coordonnées GPS d'une pharmacie
- Suggérer une nouvelle pharmacie
- Envoyer des idées d'amélioration

## Licence

MIT
