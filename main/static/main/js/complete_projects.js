// Открытие модального окна
function openModal(imgElement) {
    const modal = document.getElementById('modal');
    const modalImage = document.getElementById('modalImage');

    // Сначала устанавливаем display на flex
    modal.style.display = "flex";

    // Используем setTimeout для плавного появления
    setTimeout(() => {
        modal.style.opacity = 1; // Добавляем класс show для плавного появления
    }, 1); // Небольшая задержка для применения стилей
    modalImage.src = imgElement.src; // Устанавливаем изображение в модальном окне

    // Отключаем прокрутку
    document.body.classList.add('no-scroll');
}

// Закрытие модального окна
function closeModal(event) {
    if (event.target === event.currentTarget || event.target.classList.contains('close')) {
        const modal = document.getElementById('modal');
        modal.style.display = "none";

        setTimeout(() => {
            modal.style.opacity = 0; // Добавляем класс show для плавного появления
        }, 1);

        // Включаем прокрутку
        document.body.classList.remove('no-scroll');
    }
}