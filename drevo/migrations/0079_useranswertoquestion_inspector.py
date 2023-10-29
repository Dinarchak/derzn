# Generated by Django 3.2.4 on 2023-10-14 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drevo', '0078_merge_20231003_2326'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswertoquestion',
            name='inspector',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='inspector', to=settings.AUTH_USER_MODEL, verbose_name='Проверил эксперт'),
        ),
    ]
