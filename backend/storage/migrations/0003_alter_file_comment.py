from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('storage', '0002_initial')]
    operations = [
        migrations.AlterField(
            model_name='file',
            name='comment',
            field=models.TextField(blank=True, default='', verbose_name='Комментарий'),
        ),
    ]
