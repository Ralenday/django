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
