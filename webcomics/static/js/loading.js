window.addEventListener('load', function() {
    const loadingScreen = document.getElementById('loading-screen');
    const wrapper = document.getElementById('wrapper');
    const body = document.body;    
    if (loadingScreen && wrapper) {
        // Muestra el contenido de la página
        body.style.overflow = 'hidden';
        wrapper.style.display = 'block';
        loadingScreen.classList.add('fade-out');

        // Espera a que termine la transición antes de ocultar completamente la pantalla de carga
        loadingScreen.addEventListener('transitionend', function() {
            loadingScreen.style.display = 'none';
            body.style.overflow = 'auto';
        });
    } else {
        console.error('No se encontró el elemento con ID "loading-screen" o "content".');
    }
});
