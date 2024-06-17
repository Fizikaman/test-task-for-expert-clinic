from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ()

    def validate(self, data):
        request = self.context.get('request')
        device = request.headers.get('x-Device')

        if device == 'mail':
            required_fields = ['first_name', 'email']
            for field in required_fields:
                if field not in data:
                    raise serializers.ValidationError(f"{field} обязательно для устройства 'mail'.")
            return data
        elif device == 'mobile':
            required_fields = ['phone']
            for field in required_fields:
                if field not in data:
                    raise serializers.ValidationError(f"{field} обязателен для устройства 'mobile'.")
            return data
        elif device == 'web':
            required_fields = [
                'last_name', 'first_name',
                'birth_date', 'passport_number',
                'place_of_birth', 'phone', 'registration_address'
            ]
            for field in required_fields:
                if field not in data:
                    raise serializers.ValidationError(f"{field} обязательно для устройства 'web'.")
            return data
        else:
            raise serializers.ValidationError("Неверное значение заголовка 'x-Device'.")

    def to_representation(self, instance):
        request = self.context.get('request')
        representation = super().to_representation(instance)

        # только для POST-запросов
        if request and request.method == 'POST':
            device = request.headers.get('x-Device')
            devices_to_filter = {'mail', 'mobile', 'web'}

            if device in devices_to_filter:
                initial_data = request.data
                fields_to_include = set(initial_data.keys())
                # Возвращаем только те поля, которые были в запросе
                representation = {field: value for field, value in representation.items() if field in fields_to_include}

        return representation
