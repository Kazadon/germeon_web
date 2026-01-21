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
                
                const progress_div = document.createElement('div')
                progress_div.classList.add('progress')
                progress_div.style.background = '#2c3033'
                progress_div.style.border = '1px solid #797e82'
                
                const progressbar = document.createElement('div')
                progressbar.classList.add('progress-bar')
                progressbar.role = 'progressbar'
                progressbar.ariaValueNow = parseInt(result)
                progressbar.ariaValueMin = 0
                progressbar.ariaValueMax = 100
                progressbar.style.width = `${result}%`
                progressbar.textContent = `${result}%`
                if (result < 30) {
                    progressbar.style.background = `#b30000`
                } 
                else if(result < 50) {
                    progressbar.style.background = `#b35c00`
                }
                else if(result < 60) {
                    progressbar.style.background = `#b3ad00`
                }
                else {
                    progressbar.style.background = `#0dcaf0`
                }

                progress_div.appendChild(progressbar)
                callback_div.appendChild(progress_div)
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