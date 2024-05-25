document.addEventListener('DOMContentLoaded', function() {
    const loadingScreen = document.getElementById('loading-screen');
    const wrapper = document.getElementById('wrapper');
    
    window.addEventListener('load', function() {
        wrapper.style.display = 'block';

        loadingScreen.classList.add('fade-out');

        loadingScreen.addEventListener('transitionend', function() {
            loadingScreen.style.display = 'none';
        });
    });
});

