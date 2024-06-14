from django.test import TestCase
from rest_framework import status

from user_app.models import User


class UserCreateViewTestCase(TestCase):

    URL = '/API/users/'

    def test_create_user_with_valid_data(self):
        # Подготовка данных для отправки запроса
        headers = {'HTTP_X_DEVICE': 'web'}

        data = {
            'first_name': 'Вася',
            'last_name': 'Пупкин',
            'birth_date': '1990-01-01',
            'passport_number': '1234567890',
            'place_of_birth': 'Москва',
            'phone': '79123456789',
            'email': 'vasya_pupkin@example.com',
            'registration_address': 'кремль',
            'residential_address': 'кремль',
        }

        response = self.client.post(self.URL, data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(User.objects.filter(email='vasya_pupkin@example.com').exists())

        user = User.objects.get(email='vasya_pupkin@example.com')
        self.assertEqual(user.first_name, 'Вася')

    def test_missing_x_device_header(self):
        # Отправляем POST запрос без указания заголовка x-Device
        data = {
            'first_name': 'John',
            'email': 'john.doe@example.com',
        }

        response = self.client.post('/API/users/', data, format='json')

        # Проверяем, что сервер вернул ошибку 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Заголовок 'x-Device' обязателен.", str(response.data))

