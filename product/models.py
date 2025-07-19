from django.db import models
from django.contrib.auth import get_user_model
from custom_auth.validator import image_validator
from django.utils.html import format_html
User = get_user_model()

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_%(class)ss')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT,  related_name='updated_%(class)ss', null=True, blank=True)

    class Meta:
        abstract = True

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self.__class__.__name__._meta.fields]


class Product(BaseModel):
    title = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    stock = models.DecimalField(max_digits=8, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    thumbnail = models.ImageField(upload_to='product_images/', validators=[image_validator], blank=True, null=True, help_text='Must be .jpeg .jpg .png Format and Size should not exceed 2 MiB.')

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.title
    
    def product_image(self):
        return format_html('<img src="/media/{}" width = "50" height = "50"/>', self.thumbnail)