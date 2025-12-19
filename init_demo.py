#!/usr/bin/env python3
"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

init_demo.py - Données de démonstration
Ce fichier contient les données initiales pour les pharmacies, contacts d'urgence
et autres informations de démonstration pour le Maroc.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

env_file = Path('.env')
if env_file.exists():
    load_dotenv(env_file)

from app import app
from extensions import db
from models.pharmacy import Pharmacy
from models.emergency_contact import EmergencyContact
from models.site_settings import PopupMessage
from models.admin import Admin
from utils.helpers import CITY_COORDINATES

EMERGENCY_CONTACTS_DATA = [
    {"ville": None, "service_type": "police", "label": "Police Secours (National)", "phone_numbers": "1730 / 177", "notes": "Numéro national d'urgence police", "is_national": True, "ordering": 1},
    {"ville": None, "service_type": "pompiers", "label": "Pompiers (National)", "phone_numbers": "18", "notes": "Numéro national des sapeurs-pompiers", "is_national": True, "ordering": 2},
    {"ville": None, "service_type": "ambulance", "label": "Ambulance / SAMU (National)", "phone_numbers": "1300 - 1399", "notes": "Numéros d'urgence médicale selon le réseau", "is_national": True, "ordering": 3},
    {"ville": None, "service_type": "sos_medecins", "label": "SOS Médecins (National)", "phone_numbers": "1300 / 0174 / 0880", "notes": "Selon votre opérateur téléphonique", "is_national": True, "ordering": 4},
    {"ville": "Libreville", "service_type": "police", "label": "Police Libreville", "phone_numbers": "177 / 011 72 00 37", "notes": "Commissariat Central de Libreville", "is_national": False, "ordering": 10},
    {"ville": "Libreville", "service_type": "hopital", "label": "CHU de Libreville", "phone_numbers": "011 76 24 46", "address": "Boulevard Omar Bongo, Libreville", "notes": "Centre Hospitalier Universitaire - Urgences 24h/24", "is_national": False, "ordering": 11},
    {"ville": "Libreville", "service_type": "clinique", "label": "Clinique El Rapha", "phone_numbers": "011 44 34 44", "address": "Libreville", "notes": "Clinique privée avec service d'urgence", "is_national": False, "ordering": 12},
    {"ville": "Libreville", "service_type": "hopital", "label": "Hôpital d'Instructions des Armées", "phone_numbers": "011 76 00 55", "address": "Libreville", "notes": "Hôpital militaire avec urgences", "is_national": False, "ordering": 13},
    {"ville": "Libreville", "service_type": "ambulance", "label": "SAMU Libreville", "phone_numbers": "1300 / 011 76 24 46", "notes": "Service d'Aide Médicale Urgente", "is_national": False, "ordering": 14},
    {"ville": "Port-Gentil", "service_type": "police", "label": "Police Port-Gentil", "phone_numbers": "011 55 22 36", "notes": "Commissariat de Port-Gentil", "is_national": False, "ordering": 20},
    {"ville": "Port-Gentil", "service_type": "hopital", "label": "Hôpital Régional de Port-Gentil", "phone_numbers": "011 55 20 44", "address": "Port-Gentil", "notes": "Hôpital régional avec urgences", "is_national": False, "ordering": 21},
    {"ville": "Port-Gentil", "service_type": "clinique", "label": "Clinique Mandji", "phone_numbers": "011 55 39 00", "address": "Port-Gentil", "notes": "Clinique privée de référence", "is_national": False, "ordering": 22},
    {"ville": "Franceville", "service_type": "police", "label": "Police Franceville", "phone_numbers": "011 67 72 76 / 011 67 72 94", "notes": "Commissariat de Franceville", "is_national": False, "ordering": 30},
    {"ville": "Franceville", "service_type": "hopital", "label": "Hôpital Régional de Franceville", "phone_numbers": "011 67 72 33", "address": "Franceville", "notes": "Hôpital régional du Haut-Ogooué", "is_national": False, "ordering": 31},
    {"ville": "Oyem", "service_type": "hopital", "label": "Hôpital Régional d'Oyem", "phone_numbers": "011 98 60 16", "address": "Oyem", "notes": "Hôpital régional du Woleu-Ntem", "is_national": False, "ordering": 40},
    {"ville": "Mouila", "service_type": "hopital", "label": "Hôpital Régional de Mouila", "phone_numbers": "011 86 12 33", "address": "Mouila", "notes": "Hôpital régional de la Ngounié", "is_national": False, "ordering": 50},
    {"ville": "Makokou", "service_type": "hopital", "label": "Hôpital Régional de Makokou", "phone_numbers": "011 66 10 20", "address": "Makokou", "notes": "Hôpital régional de l'Ogooué-Ivindo", "is_national": False, "ordering": 60},
    {"ville": "Koulamoutou", "service_type": "hopital", "label": "Hôpital Régional de Koulamoutou", "phone_numbers": "011 65 10 25", "address": "Koulamoutou", "notes": "Hôpital régional de l'Ogooué-Lolo", "is_national": False, "ordering": 70},
]

