from django.db.models import ImageField, PositiveIntegerField, DateTimeField, ForeignKey, CASCADE
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import SlugBaseModel


class Product(SlugBaseModel):
    description = CKEditor5Field('Text', config_name='extends')
    image = ImageField(upload_to='products/%Y/%m/%d/')
    price = PositiveIntegerField(db_default=0)
    quantity = PositiveIntegerField(db_default=0)
    discount_price = PositiveIntegerField(db_default=0)
    category = ForeignKey('Category', CASCADE)
