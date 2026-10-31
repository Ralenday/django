from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet, precio_final, soap_pais_info

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
]

# Rutas adicionales: Facade de precio final y consumo SOAP con zeep
urlpatterns += [
    path('products/<int:pk>/precio-final/', precio_final, name='precio_final'),
    path('soap/pais/', soap_pais_info, name='soap_pais_info'),
]
