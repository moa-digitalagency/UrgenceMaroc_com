/**
 * UrgenceMaroc.com
 * By MOA Digital Agency LLC
 * Developed by: Aisance KALONJI
 * Contact: moa@myoneart.com
 * Website: www.myoneart.com
 *
 * static/js/ads.js - Système publicitaire
 * Ce fichier gère le système de publicités: déclenchement par temps/pages,
 * affichage des pubs (image/vidéo), compteurs et cooldowns.
 */

let adSettings = null;
let adState = {
    adsShown: parseInt(sessionStorage.getItem('adAdsShown') || '0'),
    pageChanges: parseInt(sessionStorage.getItem('adPageChanges') || '0'),
    refreshCount: parseInt(sessionStorage.getItem('adRefreshCount') || '0'),
    lastAdTime: parseInt(sessionStorage.getItem('adLastAdTime') || '0'),
    cooldownUntil: parseInt(sessionStorage.getItem('adCooldownUntil') || '0'),
    currentAdId: null,
    countdownTimer: null,
    timeTimer: null
};

function saveAdState() {
    sessionStorage.setItem('adAdsShown', adState.adsShown.toString());
    sessionStorage.setItem('adPageChanges', adState.pageChanges.toString());
    sessionStorage.setItem('adRefreshCount', adState.refreshCount.toString());
    sessionStorage.setItem('adLastAdTime', adState.lastAdTime.toString());
    sessionStorage.setItem('adCooldownUntil', adState.cooldownUntil.toString());
}

async function initAdSystem() {
    try {
        const response = await fetch('/api/ads/settings');
        adSettings = await response.json();
        
        if (!adSettings.ads_enabled) return;
        
        const isMobile = window.innerWidth < 768;
        if (isMobile && !adSettings.show_on_mobile) return;
        if (!isMobile && !adSettings.show_on_desktop) return;
        
        if (adSettings.trigger_type === 'refresh' || adSettings.trigger_type === 'combined') {
            adState.refreshCount++;
            sessionStorage.setItem('adRefreshCount', adState.refreshCount.toString());
            
            if (adSettings.refresh_show && adState.refreshCount >= adSettings.refresh_count) {
                adState.refreshCount = 0;
                saveAdState();
                setTimeout(() => showRandomAd(), 1000);
                return;
            }
        }
        
        saveAdState();
        
        if (adSettings.trigger_type === 'time' || adSettings.trigger_type === 'combined') {
            adState.timeTimer = setTimeout(() => {
                showRandomAd();
                if (adSettings.time_repeat) {
                    startAdInterval();
                }
            }, adSettings.time_delay * 1000);
        }
        
    } catch (error) {
        console.log('Ad system not available');
    }
}

function startAdInterval() {
    if (adState.timeTimer) clearInterval(adState.timeTimer);
    adState.timeTimer = setInterval(() => {
        if (canShowAd()) {
            showRandomAd();
        }
    }, adSettings.time_interval * 1000);
}

function canShowAd() {
    if (!adSettings || !adSettings.ads_enabled) return false;
    if (adState.adsShown >= adSettings.max_ads_per_session) return false;
    if (Date.now() < adState.cooldownUntil) return false;
    
    const adModal = document.getElementById('adModal');
    if (adModal && adModal.classList.contains('flex')) return false;
    
    return true;
}

function trackPageChange() {
    if (!adSettings) return;
    if (adSettings.trigger_type !== 'page' && adSettings.trigger_type !== 'combined') return;
    
    adState.pageChanges++;
    
    if (adState.pageChanges >= adSettings.page_count && canShowAd()) {
        adState.pageChanges = 0;
        saveAdState();
        showRandomAd();
    } else {
        saveAdState();
    }
}

async function showRandomAd() {
    if (!canShowAd()) return;
    
    try {
        const response = await fetch('/api/ads/random');
        const ad = await response.json();
        
        if (!ad) return;
        
        adState.currentAdId = ad.id;
        displayAd(ad);
        
        fetch(`/api/ads/${ad.id}/view`, { method: 'POST' })
            .catch(err => console.log('Failed to record ad view'));
        
    } catch (error) {
        console.log('Failed to load ad');
    }
}

