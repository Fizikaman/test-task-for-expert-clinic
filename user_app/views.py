from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    """Контроллера для создания пользователя
    /API/users/"""
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
    """Контроллер для поиска юзера по - фамилия, имя, отчество, телефон, email.
     Пример API запроса с 2-мя и более фильтрами:
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
