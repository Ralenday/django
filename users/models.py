from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
    telefono = models.CharField(
        max_length=20,
        blank=True,
        default='',
        verbose_name='Teléfono',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
