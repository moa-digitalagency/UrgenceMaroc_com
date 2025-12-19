/**
 * UrgenceMaroc.com
 * By MOA Digital Agency LLC
 * Developed by: Aisance KALONJI
 * Contact: moa@myoneart.com
 * Website: www.myoneart.com
 *
 * static/js/pharmacy.js - Affichage des pharmacies
 * Ce fichier gère le rendu des cartes pharmacie, les badges de type/statut,
 * le modal de détail et les interactions utilisateur.
 */

function getTypeBadge(pharmacy) {
    const typeStyle = getTypeStyle(pharmacy);
    return `<span class="flex-shrink-0 px-2 py-1 ${typeStyle.bg} ${typeStyle.text} text-xs font-medium rounded-full">
        ${typeStyle.label}
    </span>`;
}

function getGardeBadge(pharmacy) {
    if (pharmacy.is_garde) {
        return `<span class="flex-shrink-0 px-2 py-1 bg-red-100 text-red-700 text-xs font-medium rounded-full flex items-center gap-1">
            <span class="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
            Garde
        </span>`;
    }
    return '';
}

function getCategoryBadge(pharmacy) {
    const category = pharmacy.categorie_emplacement || 'standard';
    const label = CATEGORY_LABELS[category] || 'Standard';
    return `<span class="flex-shrink-0 px-2 py-1 bg-indigo-100 text-indigo-700 text-xs font-medium rounded-full">
        ${label}
    </span>`;
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function createPharmacyCard(pharmacy) {
    const cityBadgeClass = getCityBadgeClass(pharmacy.ville);
    const typeStyle = getTypeStyle(pharmacy);
    const borderColor = pharmacy.is_garde ? 'border-l-red-500' : typeStyle.border;
    const escapedPhone = pharmacy.telephone ? escapeHtml(pharmacy.telephone) : '';
    const escapedNom = escapeHtml(pharmacy.nom);
    const escapedQuartier = escapeHtml(pharmacy.quartier);
    const escapedVille = escapeHtml(pharmacy.ville);
    
    const card = document.createElement('div');
    card.className = `pharmacy-card bg-white rounded-xl p-4 shadow-sm border-l-4 ${borderColor} border border-gray-100 active:scale-[0.98] transition cursor-pointer hover:shadow-md`;
    card.onclick = () => showPharmacyDetail(pharmacy);
    
    card.innerHTML = `
        <div class="flex items-start justify-between">
            <div class="flex-1 min-w-0">
                <h3 class="font-semibold text-gray-800 truncate">${escapedNom}</h3>
                ${escapedQuartier ? `
                    <div class="flex items-center gap-1.5 mt-0.5">
                        <span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-gray-100 text-gray-600 text-sm font-medium rounded-full">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                            </svg>
                            ${escapedQuartier}
                        </span>
                    </div>
                ` : ''}
                ${escapedPhone ? `
                    <div class="flex items-center gap-1.5 mt-1">
                        <button class="phone-btn inline-flex items-center gap-1.5 px-2.5 py-1 bg-emerald-50 text-emerald-700 text-sm font-medium rounded-full hover:bg-emerald-100 transition cursor-pointer">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                            </svg>
                            ${escapedPhone}
                        </button>
                    </div>
                ` : ''}
            </div>
        </div>
        <div class="flex flex-wrap gap-1.5 mt-3">
            ${getGardeBadge(pharmacy)}
            ${getTypeBadge(pharmacy)}
            ${getCategoryBadge(pharmacy)}
            <span class="flex-shrink-0 px-2 py-1 ${cityBadgeClass} text-xs font-medium rounded-full">
                ${escapedVille}
            </span>
            ${pharmacy.is_verified ? `
                <span class="flex-shrink-0 px-2 py-1 bg-blue-100 text-blue-700 text-xs font-medium rounded-full flex items-center gap-1">
                    <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                    Vérifié
                </span>
            ` : `
                <span class="flex-shrink-0 px-2 py-1 bg-gray-100 text-gray-500 text-xs font-medium rounded-full flex items-center gap-1">
                    <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
                    </svg>
                    Non vérifié
                </span>
            `}
        </div>
    `;
    
    const phoneBtn = card.querySelector('.phone-btn');
    if (phoneBtn && pharmacy.telephone) {
        phoneBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            handlePhoneClick(pharmacy.telephone, e);
        });
    }
    
    return card;
}

function renderPharmacyCards(container, pharmacies, emptyMessage) {
    container.innerHTML = '';
    if (pharmacies.length === 0) {
        container.innerHTML = `<p class="text-center text-gray-500 py-8">${escapeHtml(emptyMessage)}</p>`;
        return;
    }
    pharmacies.forEach(pharmacy => {
        container.appendChild(createPharmacyCard(pharmacy));
    });
}

