/**
 * UrgenceMaroc.com
 * By MOA Digital Agency LLC
 * Developed by: Aisance KALONJI
 * Contact: moa@myoneart.com
 * Website: www.myoneart.com
 *
 * static/js/forms.js - Formulaires de soumission
 * Ce fichier gère les formulaires: soumission de localisation GPS,
 * correction d'informations, suggestions et propositions de pharmacies.
 */

function showComplementInfo(pharmacyId) {
    const modal = document.getElementById('pharmacyModal');
    const title = document.getElementById('modalTitle');
    const content = document.getElementById('modalContent');
    
    title.textContent = 'Compléter les informations';
    
    content.innerHTML = '';
    const container = document.createElement('div');
    container.className = 'space-y-4';
    container.innerHTML = `
        <p class="text-sm text-gray-600">Choisissez le type d'information à soumettre :</p>
        
        <button class="location-btn w-full py-4 bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-xl flex items-center gap-3 transition">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center ml-3">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
            </div>
            <div class="text-left">
                <p class="font-semibold text-gray-800">Proposer une localisation GPS</p>
                <p class="text-sm text-gray-500">Envoyer les coordonnées de la pharmacie</p>
            </div>
        </button>
        
        <button class="info-btn w-full py-4 bg-amber-50 hover:bg-amber-100 border border-amber-200 rounded-xl flex items-center gap-3 transition">
            <div class="w-12 h-12 bg-amber-100 rounded-lg flex items-center justify-center ml-3">
                <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
            </div>
            <div class="text-left">
                <p class="font-semibold text-gray-800">Corriger une information</p>
                <p class="text-sm text-gray-500">Téléphone, horaires, services, etc.</p>
            </div>
        </button>
        
        <button class="cancel-btn w-full py-3 bg-gray-200 text-gray-700 font-semibold rounded-xl flex items-center justify-center gap-2 hover:bg-gray-300 transition mt-4">
            Annuler
        </button>
    `;
    
    content.appendChild(container);
    
    container.querySelector('.location-btn').addEventListener('click', () => showLocationForm(pharmacyId));
    container.querySelector('.info-btn').addEventListener('click', () => showInfoForm(pharmacyId));
    container.querySelector('.cancel-btn').addEventListener('click', closeModal);
    
    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

function showLocationForm(pharmacyId) {
    const content = document.getElementById('modalContent');
    const title = document.getElementById('modalTitle');
    
    title.textContent = 'Proposer une localisation';
    
    content.innerHTML = '';
    const container = document.createElement('div');
    container.className = 'space-y-4';
    container.innerHTML = `
        <div class="p-4 bg-blue-50 rounded-xl border border-blue-200">
            <p class="text-sm text-blue-700">
                Rendez-vous devant la pharmacie et cliquez sur "Utiliser ma position actuelle" pour envoyer les coordonnées GPS.
            </p>
        </div>
        
        <form id="locationForm" class="space-y-4">
            <div class="grid grid-cols-2 gap-3">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Latitude</label>
                    <input type="text" id="submitLat" readonly class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-600" placeholder="--">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Longitude</label>
                    <input type="text" id="submitLng" readonly class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-600" placeholder="--">
                </div>
            </div>
            
            <button type="button" class="get-position-btn w-full py-3 bg-blue-600 text-white font-semibold rounded-xl flex items-center justify-center gap-2 hover:bg-blue-700 transition">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                </svg>
                Utiliser ma position actuelle
            </button>
            
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Votre nom (optionnel)</label>
                <input type="text" id="submitName" class="w-full px-3 py-2 border border-gray-300 rounded-lg" placeholder="Votre nom">
            </div>
            
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Votre téléphone (optionnel)</label>
                <input type="tel" id="submitPhone" class="w-full px-3 py-2 border border-gray-300 rounded-lg" placeholder="Ex: 077 00 00 00">
            </div>
            
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Commentaire (optionnel)</label>
                <textarea id="submitComment" rows="2" class="w-full px-3 py-2 border border-gray-300 rounded-lg" placeholder="Informations supplémentaires..."></textarea>
            </div>
            
            <div class="flex gap-3">
                <button type="button" class="back-btn flex-1 py-3 bg-gray-200 text-gray-700 font-semibold rounded-xl hover:bg-gray-300 transition">
                    Retour
                </button>
                <button type="button" class="submit-btn flex-1 py-3 bg-emerald-600 text-white font-semibold rounded-xl hover:bg-emerald-700 transition">
                    Envoyer
                </button>
            </div>
        </form>
    `;
    
    content.appendChild(container);
    
    container.querySelector('.get-position-btn').addEventListener('click', getCurrentLocation);
    container.querySelector('.back-btn').addEventListener('click', () => showComplementInfo(pharmacyId));
    container.querySelector('.submit-btn').addEventListener('click', () => submitLocation(pharmacyId));
}

function showInfoForm(pharmacyId) {
    const content = document.getElementById('modalContent');
    const title = document.getElementById('modalTitle');
    
    title.textContent = 'Corriger une information';
    
    content.innerHTML = '';
    const container = document.createElement('div');
    container.className = 'space-y-4';
    container.innerHTML = `
        <form id="infoForm" class="space-y-4">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Type d'information à corriger</label>
                <select id="fieldName" class="w-full px-3 py-2 border border-gray-300 rounded-lg">
                    <option value="">Sélectionnez...</option>
                    <option value="telephone">Téléphone</option>
                    <option value="horaires">Horaires d'ouverture</option>
                    <option value="quartier">Quartier / Adresse</option>
                    <option value="services">Services proposés</option>
                    <option value="proprietaire">Propriétaire</option>
                </select>
            </div>
            
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Nouvelle valeur</label>
                <textarea id="proposedValue" rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-lg" placeholder="Entrez la valeur correcte..."></textarea>
            </div>
            
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Votre nom (optionnel)</label>
                <input type="text" id="infoSubmitName" class="w-full px-3 py-2 border border-gray-300 rounded-lg" placeholder="Votre nom">
            </div>
            
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Votre téléphone (optionnel)</label>
                <input type="tel" id="infoSubmitPhone" class="w-full px-3 py-2 border border-gray-300 rounded-lg" placeholder="Ex: 077 00 00 00">
            </div>
            
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Commentaire (optionnel)</label>
                <textarea id="infoSubmitComment" rows="2" class="w-full px-3 py-2 border border-gray-300 rounded-lg" placeholder="Précisions supplémentaires..."></textarea>
            </div>
            
            <div class="flex gap-3">
                <button type="button" class="back-btn flex-1 py-3 bg-gray-200 text-gray-700 font-semibold rounded-xl hover:bg-gray-300 transition">
                    Retour
                </button>
                <button type="button" class="submit-btn flex-1 py-3 bg-emerald-600 text-white font-semibold rounded-xl hover:bg-emerald-700 transition">
                    Envoyer
                </button>
            </div>
        </form>
    `;
    
    content.appendChild(container);
    
    container.querySelector('.back-btn').addEventListener('click', () => showComplementInfo(pharmacyId));
    container.querySelector('.submit-btn').addEventListener('click', () => submitInfo(pharmacyId));
}

function getCurrentLocation() {
    if (!navigator.geolocation) {
        alert('La géolocalisation n\'est pas supportée par votre navigateur');
        return;
    }
    
    const latInput = document.getElementById('submitLat');
    const lngInput = document.getElementById('submitLng');
    
    latInput.value = 'Chargement...';
    lngInput.value = 'Chargement...';
    
    navigator.geolocation.getCurrentPosition(
        (position) => {
            latInput.value = position.coords.latitude.toFixed(6);
            lngInput.value = position.coords.longitude.toFixed(6);
        },
        (error) => {
            latInput.value = '--';
            lngInput.value = '--';
            handleGeolocationError(error);
        }
    );
}

async function submitLocation(pharmacyId) {
    const lat = document.getElementById('submitLat').value;
    const lng = document.getElementById('submitLng').value;
    
    if (!lat || !lng || lat === '--' || lng === '--' || lat === 'Chargement...') {
        alert('Veuillez d\'abord obtenir votre position GPS');
        return;
    }
    
    const data = {
        latitude: parseFloat(lat),
        longitude: parseFloat(lng),
        name: document.getElementById('submitName').value,
        phone: document.getElementById('submitPhone').value,
        comment: document.getElementById('submitComment').value
    };
    
    try {
        const response = await fetch(`/api/pharmacy/${pharmacyId}/submit-location`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showSuccessMessage('Localisation envoyée ! Elle sera vérifiée par notre équipe.');
        } else {
            alert(result.error || 'Erreur lors de l\'envoi');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Erreur lors de l\'envoi. Veuillez réessayer.');
    }
}

async function submitInfo(pharmacyId) {
    const fieldName = document.getElementById('fieldName').value;
    const proposedValue = document.getElementById('proposedValue').value;
    
    if (!fieldName) {
        alert('Veuillez sélectionner le type d\'information');
        return;
    }
    
    if (!proposedValue.trim()) {
        alert('Veuillez entrer la nouvelle valeur');
        return;
    }
    
    const data = {
        field_name: fieldName,
        proposed_value: proposedValue,
        name: document.getElementById('infoSubmitName').value,
        phone: document.getElementById('infoSubmitPhone').value,
        comment: document.getElementById('infoSubmitComment').value
    };
    
    try {
        const response = await fetch(`/api/pharmacy/${pharmacyId}/submit-info`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showSuccessMessage('Information envoyée ! Elle sera vérifiée par notre équipe.');
        } else {
            alert(result.error || 'Erreur lors de l\'envoi');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Erreur lors de l\'envoi. Veuillez réessayer.');
    }
}

function showSuccessMessage(message) {
    const content = document.getElementById('modalContent');
    const title = document.getElementById('modalTitle');
    
    title.textContent = 'Merci !';
    
    content.innerHTML = '';
    const container = document.createElement('div');
    container.className = 'space-y-4 text-center';
    container.innerHTML = `
        <div class="w-20 h-20 bg-emerald-100 rounded-full flex items-center justify-center mx-auto">
            <svg class="w-10 h-10 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
        </div>
        <p class="text-gray-700">${escapeHtml(message)}</p>
        <button class="close-btn w-full py-3 bg-emerald-600 text-white font-semibold rounded-xl hover:bg-emerald-700 transition">
            Fermer
        </button>
    `;
    
    content.appendChild(container);
    container.querySelector('.close-btn').addEventListener('click', closeModal);
}

function resetSuggestionForm() {
    const form = document.getElementById('suggestionForm');
    if (form) {
        form.reset();
        form.classList.remove('hidden');
    }
    const success = document.getElementById('suggestionSuccess');
    if (success) {
        success.classList.add('hidden');
    }
    updateSuggestionForm();
}

function updateSuggestionForm() {
    const category = document.getElementById('suggestionCategory');
    const standardFields = document.getElementById('standardFields');
    const pharmacyFields = document.getElementById('pharmacyFields');
    const submitBtnText = document.getElementById('submitBtnText');
    
    if (!category) return;
    
    if (category.value === 'pharmacie') {
        if (standardFields) standardFields.classList.add('hidden');
        if (pharmacyFields) pharmacyFields.classList.remove('hidden');
        if (submitBtnText) submitBtnText.textContent = 'Proposer cette pharmacie';
    } else {
        if (standardFields) standardFields.classList.remove('hidden');
        if (pharmacyFields) pharmacyFields.classList.add('hidden');
        if (submitBtnText) submitBtnText.textContent = 'Envoyer ma suggestion';
    }
}

async function submitSuggestion(e) {
    e.preventDefault();
    
    const category = document.getElementById('suggestionCategory').value;
    const name = document.getElementById('suggestionName').value;
    const phone = document.getElementById('suggestionPhone').value;
    const email = document.getElementById('suggestionEmail').value;
    
    if (!category) {
        alert('Veuillez sélectionner une catégorie');
        return;
    }
    
    try {
        let response;
        
        if (category === 'pharmacie') {
            const nom = document.getElementById('pharmacyNom').value;
            const ville = document.getElementById('pharmacyVille').value;
            
            if (!nom || !ville) {
                alert('Le nom et la ville sont obligatoires');
                return;
            }
            
            const latValue = document.getElementById('pharmacyLat').value;
            const lngValue = document.getElementById('pharmacyLng').value;
            
            const data = {
                nom,
                ville,
                quartier: document.getElementById('pharmacyQuartier').value,
                telephone: document.getElementById('pharmacyTelephone').value,
                bp: document.getElementById('pharmacyBP').value,
                horaires: document.getElementById('pharmacyHoraires').value,
                services: document.getElementById('pharmacyServices').value,
                proprietaire: document.getElementById('pharmacyProprietaire').value,
                type_etablissement: document.getElementById('pharmacyType').value,
                categorie: document.getElementById('pharmacyCategorie').value,
                is_garde: document.getElementById('pharmacyIsGarde').checked,
                comment: document.getElementById('pharmacyComment').value,
                latitude: latValue ? parseFloat(latValue) : null,
                longitude: lngValue ? parseFloat(lngValue) : null,
                name,
                phone,
                email
            };
            
            response = await fetch('/api/pharmacy-proposal', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        } else {
            const subject = document.getElementById('suggestionSubject').value;
            const message = document.getElementById('suggestionMessage').value;
            
            if (!subject || !message) {
                alert('Veuillez remplir tous les champs obligatoires');
                return;
            }
            
            response = await fetch('/api/suggestions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ category, subject, message, name, phone, email })
            });
        }
        
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('suggestionForm').classList.add('hidden');
            document.getElementById('suggestionSuccess').classList.remove('hidden');
        } else {
            alert(result.error || 'Une erreur est survenue');
        }
    } catch (error) {
        console.error('Error submitting suggestion:', error);
        alert('Erreur de connexion. Veuillez réessayer.');
    }
}

