from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Category, Product


# Pruebas del endpoint de categorías
class CategoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Usuario de prueba para pasar la autenticación JWT (IsAuthenticated)
        self.user = User.objects.create_user(username='test', password='test123')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Electronica')

    def test_create_category(self):
        response = self.client.post('/api/v1/categories/', {'name': 'Ropa'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Ropa')

    def test_list_categories(self):
        response = self.client.get('/api/v1/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Electronica')


# Pruebas del endpoint de productos
class ProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', password='test123')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Electronica')
        self.product = Product.objects.create(
            name='Laptop',
            category=self.category,
            description='Laptop HP',
            price=15000.00
        )

    def test_create_product(self):
        response = self.client.post('/api/v1/products/', {
            'name': 'Mouse',
            'category': self.category.id,
            'description': 'Mouse inalambrico',
            'price': 500.00
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(response.data['category_name'], 'Electronica')

    def test_list_products(self):
        response = self.client.get('/api/v1/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Laptop')

    def test_update_product(self):
        response = self.client.put(f'/api/v1/products/{self.product.id}/', {
            'name': 'Laptop Pro',
            'category': self.category.id,
            'description': 'Laptop HP actualizada',
            'price': 18000.00
        })
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Laptop Pro')
        self.assertEqual(self.product.price, 18000)

    def test_delete_product(self):
        response = self.client.delete(f'/api/v1/products/{self.product.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)

    # Pruebas del endpoint /precio-final/ (Facade + Strategy)
    def test_precio_final_autenticado(self):
        response = self.client.get(f'/api/v1/products/{self.product.id}/precio-final/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('precio_final', response.data)

    def test_precio_final_sin_autenticar(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(f'/api/v1/products/{self.product.id}/precio-final/')
        self.assertEqual(response.status_code, 401)
