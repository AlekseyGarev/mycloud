import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


def default_storage_path():
    # Генерируем уникальное имя папки для пользователя
    return str(uuid.uuid4())


class User(AbstractUser):
    # AbstractUser уже содержит: username, password, email, first_name, last_name, is_staff, is_superuser
    full_name = models.CharField(max_length=255, verbose_name="Полное имя")
    is_admin = models.BooleanField(default=False, verbose_name="Признак администратора")
    storage_path = models.CharField(
        max_length=255,
        unique=True,
        default=default_storage_path,
        verbose_name="Путь к хранилищу"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username} ({self.email})"