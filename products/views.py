from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .services import consultar_pais_soap, obtener_estrategia


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']  # Permite /api/products/?category=1
    permission_classes = [IsAuthenticated]  # Solo usuarios con token JWT válido


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios con token JWT válido


# Patrón estructural (Facade): una sola llamada oculta la búsqueda del producto,
# la selección de la estrategia de descuento y el cálculo del precio final
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Protegido con JWT
def precio_final(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    estrategia = obtener_estrategia(producto.category.name)
    precio_con_descuento = estrategia.calcular(float(producto.price))
    return Response({
        'producto': producto.name,
        'categoria': producto.category.name,
        'precio_original': producto.price,
        'precio_final': round(precio_con_descuento, 2),
    })


# Consumo de Web Service SOAP público con zeep (Unidad 3)
@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'codigo',
            openapi.IN_QUERY,
            description='Código ISO del país a consultar vía SOAP (ej. MX, US, ES)',
            type=openapi.TYPE_STRING,
            default='MX',
        )
    ],
)
@api_view(['GET'])
@permission_classes([AllowAny])
def soap_pais_info(request):
    codigo = request.query_params.get('codigo', 'MX')
    resultado = consultar_pais_soap(codigo)
    return Response(resultado)