function displayAd(ad) {
    const modal = document.getElementById('adModal');
    const mediaContainer = document.getElementById('adMediaContainer');
    const title = document.getElementById('adTitle');
    const description = document.getElementById('adDescription');
    const ctaBtn = document.getElementById('adCtaBtn');
    const skipBtn = document.getElementById('adSkipBtn');
    const countdown = document.getElementById('adCountdown');
    
    title.textContent = ad.title;
    description.textContent = ad.description || '';
    ctaBtn.textContent = ad.cta_text || 'En savoir plus';
    ctaBtn.href = ad.cta_url || '#';
    
    if (!ad.cta_url) {
        ctaBtn.classList.add('hidden');
    } else {
        ctaBtn.classList.remove('hidden');
    }
    
    mediaContainer.innerHTML = '';
    if (ad.media_type === 'image' && ad.image_url) {
        const img = document.createElement('img');
        img.src = ad.image_url;
        img.alt = ad.title;
        img.className = 'w-full h-48 object-cover';
        mediaContainer.appendChild(img);
    } else if (ad.media_type === 'video' && ad.video_url) {
        const embedUrl = getVideoEmbedUrl(ad.video_url);
        if (embedUrl) {
            const iframe = document.createElement('iframe');
            iframe.src = embedUrl;
            iframe.className = 'w-full h-56';
            iframe.frameBorder = '0';
            iframe.allowFullscreen = true;
            iframe.allow = 'autoplay; encrypted-media';
            mediaContainer.appendChild(iframe);
        }
    }
    
    let timeLeft = ad.skip_delay || 5;
    countdown.textContent = timeLeft;
    skipBtn.disabled = true;
    skipBtn.classList.add('cursor-not-allowed', 'bg-gray-200', 'text-gray-500');
    skipBtn.classList.remove('cursor-pointer', 'bg-gray-300', 'text-gray-700', 'hover:bg-gray-400');
    
    if (adState.countdownTimer) clearInterval(adState.countdownTimer);
    
    adState.countdownTimer = setInterval(() => {
        timeLeft--;
        countdown.textContent = timeLeft;
        
        if (timeLeft <= 0) {
            clearInterval(adState.countdownTimer);
            skipBtn.disabled = false;
            skipBtn.textContent = 'Passer la pub';
            skipBtn.classList.remove('cursor-not-allowed', 'bg-gray-200', 'text-gray-500');
            skipBtn.classList.add('cursor-pointer', 'bg-gray-300', 'text-gray-700', 'hover:bg-gray-400');
        }
    }, 1000);
    
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    adState.adsShown++;
    adState.lastAdTime = Date.now();
    saveAdState();
}

function getVideoEmbedUrl(url) {
    const ytMatch = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\s]+)/);
    if (ytMatch) {
        return `https://www.youtube.com/embed/${ytMatch[1]}?autoplay=1`;
    }
    
    if (url.includes('facebook.com')) {
        return `https://www.facebook.com/plugins/video.php?href=${encodeURIComponent(url)}&show_text=false&autoplay=true`;
    }
    
    const vimeoMatch = url.match(/vimeo\.com\/(\d+)/);
    if (vimeoMatch) {
        return `https://player.vimeo.com/video/${vimeoMatch[1]}?autoplay=1`;
    }
    
    return null;
}

function closeAdModal() {
    const modal = document.getElementById('adModal');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    
    if (adState.countdownTimer) {
        clearInterval(adState.countdownTimer);
    }
    
    if (adSettings) {
        adState.cooldownUntil = Date.now() + (adSettings.cooldown_after_skip * 1000);
        saveAdState();
    }
    
    adState.currentAdId = null;
}

function handleAdClick() {
    if (adState.currentAdId) {
        fetch(`/api/ads/${adState.currentAdId}/click`, { method: 'POST' })
            .catch(err => console.log('Failed to record ad click'));
    }
    
    if (adSettings) {
        adState.cooldownUntil = Date.now() + (adSettings.cooldown_after_click * 1000);
        saveAdState();
    }
    
    setTimeout(closeAdModal, 100);
}

// Expose to global scope
window.initAdSystem = initAdSystem;
window.showRandomAd = showRandomAd;
window.displayAd = displayAd;
window.closeAdModal = closeAdModal;
window.handleAdClick = handleAdClick;
window.trackPageChange = trackPageChange;
