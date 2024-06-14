from rest_framework.test import APITestCase
from django.urls import reverse
from user_app.models import User
from user_app.serializers import UserSerializer


class UserSearchViewTestCase(APITestCase):
    url = reverse('user_app:user-search')

    def setUp(self):
        self.user1 = User.objects.create(
            first_name="Петя", last_name="Петров", middle_name="Иванович",
            phone="79123456789", email="petya_petrov@example.com"
        )
        self.user2 = User.objects.create(
            first_name="Вася", last_name="Пупкин", middle_name="Сергеевич",
            phone="79234567890", email="vasya_pupkin@example.com"
        )
        self.user3 = User.objects.create(
            first_name="Анна", last_name="Сидорова", middle_name="Игоревна",
            phone="79345678901", email="anna_sidorova@example.com"
        )

    def test_search_user_by_first_name(self):
        response = self.client.get(self.url, {'first_name': 'Петя'})
        expected_users = User.objects.filter(first_name__icontains='Петя')
        serialized_users = UserSerializer(expected_users, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serialized_users.data)

    def test_search_user_by_last_name(self):
        response = self.client.get(self.url, {'last_name': 'Пупкин'})
        expected_users = User.objects.filter(last_name__icontains='Пупкин')
        serialized_users = UserSerializer(expected_users, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serialized_users.data)

    def test_search_user_by_phone(self):
        response = self.client.get(self.url, {'phone': '79123456789'})
        expected_users = User.objects.filter(phone__icontains='79123456789')
        serialized_users = UserSerializer(expected_users, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serialized_users.data)

    def test_search_user_by_email(self):
        response = self.client.get(self.url, {'email': 'vasya_pupkin@example.com'})
        expected_users = User.objects.filter(email__icontains='vasya_pupkin@example.com')
        serialized_users = UserSerializer(expected_users, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serialized_users.data)

    def test_search_user_by_multiple_fields(self):
        response = self.client.get(self.url, {
            'first_name': 'Анна',
            'last_name': 'Сидорова'
        })
        expected_users = User.objects.filter(
            first_name__icontains='Анна',
            last_name__icontains='Сидорова'
        )
        serialized_users = UserSerializer(expected_users, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serialized_users.data)
