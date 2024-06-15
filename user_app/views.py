from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .models import User
from .serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    """Контроллер для создания пользователя через разные девайсы
    На данный endpoint /API/users/ необходимо передать заголовок 'x-Device' с возможными
    значениями - mail, mobile, web.
    Для каждого заголовка свои обязательные поля:
    mail - first_name, email
    mobile - phone
    web - last_name, first_name, birth_date, passport_number, place_of_birth, phone, registration_address"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        if 'x-Device' not in request.headers:
            raise ValidationError("Заголовок 'x-Device' обязателен.")
        return super(UserCreateView, self).create(request, *args, **kwargs)


class UserDetailView(generics.RetrieveAPIView):
    """Контроллер для просмотра инфы о юзере по его id
    /API/users/<int:id>/"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'


class UserSearchView(generics.ListAPIView):
    """Контроллер для поиска юзера по следующим параметрам - фамилия, имя, отчество, телефон, email.
     Пример API запроса с 2-мя и более параметрами:
            ?first_name=<Петя>&last_name=<Петров>
            /API/users/search/?first_name=Петя&last_name=Петров
     """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_params = self.request.query_params

        if 'first_name' in search_params:
            queryset = queryset.filter(first_name__icontains=search_params['first_name'])
        if 'last_name' in search_params:
            queryset = queryset.filter(last_name__icontains=search_params['last_name'])
        if 'middle_name' in search_params:
            queryset = queryset.filter(middle_name__icontains=search_params['middle_name'])
        if 'phone' in search_params:
            queryset = queryset.filter(phone__icontains=search_params['phone'])
        if 'email' in search_params:
            queryset = queryset.filter(email__icontains=search_params['email'])

        return queryset
