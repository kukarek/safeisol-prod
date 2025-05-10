


window.addEventListener('load', () => {
    const modal_form = document.getElementById('modal-form');
    const openModalBtns = document.querySelectorAll('.openModalForm'); // Получаем все кнопки

    // Добавляем обработчик события для каждой кнопки
    openModalBtns.forEach(button => {
        button.addEventListener('click', () => {
            modal_form.style.display = 'flex';
            setTimeout(() => {
                modal_form.style.opacity = 1; // Плавное появление
            }, 1);
        });
    });

    // Закрываем модал при клике вне его содержимого
    window.addEventListener('click', (e) => {
        if (e.target === modal_form) {
            modal_form.style.opacity = 0; // Плавное исчезновение
            setTimeout(() => {
                modal_form.style.display = 'none'; // Скрываем модал
            }, 300); // Задержка должна соответствовать времени анимации
        }
    });

    // Закрываем модал при клике на кнопку "Отправить"
    document.querySelector('.submit-btn').addEventListener('click', () => {
        modal_form.style.opacity = 0;
        setTimeout(() => {
            modal_form.style.display = 'none';
        }, 300);
    });

    document.getElementById('contactForm').addEventListener('submit', (e) => {
        e.preventDefault();
    
        const form = e.target;
        const formData = new FormData(form);
    
        // Логируем данные формы для проверки
        console.log('Form Data:', Array.from(formData.entries()));
    
        fetch('/api/send_contacts/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка при отправке. Код ответа: ' + response.status);
            }
    
            return response.json().catch(error => {
                throw new Error('Ошибка при обработке ответа от сервера: ' + error.message);
            });
        })
        .then(data => {
            if (data.success) {
                alert('Заявка принята!');
                modal_form.style.opacity = 0;
                setTimeout(() => {
                    modal_form.style.display = 'none';
                }, 300);
            } else {
                alert('Ошибка: ' + data.message);
            }
        })
        .catch(error => {
            alert('Ошибка: ' + error.message);
        });
    
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
    });
})