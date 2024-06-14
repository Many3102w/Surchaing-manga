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
