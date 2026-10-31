# Tienda Online — Full Stack Django REST + ReactJS + JWT + SOAP (RA2 y RA3)

Proyecto Full Stack de **Tienda Online** desarrollado para la materia de Desarrollo Web Integral (IDGS 9-2). Integra un **Backend en Django REST Framework** (con documentación Swagger, modelo de usuario personalizado con login por correo electrónico y campo `telefono`, autenticación JWT y consumo de un Web Service SOAP público con `zeep`) y un **Frontend en React + Vite** (con React Router v6, Semantic UI, Formik/Yup, `AuthContext`, registro de usuarios y consumo de APIs de terceros mediante `fetch`).

## Estructura del Repositorio

```text
django-project/
├── manage.py
├── requirements.txt           # Dependencias del Backend (Django, DRF, SimpleJWT, drf-yasg, corsheaders, zeep)
├── tienda_online/             # Configuración del proyecto, CORS, JWT y Swagger
├── users/                     # Modelo User (login por email + telefono), CRUD, /auth/me/ y /auth/register/
├── products/                  # CRUD de productos/categorías, Facade /precio-final/ y cliente SOAP /soap/pais/
└── frontend/                  # Aplicación Frontend en React + Vite
    ├── package.json
    ├── .env.example
    └── src/
        ├── api/               # Comunicación con la API (token.js, user.js)
        ├── context/           # Contexto de sesión persistente (AuthContext.jsx)
        ├── hooks/             # Custom hooks (useAuth.jsx, useUser.jsx)
        ├── layouts/           # Layouts (AdminLayout, ClientLayout, CommonLayout)
        ├── pages/             # Pantallas (Login, Register, Dashboard con widgets, Home, Error404)
        └── routes/            # Sistema de rutas con React Router DOM v6
```

## Instrucciones de Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/Ralenday/django.git
cd django
```

### 2. Configurar y ejecutar el Backend (Django)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- **Documentación interactiva Swagger:** `http://127.0.0.1:8000/swagger/`
- **Endpoint de Login JWT:** `POST http://127.0.0.1:8000/api/v1/auth/token/`
- **Endpoint de Registro:** `POST http://127.0.0.1:8000/api/v1/auth/register/`
- **Web Service Propio Protegido:** `GET http://127.0.0.1:8000/api/v1/auth/me/`
- **Consumo de Web Service SOAP (`zeep`):** `GET http://127.0.0.1:8000/api/v1/soap/pais/?codigo=MX`

### 3. Configurar y ejecutar el Frontend (React + Vite)

En una segunda terminal:

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

- **Aplicación React:** `http://localhost:5173/`
- **Login:** `http://localhost:5173/login`
- **Registro:** `http://localhost:5173/register`
- **Dashboard Protegido (AuthContext + API de Terceros + SOAP):** `http://localhost:5173/dashboard`

### 4. Ejecutar pruebas unitarias

```bash
python manage.py test users products
```
