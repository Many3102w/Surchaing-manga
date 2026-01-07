const VAPID_PUBLIC_KEY = 'BONRvVIGC-QcB7-4S_zilZVHZKje8aOgxEOJLvQI2WBkg7hCGu5tgY8hlXDMUh2-K4d3wUCAUB9eOhiq0s3_oyw';

// Helper to convert key
function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

async function registerServiceWorker() {
    if ('serviceWorker' in navigator && 'PushManager' in window) {
        try {
            const registration = await navigator.serviceWorker.register('/static/sw.js');
            console.log('Service Worker registered:', registration);
            return registration;
        } catch (error) {
            console.error('Service Worker registration failed:', error);
        }
    } else {
        console.warn('Push messaging is not supported');
    }
}

async function subscribeToPush() {
    const registration = await navigator.serviceWorker.ready;
    if (!registration) return;

    try {
        const subscribeOptions = {
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array(window.VAPID_PUBLIC_KEY)
        };

        const subscription = await registration.pushManager.subscribe(subscribeOptions);
        console.log('Web Push Subscribed:', subscription);

        // Send to server
        await saveSubscription(subscription);

    } catch (error) {
        console.error('Failed to subscribe the user: ', error);
    }
}

async function saveSubscription(subscription) {
    const response = await fetch('/api/save-web-push/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // Add CSRF token if needed
        },
        body: JSON.stringify(subscription)
    });
    return response.json();
}

// Auto-run if enabled button clicked or on load if desired
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('enable-notifications-btn');
    if (btn) {
        btn.addEventListener('click', () => {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    registerServiceWorker().then(() => subscribeToPush());
                }
            });
        });
    }
});
