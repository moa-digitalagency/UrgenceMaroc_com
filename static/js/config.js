/**
 * UrgenceMaroc.com
 * By MOA Digital Agency LLC
 * Developed by: Aisance KALONJI
 * Contact: moa@myoneart.com
 * Website: www.myoneart.com
 *
 * static/js/config.js - Configuration globale
 * Ce fichier contient les constantes de configuration: coordonnées des villes,
 * couleurs par ville, types d'établissement et catégories d'emplacement.
 */

const CITY_CENTERS = {
    "Libreville": [0.4162, 9.4673],
    "Port-Gentil": [-0.7193, 8.7815],
    "Franceville": [-1.6333, 13.5833],
    "Moanda": [-1.5333, 13.2000],
    "Makokou": [0.5667, 12.8500],
    "Oyem": [1.6000, 11.5833],
    "Mouila": [-1.8667, 11.0500],
    "Koulamoutou": [-1.1333, 12.4667],
    "Ntom": [0.3667, 9.7667]
};

const CITY_COLORS = {
    "Libreville": "bg-blue-100 text-blue-700",
    "Port-Gentil": "bg-purple-100 text-purple-700",
    "Franceville": "bg-orange-100 text-orange-700",
    "Moanda": "bg-pink-100 text-pink-700",
    "Makokou": "bg-cyan-100 text-cyan-700",
    "Oyem": "bg-amber-100 text-amber-700",
    "Mouila": "bg-lime-100 text-lime-700",
    "Koulamoutou": "bg-rose-100 text-rose-700",
    "Ntom": "bg-teal-100 text-teal-700"
};

const TYPE_COLORS = {
    'pharmacie_generale': { border: 'border-l-emerald-500', bg: 'bg-emerald-100', text: 'text-emerald-700', label: 'Pharmacie générale' },
    'depot_pharmaceutique': { border: 'border-l-orange-500', bg: 'bg-orange-100', text: 'text-orange-700', label: 'Dépôt pharmaceutique' },
    'pharmacie_hospitaliere': { border: 'border-l-purple-500', bg: 'bg-purple-100', text: 'text-purple-700', label: 'Pharmacie hospitalière' }
};

const CATEGORY_LABELS = {
    'standard': 'Standard',
    'gare': 'Gare',
    'hopital': 'Hôpital',
    'aeroport': 'Aéroport',
    'centre_commercial': 'Centre commercial',
    'marche': 'Marché',
    'centre_ville': 'Centre-ville',
    'zone_residentielle': 'Zone résidentielle'
};

function getCityBadgeClass(ville) {
    return CITY_COLORS[ville] || "bg-gray-100 text-gray-700";
}

function normalizeTypeEtablissement(typeStr) {
    if (!typeStr) return 'pharmacie_generale';
    const lower = typeStr.toLowerCase();
    if (lower.includes('dépôt') || lower.includes('depot')) return 'depot_pharmaceutique';
    if (lower.includes('hospitalière') || lower.includes('hospitaliere')) return 'pharmacie_hospitaliere';
    return 'pharmacie_generale';
}

function getTypeStyle(pharmacy) {
    const normalizedType = normalizeTypeEtablissement(pharmacy.type_etablissement);
    return TYPE_COLORS[normalizedType] || TYPE_COLORS['pharmacie_generale'];
}

// Expose to global scope
window.CITY_CENTERS = CITY_CENTERS;
window.CITY_COLORS = CITY_COLORS;
window.TYPE_COLORS = TYPE_COLORS;
window.CATEGORY_LABELS = CATEGORY_LABELS;
window.getCityBadgeClass = getCityBadgeClass;
window.normalizeTypeEtablissement = normalizeTypeEtablissement;
window.getTypeStyle = getTypeStyle;
