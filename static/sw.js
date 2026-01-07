self.addEventListener('push', function (event) {
    let data = {};
    if (event.data) {
        data = event.data.json();
    }

    const title = data.title || 'Nueva Notificación';
    const options = {
        body: data.body || 'Tienes un nuevo mensaje.',
        icon: '/static/img/logo.png', // Adjust path if needed
        badge: '/static/img/badge.png', // Optional
        data: {
            url: data.url || '/'
        }
    };

    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

self.addEventListener('notificationclick', function (event) {
    event.notification.close();
    event.waitUntil(
        clients.openWindow(event.notification.data.url)
    );
});
