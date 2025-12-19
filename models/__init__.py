"""
UrgenceMaroc.com
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com

models/__init__.py - Module des modèles de données
Ce fichier exporte tous les modèles de la base de données utilisés dans l'application.
"""

from models.pharmacy import Pharmacy
from models.admin import Admin
from models.submission import LocationSubmission, InfoSubmission, PharmacyView, Suggestion, PharmacyProposal
from models.emergency_contact import EmergencyContact
from models.site_settings import SiteSettings, PopupMessage
from models.advertisement import Advertisement, AdSettings
from models.activity_log import ActivityLog

__all__ = ['Pharmacy', 'Admin', 'LocationSubmission', 'InfoSubmission', 'PharmacyView', 'Suggestion', 'PharmacyProposal', 'EmergencyContact', 'SiteSettings', 'PopupMessage', 'Advertisement', 'AdSettings', 'ActivityLog']
