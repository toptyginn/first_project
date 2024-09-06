from django.urls import path
from .views import register_view
from .views import home_view, tasks_view, grow_view, boosts_view, api_referrals_view, water_view

urlpatterns = [
    path('home/', home_view, name='home_view'),
    path('tasks/', tasks_view, name='tasks_view'),
    path('grow/', grow_view, name='grow_view'),
    path('boosts/', boosts_view, name='boosts_view'),
    path('api/referrals/', api_referrals_view, name='api_referrals_view'),
    path('register/', register_view, name='register_view'),
    path('water/', water_view, name='water_view')
]
