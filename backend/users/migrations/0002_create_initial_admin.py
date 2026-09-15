import os
from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_initial_admin(apps, schema_editor):
    User = apps.get_model('users', 'User')
    username = os.getenv('ADMIN_USERNAME', 'admin')
    email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    password = os.getenv('ADMIN_INITIAL_PASSWORD')
    if User.objects.filter(username=username).exists():
        return
    user = User(username=username, email=email, full_name='Системный администратор', is_admin=True, is_staff=True, is_superuser=True)
    user.password = make_password(password) if password else make_password(None)
    user.save()


class Migration(migrations.Migration):
    dependencies = [('users', '0001_initial')]
    operations = [migrations.RunPython(create_initial_admin, migrations.RunPython.noop)]
