


   
function updateButtons(carousel) {
    let itemsPerSlide = 5;
    if (window.innerWidth < 1080) {
        itemsPerSlide = 2; // Для мобильных устройств
    }

    const leftButton = carousel.querySelector('.carousel-button.left');
    const rightButton = carousel.querySelector('.carousel-button.right');
    const items = carousel.querySelectorAll('.product');
    const totalItems = items.length;
    const currentIndex = parseInt(carousel.dataset.currentIndex) || 0;

    // Показываем кнопку "влево", если текущий индекс больше 0
    leftButton.style.display = currentIndex > 0 ? 'block' : 'none';

    // Показываем кнопку "вправо", если текущий индекс меньше, чем последний набор карточек
    rightButton.style.display = currentIndex < totalItems - itemsPerSlide ? 'block' : 'none';
}

function moveSlide(event, direction) {
    const carousel = event.target.closest('.products-block'); // Находим родительский элемент карусели
    let currentIndex = parseInt(carousel.dataset.currentIndex) || 0; // Получаем текущий индекс

    // Динамически меняем количество карточек на слайде в зависимости от ширины экрана
    let itemsPerSlide = 5;
    if (window.innerWidth < 1080) {
        itemsPerSlide = 2;
    }

    // Обновляем текущий индекс
    currentIndex += direction;

    // Получаем все продукты в карусели
    const items = carousel.querySelectorAll('.product');
    const totalItems = items.length;

    // Проверяем границы
    if (currentIndex < 0) {
        currentIndex = 0; // Не позволяем уходить за пределы влево
    } else if (currentIndex > totalItems - itemsPerSlide) {
        currentIndex = totalItems - itemsPerSlide; // Не позволяем уходить за пределы вправо
    }

    // Перемещаем слайды
    const offset = -currentIndex * (100 / itemsPerSlide); // Рассчитываем смещение
    carousel.querySelector('.product-cards-inner').style.transform = `translateX(${offset}%)`;

    // Обновляем видимость кнопок
    carousel.dataset.currentIndex = currentIndex; // Сохраняем текущий индекс
    updateButtons(carousel);
}

// Инициализация видимости кнопок при загрузке страницы
document.querySelectorAll('.products-block').forEach(carousel => {
    carousel.dataset.currentIndex = 0; // Инициализируем текущий индекс для каждой карусели
    updateButtons(carousel);
});

// Обработка изменения размера окна
window.addEventListener('resize', () => {
    document.querySelectorAll('.products-block').forEach(carousel => {
        updateButtons(carousel);
    });
});
