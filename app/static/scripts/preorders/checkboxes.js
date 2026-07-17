document.addEventListener('DOMContentLoaded', () => {
    const selectAll = document.getElementById('selectAllRequests');
    const requestsList = document.getElementById('requestsList')
    const counter = document.getElementById('selectedCounter');

    // 1. Функция обновления счетчика выбранных элементов
    function updateCounter() {
        const allCheckboxes = requestsList.querySelectorAll('.request-checkbox');
        const checkedCount = requestsList.querySelectorAll('.request-checkbox:checked').length;

        if (checkedCount > 0) {
            counter.innerText = `ВЫБРАНО: ${checkedCount}`;
            counter.style.display = 'inline-block';
        } else {
            counter.style.display = 'none';
        }
        // Синхронизируем главный чекбокс "Выбрать все"
        if (allCheckboxes.length > 0) {
            selectAll.checked = (checkedCount === allCheckboxes.length);
        } else {
            selectAll.checked = false;
        }
    }

    // 2. Событие для индивидуальных чекбоксов
    requestsList.addEventListener('change', (event) => {
        if (event.target.classList.contains('request-checkbox')) {
            updateCounter()
        }
    })

    // 3. Событие для чекбокса "Выбрать все"
    selectAll.addEventListener('change', function() {
        // Каждый раз находим актуальные чекбоксы, которые сейчас есть на странице
        const currentCheckboxes = requestsList.querySelectorAll('.request-checkbox');
        currentCheckboxes.forEach(cb => cb.checked = this.checked);
        updateCounter();
    });

});

function printSingle(id) {
    console.log('Заявка: ', id);
}