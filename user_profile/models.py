from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.html import format_html
from PIL import Image
from django.contrib.auth import get_user_model
from custom_auth.validator import image_validator
User = get_user_model()

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    billing_address = models.TextField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', validators=[image_validator], blank=True, null=True, help_text='Must be .jpeg .jpg .png Format and Size should not exceed 2 MiB.')


    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_%(class)ss')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT,  related_name='updated_%(class)ss', null=True, blank=True)
    
    def __str__(self):
        return self.user.username

    def image_tag(self):
        return format_html('<img src="/media/{}" width = "50" height = "50"/>', self.profile_picture)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        try:
            if self.profile_picture:
                img = Image.open(self.profile_picture.path)
                if img.height > 300 or img.width > 300:
                    image_size = (300, 300)
                    img.thumbnail(image_size)
                    img.save(self.profile_picture.path)
        except Exception as e:
            pass
            # print(str(e))