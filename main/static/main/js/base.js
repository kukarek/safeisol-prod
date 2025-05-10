const navbar = document.querySelector('.navbar');
const header = document.querySelector('.header');
const content = document.querySelector('.content'); // Получаем элемент контента
const sticky = navbar.offsetTop; // Позиция навбара


if (window.innerWidth > 1080) {
    window.addEventListener('scroll', function() {
        if (window.scrollY > sticky) {
            navbar.classList.add('fixed'); // Добавляем класс для фиксации навбара
            content.classList.add('margin-navbar'); // Устанавливаем отступ сверху для контента
        } else {
            navbar.classList.remove('fixed'); // Убираем класс фиксации
            content.classList.remove('margin-navbar'); // Убираем отступ сверху для контента
        }
    });
}