PHARMACIES_DATA = [
    {"id": "LBV001", "nom": "Grande Pharmacie des Forestiers", "ville": "Libreville", "quartier": "Galerie de Mbolo", "telephone": "011 72 23 52", "bp": "2", "horaires": "Lun-Sam: 8h-19h30, Dim: 8h-18h", "services": "Parapharmacie, Conseil pharmaceutique", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "centre_commercial"},
    {"id": "LBV002", "nom": "La Nouvelle Pharmacie d'Awondo", "ville": "Libreville", "quartier": "Louis, Avenue Jean-Jacques Boucavel", "telephone": "011 44 57 07 / 066 15 80 00", "bp": "23537", "horaires": "24h/24 - 7j/7", "services": "Ordonnances, Conseil, Parapharmacie, Espace bébé, Matériel médical", "proprietaire": "Dr Yoba Bernadette", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville", "is_garde": True},
    {"id": "LBV003", "nom": "Pharmacie Avolenzame", "ville": "Libreville", "quartier": "Nkembo, Route Atong Abè", "telephone": "065 29 10 02", "bp": "1685", "horaires": "7j/7: 7h-20h", "services": "Service courant", "proprietaire": "Dr Ntogone Patience", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV004", "nom": "Pharmacie d'Akébé", "ville": "Libreville", "quartier": "Akébé Ville, Rond-point de l'église", "telephone": "011 72 01 38", "bp": "14349", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "Akani Monique", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV005", "nom": "Grande Pharmacie Pauline", "ville": "Libreville", "quartier": "Alenakiri", "telephone": "", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "Corinne Nseng Nseng Ndong", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV006", "nom": "Pharmacie d'Avorbam", "ville": "Libreville", "quartier": "Rond-point d'Avorbam", "telephone": "065 50 54 54", "bp": "12844", "horaires": "24h/24 - 7j/7", "services": "Service complet", "proprietaire": "Julie Prescilla Ada Mve", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville", "is_garde": True},
    {"id": "LBV007", "nom": "Pharmacie de Bikélé", "ville": "Libreville", "quartier": "Bikélé, Près Prix Import", "telephone": "", "bp": "6091", "horaires": "24h/24 - 7j/7", "services": "Service complet", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle", "is_garde": True},
    {"id": "LBV008", "nom": "Pharmacie de la Grâce", "ville": "Libreville", "quartier": "Angondjé, Parcelle N°26", "telephone": "062 94 94 24", "bp": "", "horaires": "24h/24 - 7j/7", "services": "Service complet", "proprietaire": "Mbadinga Mbadinga Carine", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle", "is_garde": True},
    {"id": "LBV009", "nom": "Pharmacie Le Bon Samaritain", "ville": "Libreville", "quartier": "Angondjé, Carrefour Sherko", "telephone": "065 19 03 40", "bp": "", "horaires": "24h/24 - 7j/7", "services": "Service complet", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle", "is_garde": True},
    {"id": "LBV010", "nom": "Pharmacie de l'Orchidée", "ville": "Libreville", "quartier": "Louis (Montée)", "telephone": "011 73 24 19 / 062 64 54 70", "bp": "", "horaires": "24h/24 - 7j/7", "services": "Service complet", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville", "is_garde": True},
    {"id": "LBV011", "nom": "Pharmacie de Sibang-Montalier", "ville": "Libreville", "quartier": "Bambouchine, Rue Philibert M'Bembo Pangou", "telephone": "011 71 15 16 / 062 76 84 50 / 065 20 68 44 / 062 07 20 28", "bp": "2906", "horaires": "24h/24 - 7j/7", "services": "Service complet", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle", "is_garde": True},
    {"id": "LBV012", "nom": "Pharmacie des Acaé", "ville": "Libreville", "quartier": "Carrefour ACAÉ", "telephone": "011 70 49 49", "bp": "", "horaires": "24h/24 - 7j/7", "services": "Service complet", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville", "is_garde": True},
    {"id": "LBV013", "nom": "Pharmacie Les Marguerites", "ville": "Libreville", "quartier": "Awendjé", "telephone": "011 77 14 02 / 066 43 47 01", "bp": "", "horaires": "24h/24 - 7j/7", "services": "Service complet", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle", "is_garde": True},
    {"id": "LBV014", "nom": "Pharmacie Mukemussailay", "ville": "Libreville", "quartier": "Nzeng-Ayong (Dragages)", "telephone": "065 19 03 26", "bp": "", "horaires": "24h/24 - 7j/7", "services": "Service complet", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle", "is_garde": True},
    {"id": "LBV015", "nom": "Pharmacie Nouo Cécile", "ville": "Libreville", "quartier": "IAI", "telephone": "066 28 35 22", "bp": "", "horaires": "24h/24 - 7j/7", "services": "Service complet", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle", "is_garde": True},
    {"id": "LBV016", "nom": "Pharmacie Nzeng-Ayong", "ville": "Libreville", "quartier": "Immeuble les Rosiers", "telephone": "011 71 06 16 / 065 19 03 26", "bp": "6087", "horaires": "24h/24 - 7j/7", "services": "Service complet", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle", "is_garde": True},
    {"id": "LBV017", "nom": "Pharmacie Ondogo", "ville": "Libreville", "quartier": "Ondogo, Après cité de la GR", "telephone": "065 51 68 58", "bp": "", "horaires": "24h/24 - 7j/7", "services": "Service complet", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle", "is_garde": True},
    {"id": "LBV018", "nom": "Pharmacie Rapha-Ël", "ville": "Libreville", "quartier": "Rond-point PK12, Immeuble City Star", "telephone": "011 46 45 54 / 074 42 02 48", "bp": "", "horaires": "24h/24 - 7j/7", "services": "Service complet", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle", "is_garde": True},
    {"id": "LBV019", "nom": "Pharmacie Centrale de Garde", "ville": "Libreville", "quartier": "Centre-ville, Face Agatour/Commissariat Central", "telephone": "066 15 87 44 / 077 07 01 99", "bp": "", "horaires": "7j/7: 19h-8h, 24h/24: dim & jours fériés", "services": "Service d'urgence", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville", "is_garde": True},
    {"id": "LBV020", "nom": "Pharmacie de Garde Beau Séjour", "ville": "Libreville", "quartier": "Beau Séjour (GIE), Centre social Beauséjour", "telephone": "065 19 03 36", "bp": "", "horaires": "24h/24 - 7j/7", "services": "Service d'urgence", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle", "is_garde": True},
    {"id": "LBV021", "nom": "Pharmacie de Garde de Nzeng-Ayong", "ville": "Libreville", "quartier": "Nzeng Ayong", "telephone": "066 73 45 41 / 011 71 23 67", "bp": "", "horaires": "24h/24 - 7j/7", "services": "Service d'urgence", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle", "is_garde": True},
    {"id": "LBV022", "nom": "Pharmacie de Garde du PK6", "ville": "Libreville", "quartier": "PK6, Immeuble Beyrouth", "telephone": "066 50 41 16 / 011 77 21 52", "bp": "488", "horaires": "24h/24 - 7j/7", "services": "Service d'urgence", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle", "is_garde": True},
    {"id": "LBV023", "nom": "Pharmacie de l'Aéroport", "ville": "Libreville", "quartier": "Aéroport", "telephone": "077 77 77 77 / 065 50 63 99", "bp": "5453", "horaires": "7j/7: 8h-21h", "services": "Service courant", "proprietaire": "Glen-Chancy Ella Mebiame", "type_etablissement": "pharmacie_generale", "categorie": "aeroport"},
    {"id": "LBV024", "nom": "Pharmacie de l'Express J.J et M.", "ville": "Libreville", "quartier": "Charbonnages, Station PetroMaroc", "telephone": "011 73 41 41", "bp": "", "horaires": "7j/7", "services": "Service courant", "proprietaire": "Doe Fausther Graciella Maddly", "type_etablissement": "pharmacie_generale", "categorie": "standard"},
    {"id": "LBV025", "nom": "Pharmacie des Facultés", "ville": "Libreville", "quartier": "Ancienne Sobraga, Ambassade Cameroun", "telephone": "011 44 37 38", "bp": "", "horaires": "7h30-21h30 (20h sam)", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "standard"},
    {"id": "LBV026", "nom": "Pharmacie des Gué-Gué", "ville": "Libreville", "quartier": "Rond-point Gué-Gué", "telephone": "011 44 41 36 / 065 19 03 40", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV027", "nom": "Pharmacie des Hirondelles", "ville": "Libreville", "quartier": "Alibandeng", "telephone": "", "bp": "", "horaires": "7j/7", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV028", "nom": "Pharmacie de la Kiyine", "ville": "Libreville", "quartier": "Trois-Quartiers", "telephone": "011 44 60 42 / 060 40 60 37", "bp": "", "horaires": "7j/7", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV029", "nom": "Pharmacie de Plaine Niger", "ville": "Libreville", "quartier": "Carrefour Boulingui", "telephone": "011 74 06 06", "bp": "", "horaires": "7j/7: Lun-Sam 8h-21h, Dim 8h-20h", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV030", "nom": "Pharmacie d'Oloumi", "ville": "Libreville", "quartier": "Z.I. Oloumi", "telephone": "011 72 15 82", "bp": "4060/4039", "horaires": "7j/7: 7h30-20h30 (8h-20h30 fériés)", "services": "Service courant", "proprietaire": "Hadad Keba Walid", "type_etablissement": "pharmacie_generale", "categorie": "standard"},
    {"id": "LBV031", "nom": "Pharmacie Sainte-Marie", "ville": "Libreville", "quartier": "Boulevard Triomphal (face Mbolo)", "telephone": "011 74 00 52", "bp": "1838", "horaires": "Lun-Sam: 7h30-21h, Dim: 8h-20h", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
    {"id": "LBV032", "nom": "Pharmacie Iboga de Glass", "ville": "Libreville", "quartier": "Glass, Avenue G. Damas", "telephone": "011 77 23 99 / 011 74 87 98", "bp": "2226", "horaires": "7h30-21h (20h sam)", "services": "Service courant", "proprietaire": "Gassita Laurence Victorine", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV033", "nom": "Pharmacie Jeanne et Léo", "ville": "Libreville", "quartier": "Owendo (Carrefour SNI)", "telephone": "011 70 47 60", "bp": "15592", "horaires": "7j/7: Lun-Sam 7h30-20h30, Dim 8h-18h", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
    {"id": "LBV034", "nom": "Pharmacie La Librevilloise", "ville": "Libreville", "quartier": "Centre-ville", "telephone": "", "bp": "", "horaires": "7h30-21h30 - 7j/7", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
    {"id": "LBV035", "nom": "Pharmacie Marie-Jeanne", "ville": "Libreville", "quartier": "Nombakélé", "telephone": "011 77 58 09", "bp": "16024", "horaires": "8h-21h non-stop (7j/7)", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV036", "nom": "Pharmacie du Commissariat Central", "ville": "Libreville", "quartier": "Centre-ville", "telephone": "074 64 22", "bp": "6087", "horaires": "8h-21h45 - 7j/7", "services": "Service courant", "proprietaire": "Itou-Y-Maganga/Ziza Sandrine M", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
    {"id": "LBV037", "nom": "Pharmacie Marocaine", "ville": "Libreville", "quartier": "Entre 9 étages et Cinéma Komo", "telephone": "011 74 30 71", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
    {"id": "LBV038", "nom": "Pharmacie Le Président", "ville": "Libreville", "quartier": "Immeuble Le Président", "telephone": "011 74 12 48", "bp": "", "horaires": "8h-19h", "services": "Service courant", "proprietaire": "Okome Essono Cynthia", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
    {"id": "LBV039", "nom": "Pharmacie Royal", "ville": "Libreville", "quartier": "Oloumi (Galerie Royal Plaza/Xanadou)", "telephone": "011 76 91 06", "bp": "10880", "horaires": "7j/7: 7h30-19h30 (Dim 9h-15h)", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "centre_commercial"},
    {"id": "LBV040", "nom": "Pharmacie Saint Antoine", "ville": "Libreville", "quartier": "Carrefour SNI, Après Prix Import", "telephone": "011 70 74 60", "bp": "1063", "horaires": "7j/7", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
    {"id": "LBV041", "nom": "Pharmacie Emmanuel", "ville": "Libreville", "quartier": "Awendjé", "telephone": "065 65 65 31", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV042", "nom": "Pharmacie Saint André", "ville": "Libreville", "quartier": "Dispensaire d'Okala", "telephone": "066 25 56 67", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "hopital"},
    {"id": "LBV043", "nom": "Pharmacie de la Gare Routière", "ville": "Libreville", "quartier": "Galerie Gare Routière", "telephone": "", "bp": "16249", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "gare"},
    {"id": "LBV044", "nom": "Pharmacie de la Poste", "ville": "Libreville", "quartier": "Galerie Hollando (Bord de Mer)", "telephone": "011 72 83 30", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
    {"id": "LBV045", "nom": "Pharmacie de St Joseph de Lalala", "ville": "Libreville", "quartier": "Lalala", "telephone": "", "bp": "379", "horaires": "8h-20h (fermée dimanche)", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV046", "nom": "Pharmacie des Jardins de la Peyrie", "ville": "Libreville", "quartier": "La Peyrie", "telephone": "011 72 33 33", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV047", "nom": "Pharmacie du Rond-Point la Plaine", "ville": "Libreville", "quartier": "La Plaine", "telephone": "066 04 41 21 / 011 74 70 50", "bp": "503", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "Okowa Aline", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV048", "nom": "Pharmacie du Lycée Technique", "ville": "Libreville", "quartier": "Owendo, Avant Lycée Technique", "telephone": "077 05 01 90", "bp": "19193", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV049", "nom": "Pharmacie Nouvelle Owendo", "ville": "Libreville", "quartier": "Owendo", "telephone": "011 70 27 80", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV050", "nom": "Pharmacie Razel", "ville": "Libreville", "quartier": "Owendo Business Center", "telephone": "065 19 02 97", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "centre_commercial"},
    {"id": "LBV051", "nom": "Grande Pharmacie l'Acacia", "ville": "Libreville", "quartier": "PK5", "telephone": "066 41 41 86 / 029 42 85 3", "bp": "2682", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "Nzongou Casimir Raoul", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV052", "nom": "Pharmacie Nibigholet", "ville": "Libreville", "quartier": "PK8", "telephone": "065 19 03 17", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV053", "nom": "Pharmacie Le Maïs", "ville": "Libreville", "quartier": "PK9", "telephone": "065 09 00 49", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV054", "nom": "Pharmacie Dissang Dietou", "ville": "Libreville", "quartier": "Melen PK11", "telephone": "011 46 45 54", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV055", "nom": "Pharmacie Elbous", "ville": "Libreville", "quartier": "Libreville (divers)", "telephone": "069 26 083", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "standard"},
    {"id": "LBV056", "nom": "Pharmacie du Golf", "ville": "Libreville", "quartier": "Libreville (divers)", "telephone": "077 75 380", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV057", "nom": "Pharmacie du Lys", "ville": "Libreville", "quartier": "Libreville (divers)", "telephone": "065 34 61 52", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "standard"},
    {"id": "LBV058", "nom": "Pharmacie du PK12", "ville": "Libreville", "quartier": "Libreville (divers)", "telephone": "023 13 797", "bp": "12267", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV059", "nom": "Pharmacie du PK8", "ville": "Libreville", "quartier": "Libreville (divers)", "telephone": "032 85 44", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV060", "nom": "Pharmacie GIE Beau Séjour", "ville": "Libreville", "quartier": "GIE", "telephone": "074 37 60 37", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV061", "nom": "Pharmacie GIE PK6", "ville": "Libreville", "quartier": "GIE PK6", "telephone": "067 56 112", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV062", "nom": "Pharmacie Hélène", "ville": "Libreville", "quartier": "Owendo", "telephone": "066 56 20 96", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV063", "nom": "Pharmacie d'Akournam II", "ville": "Libreville", "quartier": "Owendo (Akournam)", "telephone": "070 56 89", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "Eloumi Ropivia Jacqueline", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV064", "nom": "Pharmacie d'Awendjé", "ville": "Libreville", "quartier": "Awendjé", "telephone": "076 59 73 / 060 03 26 51", "bp": "9669", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "Mengue Bengone Bernadette", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV065", "nom": "Pharmacie d'Okala Village", "ville": "Libreville", "quartier": "Dispensaire d'Okala", "telephone": "045 55 06", "bp": "6038", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "Ditsambo Vincent", "type_etablissement": "pharmacie_generale", "categorie": "hopital"},
    {"id": "LBV066", "nom": "Pharmacie d'Agondije", "ville": "Libreville", "quartier": "Angondjé", "telephone": "032 46 67 / 028 45 91", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "Moussonda Georges", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV067", "nom": "Pharmacie Coeur de Jesus", "ville": "Libreville", "quartier": "Angondjé", "telephone": "065 19 03 02", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "Poaty Annie Josette", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV068", "nom": "Pharmacie Blanche et Elise", "ville": "Libreville", "quartier": "Nialy", "telephone": "062 05 51 50", "bp": "13977", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "Alaric Farel Ekowa Ndoumou", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "LBV069", "nom": "Pharmacie Carrefour JJ", "ville": "Libreville", "quartier": "Libreville", "telephone": "011 45 03 73 / 070 70 166", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "Doe Fausther Graciella Maddly", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
    {"id": "LBV070", "nom": "Pharmacie Espérance des Cocotiers", "ville": "Libreville", "quartier": "Après station Nkembo", "telephone": "077 67 53 48", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "PG001", "nom": "Pharmacie Banco", "ville": "Port-Gentil", "quartier": "Boulevard Léon Mba, Carrefour Banco", "telephone": "011 55 50 45 / 074 61 77 12", "bp": "1527", "horaires": "Horaires standards", "services": "Allopathie, Homéopathie, Aromathérapie, Phytothérapie, Parfumerie", "proprietaire": "Dr Rebienot Pellégrin Olivier", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
    {"id": "PG002", "nom": "Pharmacie Centrale", "ville": "Port-Gentil", "quartier": "Parking Rétro", "telephone": "011 55 21 64 / 01 55 21 64", "bp": "640", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "Mr Poyet", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
    {"id": "PG003", "nom": "Pharmacie du Boulevard", "ville": "Port-Gentil", "quartier": "Boulevard Léon Mba", "telephone": "011 53 11 03 / 043 34 113", "bp": "1922", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "Dr Annick Divounguy", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
    {"id": "PG004", "nom": "Pharmacie du Cap", "ville": "Port-Gentil", "quartier": "Centre-ville, Galerie Casino", "telephone": "011 55 26 80", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "centre_commercial"},
    {"id": "PG005", "nom": "Pharmacie du Grand Village", "ville": "Port-Gentil", "quartier": "Grand Village, Rue principale", "telephone": "011 55 34 83", "bp": "", "horaires": "Horaires standards", "services": "Service courant, Réputée", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "PG006", "nom": "Pharmacie Radoca", "ville": "Port-Gentil", "quartier": "Quartier la Balise", "telephone": "011 55 10 72", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "PG007", "nom": "Pharmacie Von'Okuwa", "ville": "Port-Gentil", "quartier": "Centre-ville, Près Hôtel Mandji", "telephone": "011 55 55 32", "bp": "1794", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
    {"id": "PG008", "nom": "Pharmacie Andrea", "ville": "Port-Gentil", "quartier": "Boulevard Léon Mba", "telephone": "022 62 666 / 07 07 03 97 96", "bp": "1228", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "Dr Andrea Olivier", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
    {"id": "FV001", "nom": "Pharmacie du Plateau", "ville": "Franceville", "quartier": "Quartier Potos", "telephone": "06 77 502", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "zone_residentielle"},
    {"id": "FV002", "nom": "Pharmacie Moderne", "ville": "Franceville", "quartier": "Rue des Maquis", "telephone": "", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
    {"id": "MK001", "nom": "Pharmacie du Marché Central", "ville": "Makokou", "quartier": "Marché Central", "telephone": "077 13 30 89", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "marche"},
    {"id": "KM001", "nom": "Dépôt Pharmaceutique des Forestiers", "ville": "Koulamoutou", "quartier": "Koulamoutou", "telephone": "011 65 50 08", "bp": "100", "horaires": "Lun-Sam: 7h30-20h", "services": "Dépôt pharmaceutique", "proprietaire": "", "type_etablissement": "depot_pharmaceutique", "categorie": "centre_ville"},
    {"id": "NT001", "nom": "Pharmacie Clementine", "ville": "Ntom", "quartier": "Ntom", "telephone": "062 57 76 22", "bp": "", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "Ambolo Kanga Chelsy Michelle", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
    {"id": "MD001", "nom": "Dépôt Phar. Boundama", "ville": "Moanda", "quartier": "Moanda", "telephone": "02 66 85 3 / 026 68 53", "bp": "", "horaires": "Horaires standards", "services": "Dépôt pharmaceutique", "proprietaire": "Chami Frederic R", "type_etablissement": "depot_pharmaceutique", "categorie": "centre_ville"},
    {"id": "MD002", "nom": "Pharmacie de Moanda", "ville": "Moanda", "quartier": "Moanda", "telephone": "028 27 15", "bp": "2372", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
    {"id": "OY001", "nom": "Pharmacie Pascale Magalie Nfoumou", "ville": "Oyem", "quartier": "Oyem", "telephone": "077 84 50 61", "bp": "1207", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "Ndoumou Obame Daniel", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
    {"id": "ML001", "nom": "Pharmacie Bangolouis", "ville": "Mouila", "quartier": "Mouila", "telephone": "074 41 96 16", "bp": "162", "horaires": "Horaires standards", "services": "Service courant", "proprietaire": "Dr Mahoumbou Aude Felicia", "type_etablissement": "pharmacie_generale", "categorie": "centre_ville"},
]

def init_demo_data(force=False):
    with app.app_context():
        if Pharmacy.query.count() > 0:
            print(f"Database already contains {Pharmacy.query.count()} pharmacies.")
            if not force:
                print("Use --force to clear and reimport.")
                return
            Pharmacy.query.delete()
            db.session.commit()
            print("Existing pharmacies cleared.")

        quartier_offsets = {}
        count = 0

        for idx, row in enumerate(PHARMACIES_DATA):
            ville = row.get('ville', '')
            quartier = row.get('quartier', '')

            base_coords = CITY_COORDINATES.get(ville, {"lat": 0.4162, "lng": 9.4673})

            offset_key = f"{ville}_{quartier}"
            if offset_key not in quartier_offsets:
                quartier_offsets[offset_key] = len(quartier_offsets)

            offset_idx = quartier_offsets[offset_key] + idx
            lat_offset = (offset_idx % 50) * 0.002 - 0.05
            lng_offset = (offset_idx // 50 % 50) * 0.002 - 0.05

            pharmacy = Pharmacy(
                code=row.get('id', f'PH{idx+1:03d}'),
                nom=row.get('nom', ''),
                ville=ville,
                quartier=quartier,
                telephone=row.get('telephone', ''),
                bp=row.get('bp', ''),
                horaires=row.get('horaires', ''),
                services=row.get('services', ''),
                proprietaire=row.get('proprietaire', ''),
                type_etablissement=row.get('type_etablissement', 'pharmacie_generale'),
                categorie_emplacement=row.get('categorie', 'standard'),
                latitude=base_coords["lat"] + lat_offset,
                longitude=base_coords["lng"] + lng_offset,
                is_garde=False,
                is_verified=False
            )
            db.session.add(pharmacy)
            count += 1

        db.session.commit()
        print(f"Successfully imported {count} pharmacies!")

        EmergencyContact.query.delete()
        db.session.commit()

        emergency_count = 0
        for contact_data in EMERGENCY_CONTACTS_DATA:
            contact = EmergencyContact(
                ville=contact_data.get('ville'),
                service_type=contact_data.get('service_type'),
                label=contact_data.get('label'),
                phone_numbers=contact_data.get('phone_numbers'),
                address=contact_data.get('address', ''),
                notes=contact_data.get('notes', ''),
                is_national=contact_data.get('is_national', False),
                ordering=contact_data.get('ordering', 0)
            )
            db.session.add(contact)
            emergency_count += 1

        db.session.commit()
        print(f"Successfully imported {emergency_count} emergency contacts!")

        PopupMessage.query.delete()
        db.session.commit()

        welcome_popup = PopupMessage(
            title="Bienvenue sur UrgenceMaroc.com",
            description="Découvrez la première plateforme qui réunit toutes les pharmacies du Maroc ! Trouvez aussi facilement la pharmacie de garde la plus proche et les contacts d'urgence où que vous soyez.",
            warning_text="Le projet est encore en construction — aidez-nous à le rendre meilleur ! Ajoutez une pharmacie manquante ou corrigez des infos… chaque contribution compte !",
            is_active=True,
            show_once=True,
            ordering=0
        )
        db.session.add(welcome_popup)
        db.session.commit()
        print("Welcome popup created!")


def init_superadmin():
    with app.app_context():
        admin_username = os.environ.get('ADMIN_USERNAME')
        admin_password = os.environ.get('ADMIN_PASSWORD')

        if not admin_username or not admin_password:
            print("Warning: ADMIN_USERNAME and/or ADMIN_PASSWORD not set in environment.")
            print("Superadmin creation skipped. Set these secrets to create an admin account.")
            return False

        existing_admin = Admin.query.filter_by(username=admin_username).first()
        if existing_admin:
            print(f"Admin '{admin_username}' already exists. Updating password...")
            existing_admin.set_password(admin_password)
            db.session.commit()
            print(f"Admin '{admin_username}' password updated successfully!")
        else:
            admin = Admin(username=admin_username)
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            print(f"Superadmin '{admin_username}' created successfully!")

        return True


if __name__ == "__main__":
    force = "--force" in sys.argv
    init_demo_data(force=force)
    init_superadmin()
