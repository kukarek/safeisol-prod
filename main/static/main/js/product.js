

function selectImage(src, element) {
    const mainImage = document.getElementById('main-image');
    const img = element.querySelector('img'); // находим вложенный <img>

    mainImage.src = "/static/main/media/" + src;
    mainImage.alt = img.alt || '';
    mainImage.title = img.alt || '';

    const miniImages = document.querySelectorAll('.mini-img');
    miniImages.forEach(imgDiv => imgDiv.classList.remove('selected'));

    element.classList.add('selected');
}

// Открытие модального окна
function openModal() {
    const modal = document.getElementById('modal');
    const modalImage = document.getElementById('modal-image');
    // Сначала устанавливаем display на flex
    modal.style.display = "flex";

    // Используем setTimeout для плавного появления
    setTimeout(() => {
        modal.style.opacity = 1; // Добавляем класс show для плавного появления
    }, 1); // Небольшая задержка для применения стилей
    modalImage.src = document.getElementById('main-image').src; // Устанавливаем изображение в модальном окне
    modalImage.alt = document.getElementById('main-image').alt;
    modalImage.title = document.getElementById('main-image').alt; 

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


// Получаем все элементы навигации
const navLinks = document.querySelectorAll('.product-navbar-li a');

// Функция для переключения контента
function showContent(event) {
    event.preventDefault(); // Отменяем переход по ссылке

    // Убираем класс 'selected' и добавляем 'navbar-link' ко всем ссылкам
    navLinks.forEach(link => {
        link.classList.remove('selected');
        link.classList.add('navbar-link');
    });

    // Получаем ID нажатой ссылки
    const selectedId = event.target.parentElement.id.replace('navbar-', 'content-');

    // Скрываем все секции контента
    const sections = document.querySelectorAll('.container > div[id^="content-"]');
    sections.forEach(section => {
        section.style.display = 'none';
    });

    // Показываем соответствующий контент
    document.getElementById(selectedId).style.display = 'block';

    // Выделяем нажатую ссылку
    event.target.classList.add('selected');
    event.target.classList.remove('navbar-link'); // Убираем класс 'navbar-link' у выбранной ссылки
}

// Добавляем обработчики событий для каждой ссылки
navLinks.forEach(link => {
    link.addEventListener('click', showContent);
});



