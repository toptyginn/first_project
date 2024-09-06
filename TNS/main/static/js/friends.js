document.addEventListener('DOMContentLoaded', function() {
    // Пример: Асинхронная загрузка данных о рефералах
    function loadReferrals() {
        fetch('/api/referrals/')
            .then(response => response.json())
            .then(data => {
                let referralContainer = document.getElementById('referral-container');
                referralContainer.innerHTML = '';  // Очищаем контейнер перед добавлением новых данных

                data.forEach(referral => {
                    let referralDiv = document.createElement('div');
                    referralDiv.style = "border: 1px solid #000; padding: 20px; margin: 10px; display: flex; align-items: center;";

                    let profilePicDiv = document.createElement('div');
                    profilePicDiv.style = "width: 50px; height: 50px; border-radius: 50%; background-color: grey;";

                    if (referral.profile_picture) {
                        let profilePic = document.createElement('img');
                        profilePic.src = referral.profile_picture;
                        profilePic.style = "width: 50px; height: 50px; border-radius: 50%;";
                        profilePicDiv.appendChild(profilePic);
                    }

                    let infoDiv = document.createElement('div');
                    infoDiv.style = "margin-left: 20px;";
                    infoDiv.innerHTML = `<p><strong>Name:</strong> ${referral.first_name} ${referral.last_name}</p>
                                        <p><strong>XP:</strong> ${referral.xp}</p>
                                        <p><strong>Coins:</strong> ${referral.coins}</p>`;

                    referralDiv.appendChild(profilePicDiv);
                    referralDiv.appendChild(infoDiv);
                    referralContainer.appendChild(referralDiv);
                });
            })
            .catch(error => console.error('Error:', error));
    }

    loadReferrals();  // Загрузить данные при загрузке страницы
});