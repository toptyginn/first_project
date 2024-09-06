from django.test import TestCase
from django.urls import reverse
from .models import UserProfile, Referral
from unittest.mock import patch
from .views import register_view
from django.test import RequestFactory
from django.http import HttpResponseForbidden, HttpResponse
from .decorators import mobile_only


class UserDataModelTest(TestCase):
    def test_creating_user_data(self):
        user = UserProfile.objects.create(id=12345, username='testuser')
        user.save()
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.id, 12345)


class ViewsTest(TestCase):
    def test_user_data_view_get(self):
        response = self.client.get(reverse('register_view'), HTTP_USER_AGENT='Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X)', )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'load_user_data.html')

    def test_user_data_view_post_success(self):
        response = self.client.post(reverse('register_view'), {
            'tg_user_id': 12345,
            'username': 'testuser'
        },
                                    HTTP_USER_AGENT='Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X)', )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertJSONEqual(response.content, {'status': 'success'})

    def test_redirect_to_home_after_submission(self):
        response = self.client.post(reverse('register_view'), {
            'tg_user_id': 12345,
            'username': 'testuser'
        },
                                    HTTP_USER_AGENT='Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X)', )
        self.assertEqual(response.status_code, 200)
        # Предположим, что редирект в JS осуществляется правильно
        response = self.client.get(reverse('home_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view(self):
        response = self.client.post(reverse('register_view'), {
            'tg_user_id': 12345,
            'tg_user_name': 'testuser'
        },
                                    HTTP_USER_AGENT='Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X)', )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('home_view'), data={
            'id': 12345
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    # Тесты для остальных страниц
    def test_grow_view(self):
        response = self.client.get(reverse('grow_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grow.html')

    def test_tasks_view(self):
        response = self.client.get(reverse('tasks_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks.html')

    def test_boosts_view(self):
        response = self.client.get(reverse('boosts_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'boosts.html')

    def test_friends_view(self):
        response = self.client.post(reverse('register_view'), {
            'tg_user_id': 12345,
            'tg_user_name': 'testuser'
        },
                                    HTTP_USER_AGENT='Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X)', )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('api_referrals_view'), data={
            'id': 12345
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'friends.html')


class ReferralTest(TestCase):
    def setUp(self):
        self.referrer = UserProfile.objects.create(id=333, username='referrer')
        self.referree = UserProfile.objects.create(id=67890, username='referree')
        self.referral = Referral.objects.create(user=self.referrer, referred_user=self.referree)
        self.referrer.save()
        self.referree.save()
        self.referral.save()

    def test_referral_creation(self):
        self.assertEqual(Referral.objects.count(), 1)
        self.assertEqual(self.referral.user, self.referrer)

    # def test_apply_referral_code(self):
    #     # Логика применения реферального кода
    #     applied = self.referral.apply_to_user(self.referree)
    #     self.assertTrue(applied)
    #     self.assertEqual(self.referral.referree, self.referree)
    #
    # def test_referral_usage_limit(self):
    #     # Проверка лимита использования кода
    #     for _ in range(self.referral.usage_limit):
    #         self.referral.apply_to_user(UserProfile.objects.create(id=70000 + _, username=f'user{_}'))
    #     self.assertEqual(self.referral.usage_count, self.referral.usage_limit)
    #     self.assertFalse(
    #         self.referral.apply_to_user(UserProfile.objects.create(id=90000, username='user_exceed')))


class TelegramWebAppTest(TestCase):
    @patch('main.views.register_view')
    def test_telegram_webapp_data(self, MockTelegram):
        """Тест для Telegram WebApps data"""
        # Настроим мока для имитации Telegram WebApp
        tg_instance = MockTelegram.WebApp.initDataUnsafe
        tg_instance.user.id = 12345
        tg_instance.user.username = 'testuser'

        response = self.client.post(reverse('register_view'), {
            'tg_user_id': tg_instance.user.id,
            'username': tg_instance.user.username
        },
                                    HTTP_USER_AGENT='Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X)', )
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success'})


class MobileOnlyDecoratorTestCase(TestCase):

    def test_mobile_user_agent(self):
        """Тест для запроса с мобильного устройства"""
        # Эмулируем GET-запрос с мобильного устройства
        response = self.client.get(reverse('register_view'), {
            'tg_user_id': 12345,
            'tg_user_name': 'testuser'
        },
                                   HTTP_USER_AGENT='Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X)', )

        # Ожидается, что декоратор пропустит запрос и вернет успешный ответ
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'load_user_data.html')

    def test_non_mobile_user_agent(self):
        """Тест для запроса с немобильного устройства"""
        # Эмулируем GET-запрос с немобильного устройства
        response = self.client.get(reverse('register_view'), {
            'tg_user_id': 12345,
            'tg_user_name': 'testuser'
        },
                                   HTTP_USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64)')

        # Ожидается, что декоратор вернет 403 Forbidden для немобильного устройства
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'load_user_data.html')

    def test_empty_user_agent(self):
        """Тест для запроса с пустым User-Agent"""
        # Эмулируем GET-запрос с пустым User-Agent
        response = self.client.get(reverse('register_view'), {
            'tg_user_id': 12345,
            'tg_user_name': 'testuser'
        },
                                   HTTP_USER_AGENT='')

        # Ожидается, что декоратор вернет 403 Forbidden для пустого User-Agent
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'load_user_data.html')