function getPharmacyLocation() {
    const btn = document.getElementById('getLocationBtn');
    const btnText = document.getElementById('getLocationBtnText');
    const latInput = document.getElementById('pharmacyLat');
    const lngInput = document.getElementById('pharmacyLng');
    const statusEl = document.getElementById('locationStatus');
    
    if (!navigator.geolocation) {
        alert('La géolocalisation n\'est pas supportée par votre navigateur');
        return;
    }
    
    btn.disabled = true;
    btnText.textContent = 'Récupération en cours...';
    btn.classList.add('opacity-75');
    
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            
            latInput.value = lat.toFixed(6);
            lngInput.value = lng.toFixed(6);
            
            statusEl.textContent = 'Position récupérée avec succès !';
            statusEl.classList.remove('hidden', 'text-red-600');
            statusEl.classList.add('text-green-600');
            
            btn.disabled = false;
            btnText.textContent = 'Récupérer ma position actuelle';
            btn.classList.remove('opacity-75');
        },
        (error) => {
            let message = 'Impossible d\'obtenir votre position';
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    message = 'Vous avez refusé l\'accès à votre position. Saisissez les coordonnées manuellement.';
                    break;
                case error.POSITION_UNAVAILABLE:
                    message = 'Position indisponible. Saisissez les coordonnées manuellement.';
                    break;
                case error.TIMEOUT:
                    message = 'Délai d\'attente dépassé. Réessayez ou saisissez manuellement.';
                    break;
            }
            
            statusEl.textContent = message;
            statusEl.classList.remove('hidden', 'text-green-600');
            statusEl.classList.add('text-red-600');
            
            btn.disabled = false;
            btnText.textContent = 'Réessayer';
            btn.classList.remove('opacity-75');
        },
        { enableHighAccuracy: true, timeout: 15000 }
    );
}

function selectCity(cityName) {
    const latInput = document.getElementById('pharmacyLat');
    const lngInput = document.getElementById('pharmacyLng');
    const statusEl = document.getElementById('locationStatus');
    
    if (!cityName || !CITY_CENTERS[cityName]) {
        return;
    }
    
    const coords = CITY_CENTERS[cityName];
    latInput.value = coords[0].toFixed(6);
    lngInput.value = coords[1].toFixed(6);
    
    statusEl.textContent = 'Coordonnees du centre-ville de ' + cityName + ' appliquees';
    statusEl.classList.remove('hidden', 'text-red-600');
    statusEl.classList.add('text-green-600');
}

// Expose to global scope
window.showComplementInfo = showComplementInfo;
window.showLocationForm = showLocationForm;
window.showInfoForm = showInfoForm;
window.submitLocation = submitLocation;
window.submitInfo = submitInfo;
window.submitSuggestion = submitSuggestion;
window.updateSuggestionForm = updateSuggestionForm;
window.resetSuggestionForm = resetSuggestionForm;
window.getPharmacyLocation = getPharmacyLocation;
window.selectCity = selectCity;
