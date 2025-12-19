/**
 * UrgenceMaroc.com
 * By MOA Digital Agency LLC
 * Developed by: Aisance KALONJI
 * Contact: moa@myoneart.com
 * Website: www.myoneart.com
 *
 * static/js/app.js - Application principale
 * Ce fichier gère la logique principale: navigation par onglets, filtrage par ville,
 * recherche de pharmacies et initialisation de l'application.
 */

window.pharmacies = [];
window.currentTab = 'pharmacies';
window.currentCity = '';
window.currentGardeCity = '';
let debounceTimer;

function debounce(func, delay) {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(func, delay);
}

function switchTab(tab) {
    window.currentTab = tab;
    
    document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
    const tabEl = document.getElementById(`tab-${tab}`);
    if (tabEl) tabEl.classList.remove('hidden');
    
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('border-primary-600', 'text-primary-600');
        btn.classList.add('border-transparent', 'text-gray-500');
    });
    document.querySelectorAll(`.tab-btn[data-tab="${tab}"]`).forEach(btn => {
        btn.classList.add('border-primary-600', 'text-primary-600');
        btn.classList.remove('border-transparent', 'text-gray-500');
    });
    
    document.querySelectorAll('.mobile-tab-btn').forEach(btn => {
        btn.classList.remove('active', 'text-emerald-600');
        btn.classList.add('text-gray-400');
    });
    document.querySelectorAll(`.mobile-tab-btn[data-tab="${tab}"]`).forEach(btn => {
        btn.classList.add('active', 'text-emerald-600');
        btn.classList.remove('text-gray-400');
    });
    
    const searchSection = document.getElementById('searchSection');
    if (searchSection) {
        searchSection.style.display = tab === 'pharmacies' ? 'block' : 'none';
    }
    
    const gpsBtn = document.getElementById('gpsLocateBtn');
    if (gpsBtn) {
        if (tab === 'garde' || tab === 'map') {
            gpsBtn.classList.remove('hidden');
            gpsBtn.classList.add('flex');
        } else {
            gpsBtn.classList.add('hidden');
            gpsBtn.classList.remove('flex');
        }
    }
    
    if (tab === 'map') {
        setTimeout(() => {
            initMap();
            if (window.map) window.map.invalidateSize();
            displayOnMap(window.pharmacies);
        }, 100);
    }
    
    if (tab === 'garde') {
        fetchPharmacies(true);
    } else if (tab === 'pharmacies') {
        fetchPharmacies(false);
    }
    
    trackPageChange();
}

function filterByCity(city) {
    window.currentCity = city;
    
    document.querySelectorAll('.city-filter').forEach(btn => {
        if (btn.dataset.city === city) {
            btn.classList.add('bg-white', 'text-primary-700');
            btn.classList.remove('bg-white/10', 'text-white');
        } else {
            btn.classList.remove('bg-white', 'text-primary-700');
            btn.classList.add('bg-white/10', 'text-white');
        }
    });
    
    fetchPharmacies(window.currentTab === 'garde');
    
    if (city && CITY_CENTERS[city] && window.map) {
        window.map.setView(CITY_CENTERS[city], 13);
    }
}

function filterGardeByCity(city) {
    window.currentGardeCity = city;
    fetchGardePharmacies();
}

async function fetchGardePharmacies() {
    const params = new URLSearchParams();
    if (window.currentGardeCity) params.append('ville', window.currentGardeCity);
    params.append('garde', 'true');
    
    try {
        const response = await fetch(`/api/pharmacies?${params}`);
        const data = await response.json();
        
        const countEl = document.getElementById('countGarde');
        if (countEl) countEl.textContent = `(${data.length})`;
        
        const listEl = document.getElementById('gardeList');
        if (listEl) {
            renderPharmacyCards(listEl, data, 'Aucune pharmacie de garde trouvée');
        }
    } catch (error) {
        console.error('Error fetching garde pharmacies:', error);
    }
}

async function fetchPharmacies(gardeOnly = false) {
    const searchInput = document.getElementById('searchInput');
    const search = searchInput ? searchInput.value : '';
    
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (window.currentCity) params.append('ville', window.currentCity);
    if (gardeOnly) params.append('garde', 'true');
    
    try {
        const response = await fetch(`/api/pharmacies?${params}`);
        const data = await response.json();
        window.pharmacies = data;
        
        if (gardeOnly) {
            const countEl = document.getElementById('countGarde');
            if (countEl) countEl.textContent = `(${data.length})`;
            
            const listEl = document.getElementById('gardeList');
            if (listEl) {
                renderPharmacyCards(listEl, data, 'Aucune pharmacie de garde trouvée');
            }
        } else {
            const countEl = document.getElementById('countAll');
            if (countEl) countEl.textContent = `(${data.length})`;
            
            const listEl = document.getElementById('pharmacyList');
            if (listEl) {
                renderPharmacyCards(listEl, data, 'Aucune pharmacie trouvée');
            }
        }
        
        if (window.currentTab === 'map') {
            displayOnMap(data);
        }
    } catch (error) {
        console.error('Error fetching pharmacies:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchPharmacies();
    loadActivePopups();
    initAdSystem();
    
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            debounce(() => fetchPharmacies(window.currentTab === 'garde'), 300);
        });
    }
    
    const pharmacyModal = document.getElementById('pharmacyModal');
    if (pharmacyModal) {
        pharmacyModal.addEventListener('click', (e) => {
            if (e.target === e.currentTarget) {
                closeModal();
            }
        });
    }
    
    const suggestionForm = document.getElementById('suggestionForm');
    if (suggestionForm) {
        suggestionForm.addEventListener('submit', submitSuggestion);
    }
    
    const suggestionCategory = document.getElementById('suggestionCategory');
    if (suggestionCategory) {
        suggestionCategory.addEventListener('change', updateSuggestionForm);
    }
});

// Expose to global scope
window.switchTab = switchTab;
window.filterByCity = filterByCity;
window.filterGardeByCity = filterGardeByCity;
window.fetchPharmacies = fetchPharmacies;
window.fetchGardePharmacies = fetchGardePharmacies;
