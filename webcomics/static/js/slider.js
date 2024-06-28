document.querySelectorAll('.manga-container').forEach(container => {
    const nextButton = container.querySelector('.next');
    const prevButton = container.querySelector('.prev');
    const slide = container.querySelector('.slide');

    nextButton.addEventListener('click', () => {
        const items = slide.querySelectorAll('.manga-item');
        slide.appendChild(items[0]);
    });

    prevButton.addEventListener('click', () => {
        const items = slide.querySelectorAll('.manga-item');
        slide.prepend(items[items.length - 1]);
    });

    slide.querySelectorAll('.manga-item').forEach(item => {
        item.addEventListener('transitionstart', () => {
            item.classList.add('active');
        });

        item.addEventListener('transitionend', () => {
            item.classList.remove('active');
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    let currentHeroSlide = 0;

    function moveHeroSlide(direction) {
        const heroSlides = document.querySelectorAll('.slider-section');
        const totalHeroSlides = heroSlides.length;
        currentHeroSlide = (currentHeroSlide + direction + totalHeroSlides) % totalHeroSlides;
        document.querySelector('.hero-slider').style.transform = `translateX(-${currentHeroSlide * 100}%)`;
    }

    if (window.innerWidth > 600) { // Solo en dispositivos que no sean móviles
        document.querySelector('.hero-slider-button.left').addEventListener('click', () => {
            moveHeroSlide(-1);
        });

        document.querySelector('.hero-slider-button.right').addEventListener('click', () => {
            moveHeroSlide(1);
        });
    } else {
        // Desactivar transformaciones en móviles
        document.querySelector('.hero-slider').style.transform = 'none';
    }
});

