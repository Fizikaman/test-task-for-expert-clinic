from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user_app.models import User
from user_app.serializers import UserSerializer


class UserDetailViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name='Вася',
            last_name='Пупкин',
            middle_name='Иванович',
            birth_date='1990-01-01',
            passport_number='1234567890',
            place_of_birth='Москва',
            phone='79123456789',
            email='vasya_pupkin@example.com',
            registration_address='кремль',
            residential_address='кремль'
        )

        self.url = reverse('user_app:user-detail', kwargs={'id': self.user.id})

    def test_get_user_detail(self):
        """Просмотр детальной инфы о юзере по его id"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = UserSerializer(self.user).data
        self.assertEqual(response.data, expected_data)
