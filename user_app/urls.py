from django.urls import path
from .views import UserCreateView, UserDetailView, UserSearchView

app_name = 'user_app'

urlpatterns = [
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('users/search/', UserSearchView.as_view(), name='user-search'),
]