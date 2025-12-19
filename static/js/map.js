/**
 * UrgenceMaroc.com
 * By MOA Digital Agency LLC
 * Developed by: Aisance KALONJI
 * Contact: moa@myoneart.com
 * Website: www.myoneart.com
 *
 * static/js/map.js - Carte interactive Leaflet
 * Ce fichier gère la carte: initialisation, markers colorés par type,
 * géolocalisation et affichage des pharmacies les plus proches.
 */

window.map = null;
window.markers = [];

function initMap() {
    if (window.map) return;
    window.map = L.map('map').setView([0.4162, 9.4673], 7);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(window.map);
}

function getMarkerColor(pharmacy) {
    if (pharmacy.is_garde) return '#ef4444';
    if (pharmacy.categorie_emplacement === 'gare') return '#3b82f6';
    if (pharmacy.type_etablissement && pharmacy.type_etablissement.toLowerCase().includes('dépôt')) return '#f97316';
    return '#10b981';
}

function createMarkerIcon(color) {
    return L.divIcon({
        className: 'custom-marker',
        html: `<div style="
            background-color: ${color};
            width: 32px;
            height: 32px;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="white">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v4h4v2h-4v4h-2v-4H7v-2h4V7z"/>
            </svg>
        </div>`,
        iconSize: [32, 32],
        iconAnchor: [16, 16],
        popupAnchor: [0, -16]
    });
}

function createUserMarkerIcon(size = 24) {
    return L.divIcon({
        className: 'user-marker',
        html: `<div style="
            background-color: #3b82f6;
            width: ${size}px;
            height: ${size}px;
            border-radius: 50%;
            border: ${size > 20 ? 4 : 3}px solid white;
            box-shadow: 0 2px ${size > 20 ? 10 : 8}px rgba(${size > 20 ? '59, 130, 246, 0.5' : '0,0,0,0.3'});
        "></div>`,
        iconSize: [size, size],
        iconAnchor: [size / 2, size / 2]
    });
}

function clearMarkers() {
    window.markers.forEach(marker => window.map.removeLayer(marker));
    window.markers = [];
}

function displayOnMap(data) {
    if (!window.map) initMap();
    clearMarkers();
    
    data.forEach(pharmacy => {
        if (pharmacy.lat === null || pharmacy.lat === undefined || pharmacy.lng === null || pharmacy.lng === undefined) return;
        
        const color = getMarkerColor(pharmacy);
        const icon = createMarkerIcon(color);
        
        const marker = L.marker([pharmacy.lat, pharmacy.lng], { icon })
            .addTo(window.map);
        
        marker.on('click', function() {
            showPharmacyDetail(pharmacy);
        });
        
        window.markers.push(marker);
    });
    
    if (data.length > 0) {
        const validData = data.filter(p => p.lat !== null && p.lat !== undefined && p.lng !== null && p.lng !== undefined);
        if (validData.length > 0) {
            const bounds = L.latLngBounds(validData.map(p => [p.lat, p.lng]));
            window.map.fitBounds(bounds, { padding: [30, 30] });
        }
    }
}

function showNearestPharmaciesOnMap(userLat, userLng, pharmacyList, title) {
    switchTab('map');
    
    setTimeout(() => {
        if (!window.map) initMap();
        clearMarkers();
        
        const userMarker = L.marker([userLat, userLng], {
            icon: createUserMarkerIcon(24)
        }).addTo(window.map).bindPopup('<b>Votre position</b>');
        window.markers.push(userMarker);
        
        const sortedPharmacies = pharmacyList.map(p => ({
            ...p,
            distance: Math.sqrt(Math.pow(p.lat - userLat, 2) + Math.pow(p.lng - userLng, 2))
        })).sort((a, b) => a.distance - b.distance);
        
        sortedPharmacies.forEach((pharmacy, index) => {
            const color = '#ef4444';
            const icon = createMarkerIcon(color);
            
            const marker = L.marker([pharmacy.lat, pharmacy.lng], { icon })
                .addTo(window.map);
            
            marker.on('click', function() {
                showPharmacyDetail(pharmacy);
            });
            
            window.markers.push(marker);
            
            if (index === 0) {
                showPharmacyDetail(pharmacy);
            }
        });
        
        const allPoints = [[userLat, userLng], ...sortedPharmacies.map(p => [p.lat, p.lng])];
        const bounds = L.latLngBounds(allPoints);
        window.map.fitBounds(bounds, { padding: [50, 50] });
        
    }, 200);
}

