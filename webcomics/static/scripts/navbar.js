window.addEventListener("scroll", function(){
    var header = document.querySelector("header");
    if (!header.classList.contains("static")) {
        header.classList.toggle("sticky", window.scrollY > 0);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const currentUrl = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        const linkPath = new URL(link.href).pathname;

    if (linkPath === currentUrl) {
        link.classList.add('active'); // Agregar clase 'active' al enlace correspondiente
    }
  });
});
