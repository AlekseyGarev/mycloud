import os
from django.core.management.base import BaseCommand, CommandError
from users.models import User


class Command(BaseCommand):
    help = 'Создаёт/обновляет начального администратора из ADMIN_* переменных окружения'

    def handle(self, *args, **options):
        username = os.getenv('ADMIN_USERNAME', 'admin')
        email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        password = os.getenv('ADMIN_INITIAL_PASSWORD')
        if not password:
            raise CommandError('Задайте ADMIN_INITIAL_PASSWORD в окружении перед запуском init_admin.')
        user, created = User.objects.get_or_create(username=username, defaults={'email': email, 'full_name': 'Системный администратор'})
        user.email = email
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Администратор {username} {'создан' if created else 'обновлён'}."))
