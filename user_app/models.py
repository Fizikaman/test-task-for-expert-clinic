from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Отчество")
    birth_date = models.DateField(verbose_name="Дата рождения")
    passport_number = models.CharField(max_length=15, verbose_name="Номер паспорта")
    place_of_birth = models.CharField(max_length=255, verbose_name="Место рождения")
    phone = models.CharField(
        max_length=11, verbose_name="Телефон",
        validators=[RegexValidator(regex='^7[0-9]{10}$', message='Введите правильный российский номер телефона.')])
    email = models.EmailField(null=True, blank=True, verbose_name="Email")
    registration_address = models.CharField(max_length=255, verbose_name="Адрес регистрации")
    residential_address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Адрес проживания")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
