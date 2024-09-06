from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import UserProfileForm, UserRegistrationForm
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import UserProfile, Referral
from django.http import HttpResponse
from .decorators import mobile_only


# def profile_view(request):
#     user_profile = UserProfile.objects.get(user=request.user)
#     referrals = user_profile.referrals.all()
#     return render(request, 'profile.html', {'user_profile': user_profile, 'referrals': referrals})
@mobile_only
def register_view(request):
    if request.method == 'POST':
        tg_user_id = request.POST.get('tg_user_id', 'Unknown')
        tg_user_name = request.POST.get('tg_user_name', 'Unknown')
        tg_first_name = request.POST.get('tg_first_name','Unknown')
        tg_last_name = request.POST.get('tg_last_name', 'Unknown')
        tg_photo_url = request.POST.get('tg_photo_url', '404')
        if tg_user_id and tg_user_name:
            try:
                user = UserProfile.objects.create(id=tg_user_id, username=tg_user_name, first_name=tg_first_name,
                                       last_name=tg_last_name, profile_picture=tg_photo_url)
                user.save()
            except Exception as E:
                return JsonResponse({'status': 'error', 'errors': E})
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': 'Missing Telegram user data'})

    return render(request, 'load_user_data.html')


def home_view(request):
    user_id = request.GET.get('id', 12345)
    user_profile = UserProfile.objects.get(id=user_id)
    last_watered_time = request.session.get('last_watered_time')

    if last_watered_time:
        time_difference = timezone.now() - timezone.datetime.fromtimestamp(last_watered_time)
        remaining_time = max(0, 21600 - time_difference.total_seconds())  # 21600 секунд = 6 часов
    else:
        remaining_time = 21600  # 6 часов

    return render(request, 'home.html', {
        'user_profile': user_profile,
        'remaining_time': remaining_time,
    })


# Пустая страница Tasks
def tasks_view(request):
    return render(request, 'tasks.html')


# Пустая страница Grow
def grow_view(request):
    return render(request, 'grow.html')


# Страница Boosts с четырьмя большими кнопками
def boosts_view(request):
    if request.method == 'GET':
        lvls = request.GET.get('boosts')
        boosts = [
            {"name": "Lighting", "description": "Improves lighting conditions", "cost": 0.006, 'lvl': lvls.lighting},
            {"name": "Fertilizer", "description": "Enhances soil quality", "cost": 0.006, 'lvl': lvls.fertilizer},
            {"name": "Sour", "description": "Increases growth rate", "cost": 0.006, 'lvl': lvls.sour},
            {"name": "Title", "description": "Custom title for your farm", "cost": 0, 'lvl': 0},
        ]
    return render(request, 'boosts.html', {'boosts': boosts})


# Страница Friends с реферальной программой


def api_referrals_view(request):
    user_id = request.GET.get('id', 12345)
    user_profile = UserProfile.objects.get(id=user_id) #request.user.id
    referrals = user_profile.referrals.all()

    referral_data = []
    for referral in referrals:
        referred_profile = referral.referred_user
        referral_data.append({
            'first_name': referred_profile.user.first_name,
            'last_name': referred_profile.user.last_name,
            'xp': referred_profile.xp,
            'coins': referred_profile.coins,
            'profile_picture': referred_profile.profile_picture.url if referred_profile.profile_picture else None
        })

    return render(request, 'friends.html', {'refferals': referral_data})#JsonResponse(referral_data, safe=False)


def water_view(request):
    if request.method == 'POST':
        request.session['last_watered_time'] = timezone.now().timestamp()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'})
