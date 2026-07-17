async function fetchPreorders(dateValue) {
    const searchInfoContainer = document.getElementById('search-info-container')
    const ordersContainer = document.getElementById('ordersContainer');
    const requestsList = document.getElementById('requestsList')
    const cardTemplate = document.getElementById('orderCardTemplate');
    const submitBtn = document.getElementById('preorder_submit');

    submitBtn.disabled = true;
    searchInfoContainer.innerHTML = `<span class='d-flex justify-content-center align-items-center'> Загрузка данных из Деловых Линий...</span>`;

    try {
        // Отправляем каноничный GET-запрос с query-параметром
        const response = await fetch(`/preorders/search?search_date=${dateValue}`);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Произошла ошибка при поиске');
        }

        // Очищаем перед выводом новых данных
        searchInfoContainer.innerHTML = ''; 
        requestsList.innerHTML = ''

        if (result.data.length === 0) {
            searchInfoContainer.innerHTML = `<span style="d-flex justify-content-center align-items-center text-align: center; color: #dc3545; padding: 20px;">Заказы на эту дату не найдены</span>`;
            return;
        } else {
            ordersContainer.classList.remove('d-none')
            requestsList.innerHTML = ''
        }
        
        // Клонирование и наполнение шаблонов заявки данными из респонса
        result.data.forEach(order => {
            const cardClone = cardTemplate.content.cloneNode(true);
            const collapseId = `details-${order.orderId}`;
            // Настройка триггеров сворачивания
            cardClone.querySelectorAll('.dropdown-toggle').forEach(el => {
                el.setAttribute('data-bs-target', `#${collapseId}`);
                el.setAttribute('data-bs-toggle', 'collapse');
            });
            const orderDetailsContainer = cardClone.querySelector('.order-details-container');
            orderDetailsContainer.setAttribute('id', collapseId);

            // 2. Безопасно наполняем текстовыми данными (Защита от XSS-атак)
            cardClone.querySelector('.order-id').textContent = order.orderId;
            cardClone.querySelector('.order-receiver-name').textContent = order.receiver.name;
            cardClone.querySelector('.order-arrival-city').textContent = order.arrival.city;
            cardClone.querySelector('.order-freight-places').textContent = order.freight.places
            cardClone.querySelector('.order-freight-weight').textContent = order.freight.weight;
            cardClone.querySelector('.order-freight-volume').textContent = order.freight.volume + 'м³';
            cardClone.querySelector('.order-arrival-address').textContent = order.arrival.address;
            cardClone.querySelector('.order-receiver-contacts').textContent = order.receiver.contacts;
            cardClone.querySelector('.order-receiver-phones').textContent = order.receiver.phones;
            // console.log(order)
            
            requestsList.appendChild(cardClone);
        });
    } catch (error) {
        // Выводим ошибку, если бэкенд или API Деловых Линий вернули 500
        searchInfoContainer.innerHTML = `<span class="d-flex justify-content-center align-items-center" style="text-align: center; color: #dc3545; padding: 20px; font-weight: bold;">${error.message} - ???</span>`;
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

    // 2. Возвращаем таблицу в исходное состояние
    const ordersContainer = document.getElementById('ordersContainer');
    ordersContainer.classList.add('d-none')
    const requestsList = document.getElementById('requestsList')
    requestsList.innerHTML = ``;


    // 3. ОЧИЩАЕМ АДРЕСНУЮ СТРОКУ БРАУЗЕРА
    const cleanUrl = window.location.pathname;
    window.history.pushState({ path: cleanUrl }, '', cleanUrl);
}
