from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_initial_admin(apps, schema_editor):
    User = apps.get_model("users", "User")

    if not User.objects.filter(username="admin").exists():
        User.objects.create(
            username="admin",
            password=make_password(None),
            full_name="Администратор",
            email="admin@example.com",
            is_admin=True,
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )


def remove_initial_admin(apps, schema_editor):
    User = apps.get_model("users", "User")
    User.objects.filter(username="admin").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_initial_admin,
            remove_initial_admin,
        ),
    ]
