from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'telefono',
            'password',
            'is_active',
            'is_staff',
        ]
        # Corrección de seguridad: write_only evita que el hash de la contraseña
        # se exponga en las respuestas de la API (incluyendo /api/v1/auth/me/)
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'telefono']
        extra_kwargs = {
            'password': {'write_only': True},
            'telefono': {'required': False},
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                'La contraseña debe tener al menos 8 caracteres.'
            )
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
