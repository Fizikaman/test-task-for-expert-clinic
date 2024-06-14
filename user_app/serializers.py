from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        request = self.context.get('request')
        device = request.headers.get('x-Device')

        if device == 'mail':
            if not data.get('first_name') or not data.get('email'):
                raise serializers.ValidationError("Имя и email обязательны для устройства 'mail'.")
        elif device == 'mobile':
            if not data.get('phone'):
                raise serializers.ValidationError("Номер телефона обязателен для устройства 'mobile'.")
        elif device == 'web':
            required_fields = [
                'last_name', 'first_name',
                'birth_date', 'passport_number',
                'place_of_birth', 'phone', 'registration_address'
            ]
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError(f"Поле {field} обязательно для устройства 'web'.")
        else:
            raise serializers.ValidationError("Неверное значение заголовка 'x-Device'.")

        return data
