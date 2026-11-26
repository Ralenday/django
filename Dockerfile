# Imagen base de Python (Django 6 requiere Python 3.12 o superior)
FROM python:3.13-slim

# Evita archivos .pyc y muestra los logs de Django al momento
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Librerías del sistema que necesita mysqlclient para conectarse a MySQL
RUN apt-get update && apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev build-essential pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Primero solo requirements.txt para aprovechar la caché de capas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código del backend
COPY . .

EXPOSE 8000

# Aplica las migraciones y arranca Django escuchando en todas las interfaces
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