function locatePharmacy(pharmacyId, lat, lng) {
    if (!navigator.geolocation) {
        alert('La géolocalisation n\'est pas supportée par votre navigateur');
        return;
    }
    
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const userLat = position.coords.latitude;
            const userLng = position.coords.longitude;
            
            if (lat !== null && lat !== undefined && lng !== null && lng !== undefined) {
                switchTab('map');
                setTimeout(() => {
                    if (window.map) {
                        const bounds = L.latLngBounds([[userLat, userLng], [lat, lng]]);
                        window.map.fitBounds(bounds, { padding: [50, 50] });
                        
                        L.marker([userLat, userLng], {
                            icon: createUserMarkerIcon(20)
                        }).addTo(window.map).bindPopup('Votre position').openPopup();
                    }
                }, 200);
            } else {
                alert('Les coordonnées de cette pharmacie ne sont pas disponibles');
            }
        },
        (error) => {
            handleGeolocationError(error);
        }
    );
}

function locateNearestGardePharmacy() {
    const btn = document.getElementById('gpsLocateBtn');
    const originalIcon = '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>';
    btn.innerHTML = '<svg class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>';
    
    if (!navigator.geolocation) {
        alert('La géolocalisation n\'est pas supportée par votre navigateur');
        btn.innerHTML = originalIcon;
        return;
    }
    
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const userLat = position.coords.latitude;
            const userLng = position.coords.longitude;
            
            let nearestCity = '';
            let minDistance = Infinity;
            
            for (const [city, coords] of Object.entries(CITY_CENTERS)) {
                const distance = Math.sqrt(Math.pow(coords[0] - userLat, 2) + Math.pow(coords[1] - userLng, 2));
                if (distance < minDistance) {
                    minDistance = distance;
                    nearestCity = city;
                }
            }
            
            if (currentTab === 'garde') {
                currentCity = nearestCity;
                document.querySelectorAll('.city-filter').forEach(btn => {
                    if (btn.dataset.city === nearestCity) {
                        btn.classList.add('bg-white', 'text-primary-700');
                        btn.classList.remove('bg-white/10', 'text-white');
                    } else {
                        btn.classList.remove('bg-white', 'text-primary-700');
                        btn.classList.add('bg-white/10', 'text-white');
                    }
                });
                fetchPharmacies(true);
                btn.innerHTML = originalIcon;
            } else {
                const gardeInCity = pharmacies.filter(p => p.is_garde && p.ville === nearestCity && p.lat !== null && p.lng !== null);
                
                if (gardeInCity.length === 0) {
                    const allGarde = pharmacies.filter(p => p.is_garde && p.lat !== null && p.lng !== null);
                    if (allGarde.length === 0) {
                        alert('Aucune pharmacie de garde trouvée');
                        btn.innerHTML = originalIcon;
                        return;
                    }
                    showNearestPharmaciesOnMap(userLat, userLng, allGarde, 'Garde les plus proches');
                } else {
                    showNearestPharmaciesOnMap(userLat, userLng, gardeInCity, `Garde à ${nearestCity}`);
                }
                btn.innerHTML = originalIcon;
            }
        },
        (error) => {
            handleGeolocationError(error);
            btn.innerHTML = originalIcon;
        },
        { enableHighAccuracy: true, timeout: 10000 }
    );
}

function handleGeolocationError(error) {
    let message = 'Impossible d\'obtenir votre position';
    switch(error.code) {
        case error.PERMISSION_DENIED:
            message = 'Vous avez refusé l\'accès à votre position';
            break;
        case error.POSITION_UNAVAILABLE:
            message = 'Position indisponible';
            break;
        case error.TIMEOUT:
            message = 'Délai d\'attente dépassé';
            break;
    }
    alert(message);
}

// Expose to global scope
window.initMap = initMap;
window.displayOnMap = displayOnMap;
window.locatePharmacy = locatePharmacy;
window.locateNearestGardePharmacy = locateNearestGardePharmacy;
window.showNearestPharmaciesOnMap = showNearestPharmaciesOnMap;
window.handleGeolocationError = handleGeolocationError;
window.clearMarkers = clearMarkers;
