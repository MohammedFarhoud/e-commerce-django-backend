# Generated by Django 4.2 on 2023-05-02 17:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be in the format '+201234567890' or '01234567890'", regex='^(?:\\+20|0)?1\\d{9}$')]),
        ),
    ]