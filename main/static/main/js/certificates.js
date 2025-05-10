

function openModal(imgElement) {
    const modal = document.getElementById('modal');
    const modalImage = document.getElementById('modalImage');
  
    modalImage.src = imgElement.src;
    modal.style.display = "flex";
  
    // Плавное появление
    setTimeout(() => {
      modal.style.opacity = 1;
    }, 1);
  
    document.body.classList.add('no-scroll');
  }
  
  function closeModal(event) {
    if (event.target === event.currentTarget || event.target.classList.contains('close')) {
      const modal = document.getElementById('modal');
      modal.style.opacity = 0;
  
      setTimeout(() => {
        modal.style.display = "none";
      }, 300); // Задержка под анимацию исчезновения
  
      document.body.classList.remove('no-scroll');
    }
  }



//рабочий

let isZooming = false;
let startY, initialTop, initialMouseY;

function openModal(imgElement) {
  const modal = document.getElementById('modal');
  const modalImage = document.getElementById('modalImage');

  modalImage.src = imgElement.src;
  modalImage.style.transform = 'scale(1) translate(-50%, -50%)';  // Убираем начальный зум и центрируем
  modalImage.style.position = 'absolute';  // Устанавливаем позицию абсолютную
  modalImage.style.top = '50%';  // Центрируем по вертикали
  modalImage.style.left = '50%'; // Центрируем по горизонтали
  modalImage.style.transformOrigin = 'center center'; // Увеличение по центру
  modal.style.display = "flex";

  setTimeout(() => {
    modal.style.opacity = 1;
  }, 1);

  document.body.classList.add('no-scroll');
}

// Логика для увеличения изображения при удержании ЛКМ
const modalImage = document.getElementById('modalImage');

modalImage.addEventListener('mousedown', (e) => {
  // Устанавливаем флаг, что пользователь удерживает ЛКМ
  isZooming = true;

  // Отключаем перетаскивание
  e.preventDefault();

  // Сохраняем начальные значения
  startY = e.clientY;
  initialMouseY = e.clientY;

  // Получаем точку клика относительно изображения по горизонтали и вертикали
  const rect = e.target.getBoundingClientRect();
  initialTop = modalImage.getBoundingClientRect().top;
  const xPercent = ((e.clientX - rect.left) / rect.width) * 100;
  const yPercent = ((e.clientY - rect.top) / rect.height) * 100;

  // Устанавливаем точку увеличения изображения (с учетом точки клика)
  modalImage.style.transformOrigin = `${xPercent}% ${yPercent}%`;
  modalImage.style.transform = 'scale(2) translate(-25%, -25%)';  // Увеличиваем при удержании и центрируем
});

// Отслеживаем движение мыши для прокрутки
document.addEventListener('mousemove', (e) => {
  if (isZooming) {
    // Вычисляем смещение мыши по вертикали
    const offsetY = e.clientY - initialMouseY;

    // Прокручиваем изображение только по вертикали (вверх/вниз)
    modalImage.style.top = `${initialTop + (offsetY*2) + 350}px`;
  }
});

document.addEventListener('mouseup', () => {
  if (isZooming) {
    // Возвращаем картинку к нормальному состоянию при отпускании ЛКМ
    modalImage.style.transform = 'scale(1) translate(-50%, -50%)'; // Сбрасываем зум
    modalImage.style.top = '50%'; // Сбрасываем позицию

    isZooming = false;
  }
});

function closeModal(event) {
  if (event.target === event.currentTarget || event.target.classList.contains('close')) {
    const modal = document.getElementById('modal');
    modal.style.opacity = 0;

    setTimeout(() => {
      modal.style.display = "none";
    }, 300);

    document.body.classList.remove('no-scroll');
  }
}




  
  