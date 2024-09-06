$(document).ready(function(){
    // Инициализация WebApp из Telegram
    const tg = window.Telegram.WebApp;

    // Устанавливаем данные пользователя из Telegram
    $('#tg_user_id').val(tg.initDataUnsafe.user.id);
    $('#tg_user_name').val(tg.initDataUnsafe.user.username);
    $('#tg_first_name').val(tg.initDataUnsafe.user.first_name);
    $('#tg_last_name').val(tg.initDataUnsafe.user.last_name);
    $('#tg_photo_url').val(tg.initDataUnsafe.user.photo_url);

    $('#userDataForm').on('submit', function(e){
        e.preventDefault();
        $('#loadingScreen').show();

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function(response){
                if(response.status === 'success'){
                    window.location.href = '/home/';
                } else {
                    alert('There was an error: ' + JSON.stringify(response.errors));
                }
                $('#loadingScreen').hide();
            },
            error: function(){
                alert('An unexpected error occurred.');
                $('#loadingScreen').hide();
            }
        });
    });
});