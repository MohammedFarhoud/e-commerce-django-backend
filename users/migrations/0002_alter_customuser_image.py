# Generated by Django 4.2 on 2023-05-16 16:54

import cloudinary.models
from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=cloudinary.models.CloudinaryField(default='ljpmwdkm1wz1sagqsk5f', max_length=255, validators=[users.models.validate_image_size, users.models.validate_image_extension], verbose_name='images'),
        ),
    ]
