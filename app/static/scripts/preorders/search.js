async function fetchPreorders(dateValue) {
    const ordersContainer = document.getElementById('ordersContainer');
    const cardTemplate = document.getElementById('orderCardTemplate');
    const submitBtn = document.getElementById('preorder_submit');

    submitBtn.disabled = true;
    ordersContainer.innerHTML = `<span> Загрузка данных из Деловых Линий...</span>`;

    try {
        // Отправляем каноничный GET-запрос с query-параметром
        const response = await fetch(`/preorders/search?search_date=${dateValue}`);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Произошла ошибка при поиске');
        }

        // Очищаем таблицу перед выводом новых данных
        ordersContainer.innerHTML = ''; 

        if (result.data.length === 0) {
            ordersContainer.innerHTML = `<span style="text-align: center; color: #dc3545; padding: 20px;">Заказы на эту дату не найдены</span>`;
            return;
        }

        // Фронтенд-цикл для сборки строк таблицы на лету
        result.data.forEach(order => {
            const cardClone = cardTemplate.content.cloneNode(true);
    
            // 2. Безопасно наполняем текстовыми данными (Защита от XSS-атак)
            cardClone.querySelector('.order-id').textContent = order.orderId;
            cardClone.querySelector('.order-receiver').textContent = order.receiver.name;
            cardClone.querySelector('.order-city').textContent = order.arrival.city;
            
            ordersContainer.appendChild(cardClone);
        });
    } catch (error) {
        // Выводим ошибку, если бэкенд или API Деловых Линий вернули 500
        ordersContainer.innerHTML = `<span style="text-align: center; color: #dc3545; padding: 20px; font-weight: bold;">${error.message}</span>`;
    } finally {
        // Разблокируем кнопку
        submitBtn.disabled = false;
    }

}

// 1. Отправка формы onsubmit
document.getElementById('preorder_form').addEventListener('submit', function(event) {
    event.preventDefault(); // Отменяем перезагрузку страницы
    
    const dateValue = document.getElementById('order_date').value;
    
    // Подменяем URL в браузере без перезагрузки (чтобы ссылкой можно было поделиться)
    const newUrl = `${window.location.pathname}?search_date=${dateValue}`;
    window.history.pushState({ path: newUrl }, '', newUrl);

    // Вызываем функцию загрузки
    fetchPreorders(dateValue);
});

// 2. Сброс выведенных данных и обновление URL
function resetPage() {
    // 1. Очистка данных формы
    document.getElementById('preorder_form').reset();

    // 2. Возвращаем таблицу в исходное состояние (Placeholder-текст)
    const tableBody = document.getElementById('ordersContainer');
    tableBody.innerHTML = ``;

    // 3. На случай, если сброс нажали во время загрузки, возвращаем кнопку поиска
    // document.getElementById('submitBtn').disabled = false;

    // 4. ОЧИЩАЕМ АДРЕСНУЮ СТРОКУ БРАУЗЕРА
    // Возвращаем URL к чистому виду /getpreorders без ?search_date=...
    const cleanUrl = window.location.pathname;
    window.history.pushState({ path: cleanUrl }, '', cleanUrl);
}

// 3. Дополнительная фича продакшена: Автозапрос при переходе по ссылке
// window.addEventListener('DOMContentLoaded', () => {
//     const urlParams = new URLSearchParams(window.location.search);
//     const dateParam = urlParams.get('search_date');
    
//     if (dateParam) {
//         document.getElementById('order_date').value = dateParam; // Подставляем дату в календарик
//         fetchPreorders(dateParam); // Запускаем поиск
//     }
// });