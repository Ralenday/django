from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UserApiViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        if hasattr(request.data, '_mutable'):
            request.data._mutable = True
        if request.data.get('password'):
            request.data['password'] = make_password(request.data['password'])
        return super().create(request, *args, **kwargs)

    # Corrección de seguridad: solo se actualiza la contraseña si viene en la
    # petición; si no se envía, se conserva la contraseña original del usuario
    # editado (en lugar de sobrescribirla con request.user.password).
    def partial_update(self, request, *args, **kwargs):
        if hasattr(request.data, '_mutable'):
            request.data._mutable = True
        password = request.data.get('password')
        if password:
            request.data['password'] = make_password(password)
        else:
            request.data.pop('password', None)
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not kwargs.get('partial', False):
            if hasattr(request.data, '_mutable'):
                request.data._mutable = True
            password = request.data.get('password')
            if password:
                request.data['password'] = make_password(password)
            else:
                request.data.pop('password', None)
        return super().update(request, *args, **kwargs)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: UserSerializer()})
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
