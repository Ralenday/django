from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .services import obtener_estrategia

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
        'precio_final': round(precio_con_descuento, 2)
    })
