# Tienda Online - API Django

API REST de una tienda en línea hecha con Django y Django REST Framework.

## Funcionalidades

- CRUD de productos y categorías (`/api/v1/products/`, `/api/v1/categories/`)
- Modelo de usuario personalizado con inicio de sesión por correo electrónico y campo `telefono`
- CRUD de usuarios protegido para administradores (`/api/v1/users/`)
- Endpoint de datos personales del usuario autenticado (`/api/v1/auth/me/`)
- Autenticación con JWT (`/api/v1/auth/token/` y `/api/v1/auth/token/refresh/`) con `ACCESS_TOKEN_LIFETIME` configurado a 60 minutos
- Documentación interactiva con Swagger (`/swagger/`) y ReDoc (`/redoc/`) usando `drf-yasg`
- Pruebas unitarias (`python manage.py test`)

## Flujo de trabajo

- `main`: rama principal protegida, solo recibe cambios por Pull Request
- `dev`: rama de desarrollo
- `feature/*`: ramas para cada funcionalidad nueva
- `build`: rama generada por GitHub Actions para el despliegue
