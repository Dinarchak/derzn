# Generated by Django 4.1.1 on 2022-09-17 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drevo', '0019_friendsterm'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendsInviteTerm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accept', models.BooleanField(verbose_name='Принято')),
                ('date_added', models.DateField(auto_now=True, verbose_name='Дата отправки')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL, verbose_name='Получатель')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
            ],
        ),
    ]
