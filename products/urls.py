from django.urls import path, include
from .views import CategoryViewSet, ProductViewSet, precio_final
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls))
]

# Ruta del endpoint Facade que calcula el precio final con descuento
urlpatterns += [
    path('products/<int:pk>/precio-final/', precio_final),
]
