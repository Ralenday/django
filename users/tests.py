from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

User = get_user_model()


class UserApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@tiendaonline.com',
            password='AdminPassword123!',
            first_name='Axel',
            last_name='Ramirez',
            telefono='6531234567',
        )
        self.user_cliente = User.objects.create_user(
            username='cliente1',
            email='cliente1@tiendaonline.com',
            password='ClientePassword123!',
            first_name='Carlos',
            last_name='Lopez',
            telefono='6539876543',
        )

    def test_login_jwt_con_email(self):
        response = self.client.post('/api/v1/auth/token/', {
            'email': 'admin@tiendaonline.com',
            'password': 'AdminPassword123!',
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_auth_me_no_expone_password_y_muestra_telefono(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/v1/auth/me/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'admin@tiendaonline.com')
        self.assertEqual(response.data['telefono'], '6531234567')
        self.assertNotIn('password', response.data)

    def test_list_users_no_expone_password(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        for item in response.data:
            self.assertNotIn('password', item)

    def test_actualizar_usuario_sin_password_no_cambia_su_password(self):
        self.client.force_authenticate(user=self.admin)
        hash_original = self.user_cliente.password

        response = self.client.patch(
            f'/api/v1/users/{self.user_cliente.id}/',
            {'first_name': 'Carlos Editado', 'telefono': '6530001122'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('password', response.data)

        self.user_cliente.refresh_from_db()
        self.assertEqual(self.user_cliente.first_name, 'Carlos Editado')
        self.assertEqual(self.user_cliente.telefono, '6530001122')
        # Verifica que el hash sigue siendo exactamente el original del cliente
        # y NO se sobrescribió con la contraseña del admin que hizo la petición
        self.assertEqual(self.user_cliente.password, hash_original)
        self.assertTrue(self.user_cliente.check_password('ClientePassword123!'))
        self.assertFalse(self.user_cliente.check_password('AdminPassword123!'))
