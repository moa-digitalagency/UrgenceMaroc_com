/**
 * UrgenceMaroc.com
 * By MOA Digital Agency LLC
 * Developed by: Aisance KALONJI
 * Contact: moa@myoneart.com
 * Website: www.myoneart.com
 *
 * static/js/popups.js - Popups et modales
 * Ce fichier gère les popups: sélection de numéro de téléphone,
 * messages de bienvenue et notifications.
 */

function handlePhoneClick(phoneString, event) {
    if (event) {
        event.stopPropagation();
        event.preventDefault();
    }
    
    const numbers = phoneString.split(/[\/\-]/).map(n => n.trim()).filter(n => n.length > 0);
    
    if (numbers.length === 1) {
        const cleanNumber = numbers[0].replace(/\s/g, '');
        window.location.href = 'tel:' + cleanNumber;
    } else {
        showPhonePopup(numbers);
    }
}

function showPhonePopup(numbers) {
    const overlay = document.createElement('div');
    overlay.id = 'phonePopup';
    overlay.className = 'fixed inset-0 bg-black/50 z-[2000] flex items-center justify-center p-4';
    overlay.onclick = function(e) {
        if (e.target === overlay) closePhonePopup();
    };
    
    const content = document.createElement('div');
    content.className = 'bg-white rounded-2xl w-full max-w-sm shadow-xl';
    
    const header = document.createElement('div');
    header.className = 'p-4 border-b flex items-center justify-between';
    
    const title = document.createElement('h3');
    title.className = 'text-lg font-semibold text-gray-800';
    title.textContent = 'Choisir un numéro';
    
    const closeBtn = document.createElement('button');
    closeBtn.className = 'p-2 hover:bg-gray-100 rounded-lg';
    closeBtn.innerHTML = `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
    </svg>`;
    closeBtn.onclick = closePhonePopup;
    
    header.appendChild(title);
    header.appendChild(closeBtn);
    
    const buttonsContainer = document.createElement('div');
    buttonsContainer.className = 'p-4 space-y-3';
    
    numbers.forEach(num => {
        const cleanNum = num.replace(/\s/g, '');
        const link = document.createElement('a');
        link.href = 'tel:' + cleanNum;
        link.className = 'flex items-center gap-3 p-4 bg-gray-50 rounded-xl hover:bg-emerald-50 transition border border-gray-200';
        link.onclick = closePhonePopup;
        
        link.innerHTML = `
            <div class="w-10 h-10 bg-emerald-100 rounded-full flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                </svg>
            </div>
        `;
        const numSpan = document.createElement('span');
        numSpan.className = 'text-lg font-semibold text-gray-800';
        numSpan.textContent = num;
        link.appendChild(numSpan);
        
        buttonsContainer.appendChild(link);
    });
    
    content.appendChild(header);
    content.appendChild(buttonsContainer);
    overlay.appendChild(content);
    document.body.appendChild(overlay);
}

function closePhonePopup() {
    const popup = document.getElementById('phonePopup');
    if (popup) popup.remove();
}

function loadActivePopups() {
    fetch('/api/popups')
        .then(response => response.json())
        .then(popups => {
            popups.forEach(popup => {
                const seenKey = `popup_seen_${popup.id}`;
                if (popup.show_once && localStorage.getItem(seenKey)) {
                    return;
                }
                showWelcomePopup(popup);
                if (popup.show_once) {
                    localStorage.setItem(seenKey, 'true');
                }
            });
        })
        .catch(error => console.error('Error loading popups:', error));
}

function showWelcomePopup(popup) {
    const overlay = document.createElement('div');
    overlay.id = `welcomePopup_${popup.id}`;
    overlay.className = 'fixed inset-0 bg-black/60 z-[3000] flex items-center justify-center p-4';
    overlay.onclick = function(e) {
        if (e.target === overlay) closeWelcomePopup(popup.id);
    };
    
    const container = document.createElement('div');
    container.className = 'bg-white rounded-2xl w-full max-w-md shadow-2xl overflow-hidden animate-fade-in';
    
    const headerDiv = document.createElement('div');
    headerDiv.className = 'p-6 pb-3 text-center';
    const titleEl = document.createElement('h2');
    titleEl.className = 'text-xl font-bold text-gray-800';
    titleEl.textContent = popup.title;
    headerDiv.appendChild(titleEl);
    container.appendChild(headerDiv);
    
    if (popup.image_url) {
        const imageDiv = document.createElement('div');
        imageDiv.className = 'aspect-video';
        const img = document.createElement('img');
        img.src = popup.image_url;
        img.alt = '';
        img.className = 'w-full h-full object-cover';
        imageDiv.appendChild(img);
        container.appendChild(imageDiv);
    }
    
    const bodyDiv = document.createElement('div');
    bodyDiv.className = 'p-6 text-center';
    
    if (popup.description) {
        const descP = document.createElement('p');
        descP.className = 'text-gray-600 mb-4';
        descP.textContent = popup.description;
        bodyDiv.appendChild(descP);
    }
    
    if (popup.warning_text) {
        const warningDiv = document.createElement('div');
        warningDiv.className = 'mt-4 p-4 bg-red-50 border-2 border-red-400 rounded-xl text-center';
        warningDiv.innerHTML = `
            <div class="flex flex-col items-center gap-2">
                <svg class="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>
            </div>
        `;
        const warningText = document.createElement('p');
        warningText.className = 'text-red-700 text-sm';
        warningText.textContent = popup.warning_text;
        warningDiv.querySelector('.flex').appendChild(warningText);
        bodyDiv.appendChild(warningDiv);
    }
    
    const closeButton = document.createElement('button');
    closeButton.className = 'mt-4 w-full py-3 bg-emerald-600 text-white font-semibold rounded-xl hover:bg-emerald-700 transition';
    closeButton.textContent = 'J\'ai compris';
    closeButton.onclick = () => closeWelcomePopup(popup.id);
    bodyDiv.appendChild(closeButton);
    
    container.appendChild(bodyDiv);
    overlay.appendChild(container);
    document.body.appendChild(overlay);
}

function closeWelcomePopup(popupId) {
    const popup = document.getElementById(`welcomePopup_${popupId}`);
    if (popup) popup.remove();
}

// Expose to global scope
window.handlePhoneClick = handlePhoneClick;
window.showPhonePopup = showPhonePopup;
window.closePhonePopup = closePhonePopup;
window.loadActivePopups = loadActivePopups;
window.showWelcomePopup = showWelcomePopup;
window.closeWelcomePopup = closeWelcomePopup;
