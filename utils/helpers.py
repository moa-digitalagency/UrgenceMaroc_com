"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

utils/helpers.py - Fonctions utilitaires
Ce fichier contient les coordonnées GPS des villes du Maroc
et des fonctions helper comme safe_float pour la conversion de données.
"""

CITY_COORDINATES = {
    "Libreville": {"lat": 0.4162, "lng": 9.4673},
    "Port-Gentil": {"lat": -0.7193, "lng": 8.7815},
    "Franceville": {"lat": -1.6333, "lng": 13.5833},
    "Moanda": {"lat": -1.5333, "lng": 13.2000},
    "Makokou": {"lat": 0.5667, "lng": 12.8500},
    "Oyem": {"lat": 1.6000, "lng": 11.5833},
    "Mouila": {"lat": -1.8667, "lng": 11.0500},
    "Koulamoutou": {"lat": -1.1333, "lng": 12.4667},
    "Ntom": {"lat": 0.3667, "lng": 9.7667}
}


def safe_float(value):
    """Safely convert a value to float, returning None for empty/invalid values."""
    if value is None or value == '':
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None
