from django.db.models import ImageField

from apps.models.base import SlugBaseModel

class Category(SlugBaseModel):
    image = ImageField(upload_to='categories',)
