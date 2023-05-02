from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField
from django.core.validators import MinLengthValidator, RegexValidator

def validate_image_size(image):
    if image.size > 2 * 1024 * 1024:
        raise ValidationError('Image size should be less than 2MB.')

def validate_image_extension(image):
    ext = os.path.splitext(image.name)[1]
    if not ext.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
        raise ValidationError('Image must be in JPG, JPEG, or PNG format.')
    
phone_regex = RegexValidator(
        regex=r'^(?:\+20|0)?1\d{9}$',
        message="Phone number must be in the format '+201234567890' or '01234567890'"
)
        
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    image = CloudinaryField('images', validators=[validate_image_size, validate_image_extension])
    phone = models.CharField(max_length=13, validators=[phone_regex])
    confirm_password = models.CharField(max_length=255)

    def clean(self):
        super().clean()
        if self.password != self.confirm_password:
            raise ValidationError('Passwords do not match.')
    
    def __str__(self):
        return self.username
    
class Address(models.Model):
    country = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    city = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    district = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    street = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    building_number = models.CharField(max_length=10, validators=[MinLengthValidator(3)])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')

    def __str__(self):
        return f"{self.street}, {self.district}, {self.city}, {self.country}"
