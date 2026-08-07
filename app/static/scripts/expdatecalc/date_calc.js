const form_calc = document.getElementById('form_calc')
const callback_div = document.getElementById('callback')
const mfg_input = document.getElementById('mfg_date')
const exp_input = document.getElementById('exp_date')

form_calc.addEventListener('submit', function(event){
    event.preventDefault()
    if (this.checkValidity()) {
        const mfg_date = new Date(`${mfg_input.value} 00:00:00`)
        const exp_date = new Date(`${exp_input.value} 00:00:00`)
        const current_date = new Date()
        console.log(`mfg - ${mfg_date}\nexp - ${exp_date}`)
        
        callback_div.innerHTML = `mfg - ${mfg_date}. exp - ${typeof(exp_date)}`
        if (mfg_date > current_date){
            callback_div.innerHTML = "Дата производства не может быть больше текущей даты. Проверьте введенные данные и попробуйте заново"
        }
        else if (mfg_date > exp_date){
            callback_div.innerHTML = "Дата производства не может быть больше даты окончания срока годности. Проверьте введенные данные и попробуйте заново"
        }
        else if (mfg_date == exp_date){
            callback_div.innerHTML = 'Дата производства и окончания срока годности не может быть одинаковой. Попробуйте другие данные.'
        }
        else {
            
            diff_days_exp_mfg = (exp_date - mfg_date)
            diff_days_exp_now = (exp_date - current_date)
            result = (diff_days_exp_now/diff_days_exp_mfg*100).toFixed(2)
            total_days = diff_days_exp_mfg/1000/60/60/24
            total_years = (diff_days_exp_mfg/1000/60/60/24/365).toFixed(1)
            if (result > 0){
                callback_div.innerHTML = `
                    <p class='d-flex flex-column justify-content-center'>Остаточный срок годности: ${result}%</p>
                    <p class='d-flex flex-column justify-content-center'>Срок годности в днях: ${total_days}</p>
                `
                if (total_days>=365) {
                    callback_div.innerHTML += `
                        <p class='d-flex flex-column justify-content-center'>Срок годности в годах: ${total_years}</p>
                    `
                }
                // родительский блок для прогресс бара и значения
                const progress_div = document.createElement('div')
                progress_div.classList.add('progress', 'position-relative')
                progress_div.style.background = '#1e2124' // Более глубокий темный тон
                progress_div.style.border = '1px solid #474b50' // Приглушенная граница
                progress_div.style.borderRadius = '4px'
                progress_div.style.height = '20px'
                progress_div.style.overflow = 'hidden'
                progress_div.style.boxShadow = 'inset 0 2px 4px rgba(0,0,0,0.5)' // Внутренняя тень

                // Прогресс бар
                const progressbar = document.createElement('div')
                progressbar.classList.add('progress-bar')
                progressbar.role = 'progressbar'
                progressbar.ariaValueNow = parseInt(result)
                progressbar.ariaValueMin = 0
                progressbar.ariaValueMax = 100

                // Настройка цветов градиентами
                let barColor;
                if (result < 30) {
                    barColor = 'linear-gradient(90deg, #ff3333, #b30000)'; // Красный - клиент откажется
                } else if (result < 50) {
                    barColor = 'linear-gradient(90deg, #ff9933, #b35c00)'; // Оранжевый - обязательно согласование с клиентом
                } else if (result < 60) {
                    barColor = 'linear-gradient(90deg, #e6de00, #b3ad00)'; // Желтый - лучше согласовать дополнительно
                } else if (result < 80) {
                    barColor = 'linear-gradient(90deg, #00e64d, #00b34b)'; // Зеленый - срок годности хороший
                } else {
                    barColor = 'linear-gradient(90deg, #00f0ff, #0099b3)'; // Голубой - срок идеален
                }

                progressbar.style.background = barColor;
                progressbar.style.borderRadius = '4px';

                // Эффект неонового свечения шкалы
                progressbar.style.boxShadow = '0 0 10px rgba(0, 192, 240, 0.2)'; 

                // Анимация заполнения шкалы
                progressbar.style.width = '0%';
                progressbar.style.transition = 'width 1s cubic-bezier(0.4, 0, 0.2, 1)';
                setTimeout(() => {
                    progressbar.style.width = `${result}%`;
                }, 50);

                // текст на прогресс баре
                const span_result = document.createElement('span')
                // Убран d-flex/justify, чтобы текст не сдвигался, пока шкала растет
                span_result.className = 'position-absolute w-100 h-100 text-center text-white' 
                span_result.style.lineHeight = '20px'
                span_result.style.fontSize = '12px'
                span_result.style.fontWeight = '500'
                span_result.style.textShadow = '1px 1px 2px rgba(0,0,0,0.8)' // Читаемость на любом фоне
                span_result.textContent = `${result}%`


                progress_div.appendChild(progressbar)
                callback_div.appendChild(progress_div)
                progress_div.appendChild(span_result)
            } 
            else{
                callback_div.innerHTML = `Товар просрочен`
            } 
        }
    }
})

form_calc.onreset = function(event){
    callback_div.innerHTML = ''
}