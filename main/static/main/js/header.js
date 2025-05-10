


window.addEventListener('load', function() {
    const searchButton = document.getElementById('searchButton');
    const searchInput = document.getElementById('searchInput');
    const searchPopup = document.getElementById('searchPopup');
    const searchResults = document.getElementById('searchResults');
    const closeButton = document.getElementById('closePopupButton');

    // Показать окно поиска при нажатии на кнопку
    searchButton.addEventListener('click', function() {
        searchPopup.style.display = 'flex';
        searchInput.focus();
    });

    // Закрыть окно поиска при нажатии на крестик
    closeButton.addEventListener('click', function() {
        searchPopup.style.display = 'none';
    });

    // Получение всех продуктов
    let products = [];
    fetch('/api/products/')
        .then(response => response.json())
        .then(data => {
            products = data; // Сохраняем данные о продуктах
        });

    // Обработчик ввода в поле поиска
    searchInput.addEventListener('input', function() {
        const query = this.value ? this.value.toLowerCase() : ''; // Проверяем, есть ли значение
        searchResults.innerHTML = ''; // Очищаем предыдущие результаты

        if (query.length  > 0) {
        // Фильтруем продукты на стороне клиента
        const filteredProducts = products.filter(product => {
            const includesQuery = product.title.toLowerCase().includes(query);
            return includesQuery;
        });

            if (filteredProducts.length > 0) {
                filteredProducts.forEach(product => {

                    const li = document.createElement('li');
        
                    // Создаем элемент <a>
                    const link = document.createElement('a');
                    link.textContent = product.title; // Отображаем имя продукта
                    link.href = product.url; // Устанавливаем URL

                    // Добавляем ссылку в элемент <li>
                    li.appendChild(link);
                    
                    // Добавляем элемент <li> в контейнер результатов поиска
                    searchResults.appendChild(li);
                });
                searchPopup.style.display = 'flex'; // Показываем всплывающее окно
            } 
    }});

    // Закрытие всплывающего окна при клике вне его
    window.addEventListener('click', function(event) {
        if (!searchPopup.contains(event.target) && event.target !== searchButton) {
            searchPopup.style.display = 'none'; // Скрываем всплывающее окно
        }
    });

    // Обработчик нажатия клавиши Esc
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            searchPopup.style.display = 'none'; // Закрываем всплывающее окно
        }
    });
});


const sidebar = document.getElementById('mob-panel-nav');

function toggleMobSidebar() {
    sidebar.classList.toggle('active');
}