from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
import os

def validate_image_size(image):
    if image.size > 2 * 1024 * 1024:
        raise ValidationError('Image size should be less than 2MB.')

def validate_image_extension(image):
    ext = os.path.splitext(image.name)[1]
    if not ext.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
        raise ValidationError('Image must be in JPG, JPEG, or PNG format.')

class Category(models.Model):
    name = models.CharField(max_length=30, validators=[MinLengthValidator(3)])
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100 ,validators=[MinLengthValidator(3)])
    description = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    image = CloudinaryField('images', validators=[validate_image_size, validate_image_extension])
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    
    def __str__(self):
        return self.name
    

