# Intégrité et Migration de Base de Données

**Date:** 19 Décembre 2025  
**Status:** ✅ Système de migration SÉCURISÉ

## Vue d'ensemble

La base de données UrgenceMaroc.com est conçue pour être sûre et évolutive. Les scripts de migration ne suppriment jamais les données existantes.

## Structure des tables

### Modèles de données (13 tables)

1. **pharmacy** - Pharmacies référencées
2. **admin** - Comptes administrateurs
3. **location_submission** - Soumissions de localisation GPS
4. **info_submission** - Soumissions de corrections d'info
5. **pharmacy_view** - Comptage des vues
6. **suggestion** - Suggestions/commentaires utilisateurs
7. **pharmacy_proposal** - Propositions de nouvelles pharmacies
8. **emergency_contact** - Numéros d'urgence
9. **site_settings** - Configuration du site
10. **popup_message** - Messages popup affichés aux visiteurs
11. **advertisement** - Publicités
12. **ad_settings** - Paramètres du système publicitaire
13. **activity_log** - Journal d'activité

## Vérification d'intégrité

### Scripts fournis

#### 1. `init_db.py` - Initialisation initiale
- ✅ Crée les tables si elles n'existent pas
- ✅ Utilise `db.create_all()` (sûr - ne supprime rien)
- ✅ Initialise les paramètres SEO par défaut
- ✅ Crée le compte administrateur

**Utilisation:**
```bash
python init_db.py
```

#### 2. `migrate_db.py` - Migration SÉCURISÉE (NOUVEAU)
- ✅ Vérifie l'intégrité de toutes les tables
- ✅ Crée les tables manquantes sans supprimer les données
- ✅ Ajoute les colonnes manquantes
- ✅ Rapport détaillé

**Utilisation:**
```bash
python migrate_db.py
```

## Sécurité des données

### Garanties

✅ **Les données existantes ne sont JAMAIS supprimées**
- `db.create_all()` ne supprime pas les tables
- ALTER TABLE n'affecte pas les données
- Les migrations sont unidirectionnelles (avant → après)

✅ **Vérifications intégrées**
- Détection des tables manquantes
- Détection des colonnes manquantes
- Rapports d'erreur clairs

✅ **Backup recommandé**
```bash
pg_dump DATABASE_URL > backup.sql
```

## Processus de migration

### Avant une mise à jour

1. **Sauvegarder les données**
   ```bash
   pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
   ```

2. **Vérifier l'intégrité**
   ```bash
   python migrate_db.py
   ```

3. **Appliquer les changements**
   ```bash
   python init_db.py
   ```

### En cas de problème

1. **Restaurer depuis le backup**
   ```bash
   psql $DATABASE_URL < backup_YYYYMMDD.sql
   ```

2. **Vérifier les logs**
   ```
   Consulter docs/DATABASE_INTEGRITY.md
   Consulter docs/SECURITY_AUDIT.md
   ```

## Vérification manuelle

### Accès direct à la BD

```python
from app import app
from extensions import db

with app.app_context():
    # Vérifier les tables
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print("Tables:", tables)
    
    # Vérifier une table spécifique
    columns = inspector.get_columns('pharmacy')
    for col in columns:
        print(f"  {col['name']}: {col['type']}")
```

## Historique des changements

### Session 2 - December 19, 2025
- ✅ Création du script `migrate_db.py`
- ✅ Vérification d'intégrité automatisée
- ✅ Support des migrations sans perte de données
- ✅ Documentation complète

## Recommandations

### En production
1. **Tester d'abord en développement**
   - Exécuter migrate_db.py
   - Vérifier les logs
   - Valider les données

2. **Faire un backup avant chaque déploiement**
   ```bash
   pg_dump $DATABASE_URL > backup_pre_deploy.sql
   ```

3. **Monitorer après la migration**
   - Vérifier les logs d'erreur (docs/SECURITY_AUDIT.md)
   - Checker les statistiques (GET /api/stats)
   - Valider les données critiques

### Pour les développeurs
1. Toujours ajouter des migrations progressives
2. Utiliser `checkfirst=True` pour ALTER TABLE
3. Tester avec des données de test d'abord
4. Documenter les changements de schéma

## Conclusion

✅ La base de données est **SÛRE** et **ÉVOLUTIVE**

Tous les scripts de migration respectent le principe:
- **Pas de suppression** de données
- **Pas de modification** des données existantes
- **Ajout** de nouvelles structures uniquement
- **Vérification** automatique d'intégrité

---

**Support:** Pour toute question, consulter:
- `docs/ARCHITECTURE.md` - Structure technique
- `docs/SECURITY_AUDIT.md` - Sécurité
- `init_db.py` - Initialisation
- `migrate_db.py` - Migration sécurisée
