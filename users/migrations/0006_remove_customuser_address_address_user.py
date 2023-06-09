# Generated by Django 4.2 on 2023-05-16 22:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_address_user_customuser_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='address',
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL),
        ),
    ]
