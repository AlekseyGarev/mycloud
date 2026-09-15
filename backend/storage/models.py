import os
import uuid
from django.conf import settings
from django.db import models


def user_directory_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    unique_name = f'{uuid.uuid4().hex}{ext}'
    return os.path.join('user_files', instance.user.storage_path, unique_name)


class File(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='files', verbose_name='Владелец')
    original_name = models.CharField(max_length=255, verbose_name='Оригинальное имя')
    file = models.FileField(upload_to=user_directory_path, verbose_name='Файл на диске')
    size = models.BigIntegerField(verbose_name='Размер (в байтах)')
    comment = models.TextField(blank=True, default='', verbose_name='Комментарий')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    last_downloaded_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата последнего скачивания')
    share_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name='Токен доступа')

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'{self.original_name} ({self.user.username})'
