document.addEventListener('DOMContentLoaded', function() {
    let remainingTime = parseInt(document.getElementById('water-button').dataset.remainingTime);
    let waterButton = document.getElementById("water-button");
    let timerDisplay = document.getElementById("timer-display");

    const timerElement = document.getElementById('timer');
    let timeRemaining = 6 * 60 * 60; // 6 часов в секундах
    function initializing(){
       window.Telegram.WebApp.ready();

       // Получаем данные пользователя
       const user = window.Telegram.WebApp.initDataUnsafe.user;
        fetch("{% url 'register_view' %}", {
           method: 'POST',
           headers: {
               'Content-Type': 'application/json',
           },
           body: JSON.stringify(user)
       })
       .catch((error) => {
           console.error('Error:', error);
       });

    }
    initializing();

    function updateTimer() {
        const hours = Math.floor(timeRemaining / 3600);
        const minutes = Math.floor((timeRemaining % 3600) / 60);
        const seconds = timeRemaining % 60;

        timerElement.textContent = ${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')};
        if (timeRemaining > 0) {
            timeRemaining -= 1;
        }
    }
    updateTimer();

    waterButton.addEventListener('click', function() {
        waterButton.disabled = true;
        fetch('/water/', { method: 'POST' });  // Путь '/water/' должен быть настроен в Django для обработки запроса
        remainingTime = 21600;  // Обновить таймер на 6 часов
        updateTimer();
    });
});