function showPharmacyDetail(pharmacy) {
    const modal = document.getElementById('pharmacyModal');
    const title = document.getElementById('modalTitle');
    const content = document.getElementById('modalContent');
    
    title.textContent = pharmacy.nom;
    const cityBadgeClass = getCityBadgeClass(pharmacy.ville);
    
    content.innerHTML = '';
    const detailContainer = document.createElement('div');
    detailContainer.className = 'space-y-4';
    
    detailContainer.innerHTML = buildPharmacyDetailHTML(pharmacy, cityBadgeClass);
    content.appendChild(detailContainer);
    
    bindPharmacyDetailEvents(content, pharmacy);
    
    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

function buildPharmacyDetailHTML(pharmacy, cityBadgeClass) {
    const escapedVille = escapeHtml(pharmacy.ville);
    const escapedQuartier = escapeHtml(pharmacy.quartier) || 'Non spécifié';
    const escapedHoraires = escapeHtml(pharmacy.horaires);
    const escapedServices = escapeHtml(pharmacy.services);
    const escapedPhone = escapeHtml(pharmacy.telephone);
    
    return `
        <div class="flex flex-wrap gap-2">
            <span class="px-3 py-1 ${cityBadgeClass} text-sm font-medium rounded-full">
                ${escapedVille}
            </span>
            ${pharmacy.is_garde ? `
                <span class="px-3 py-1 bg-red-100 text-red-700 text-sm font-medium rounded-full">
                    Garde
                </span>
            ` : ''}
            ${pharmacy.is_verified ? `
                <span class="px-3 py-1 bg-blue-100 text-blue-700 text-sm font-medium rounded-full flex items-center gap-1">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                    Établissement vérifié
                </span>
            ` : `
                <span class="px-3 py-1 bg-gray-100 text-gray-500 text-sm font-medium rounded-full flex items-center gap-1">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
                    </svg>
                    Non vérifié
                </span>
            `}
        </div>
        
        ${pharmacy.is_garde ? `
            <div class="flex items-center gap-2 p-3 bg-red-50 rounded-xl">
                <div class="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                <span class="text-sm font-medium text-red-700">Pharmacie de garde</span>
            </div>
        ` : ''}
        
        <div class="space-y-3">
            <div class="flex items-start gap-3">
                <div class="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                    </svg>
                </div>
                <div>
                    <p class="text-sm text-gray-500">Adresse</p>
                    <p class="font-medium text-gray-800">${escapedQuartier}</p>
                    <p class="text-sm text-gray-600">${escapedVille}</p>
                </div>
            </div>
            
            ${escapedPhone ? `
                <div class="flex items-start gap-3">
                    <div class="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                        </svg>
                    </div>
                    <div>
                        <p class="text-sm text-gray-500">Téléphone</p>
                        <button class="detail-phone-btn font-medium text-emerald-600 hover:underline cursor-pointer">${escapedPhone}</button>
                    </div>
                </div>
            ` : ''}
            
            ${escapedHoraires ? `
                <div class="flex items-start gap-3">
                    <div class="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                    </div>
                    <div>
                        <p class="text-sm text-gray-500">Horaires</p>
                        <p class="font-medium text-gray-800">${escapedHoraires}</p>
                    </div>
                </div>
            ` : ''}
            
            ${escapedServices ? `
                <div class="flex items-start gap-3">
                    <div class="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                        </svg>
                    </div>
                    <div>
                        <p class="text-sm text-gray-500">Services</p>
                        <p class="text-sm text-gray-800">${escapedServices}</p>
                    </div>
                </div>
            ` : ''}
        </div>
        
        <div class="flex flex-col gap-2 mt-4">
            ${pharmacy.telephone ? `
                <button class="call-btn w-full py-3 bg-emerald-600 text-white font-semibold rounded-xl flex items-center justify-center gap-2 hover:bg-emerald-700 transition">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                    </svg>
                    Appeler
                </button>
            ` : ''}
            
            <button class="locate-btn w-full py-3 bg-blue-600 text-white font-semibold rounded-xl flex items-center justify-center gap-2 hover:bg-blue-700 transition">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                Localiser
            </button>
            
            ${pharmacy.location_validated && pharmacy.lat !== null && pharmacy.lat !== undefined && pharmacy.lng !== null && pharmacy.lng !== undefined ? `
                <a href="https://www.google.com/maps/dir/?api=1&destination=${pharmacy.lat},${pharmacy.lng}" 
                   target="_blank"
                   class="w-full py-3 bg-purple-600 text-white font-semibold rounded-xl flex items-center justify-center gap-2 hover:bg-purple-700 transition">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/>
                    </svg>
                    Se rendre
                </a>
            ` : `
                <button disabled
                   class="w-full py-3 bg-gray-300 text-gray-500 font-semibold rounded-xl flex items-center justify-center gap-2 cursor-not-allowed">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/>
                    </svg>
                    Se rendre (non validée)
                </button>
            `}
            
            <button class="complement-btn w-full py-3 bg-amber-500 text-white font-semibold rounded-xl flex items-center justify-center gap-2 hover:bg-amber-600 transition">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
                Compléter Info
            </button>
        </div>
    `;
}

function bindPharmacyDetailEvents(content, pharmacy) {
    const phoneBtn = content.querySelector('.detail-phone-btn');
    if (phoneBtn && pharmacy.telephone) {
        phoneBtn.addEventListener('click', (e) => handlePhoneClick(pharmacy.telephone, e));
    }
    
    const callBtn = content.querySelector('.call-btn');
    if (callBtn && pharmacy.telephone) {
        callBtn.addEventListener('click', (e) => handlePhoneClick(pharmacy.telephone, e));
    }
    
    const locateBtn = content.querySelector('.locate-btn');
    if (locateBtn) {
        locateBtn.addEventListener('click', () => {
            showLocationForm(pharmacy.id);
        });
    }
    
    const complementBtn = content.querySelector('.complement-btn');
    if (complementBtn) {
        complementBtn.addEventListener('click', () => showComplementInfo(pharmacy.id));
    }
}

function closeModal() {
    const modal = document.getElementById('pharmacyModal');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
}

// Expose to global scope
window.escapeHtml = escapeHtml;
window.createPharmacyCard = createPharmacyCard;
window.renderPharmacyCards = renderPharmacyCards;
window.showPharmacyDetail = showPharmacyDetail;
window.closeModal = closeModal;
