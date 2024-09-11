from django.db.models import ImageField, PositiveIntegerField, ForeignKey, CASCADE
from django.db.models import TextChoices, IntegerField, CharField, SET_NULL, FloatField, Model
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import SlugBasedModel, TimeBasedModel, SlugTimeBasedModel


class Category(SlugBasedModel):
    image = ImageField(upload_to='categories/%Y/%m/%d')


class Product(SlugTimeBasedModel):
    description = CKEditor5Field('Text', config_name='extends')
    image = ImageField(upload_to='products/%Y/%m/%d/')
    price = PositiveIntegerField(db_default=0)
    quantity = PositiveIntegerField(db_default=0)
    discount_price = PositiveIntegerField(db_default=0)
    category = ForeignKey('apps.Category', CASCADE)


class Stream(TimeBasedModel):
    name = CharField(max_length=255)
    count = IntegerField(default=0)
    discount = IntegerField()
    product = ForeignKey('apps.Product', CASCADE, related_name='streams')
    owner = ForeignKey('apps.User', CASCADE, related_name='streams')

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.name


class Order(TimeBasedModel):
    class StatusType(TextChoices):
        NEW = 'new', 'New'
        READY = "ready", 'Ready'
        DELIVER = "deliver", 'Deliver'
        DELIVERED = "delivered", 'Delivered'
        CANT_PHONE = "cant_phone", 'Cant_phone'
        CANCELED = "canceled", 'Canceled'
        ARCHIVED = "archived", 'Archived'

    quantity = IntegerField(db_default=1)
    status = CharField(max_length=50, choices=StatusType.choices, default=StatusType.NEW)
    full_name = CharField(max_length=255)
    phone_number = CharField(max_length=20)
    stream = ForeignKey('apps.Stream', SET_NULL, null=True, blank=True, related_name='orders')
    region = ForeignKey('apps.Region', CASCADE, null=True, blank=True, related_name='orders')
    district = ForeignKey('apps.District', CASCADE, null=True, blank=True, related_name='orders')
    product = ForeignKey('apps.Product', CASCADE, related_name='orders')
    user = ForeignKey('apps.User', CASCADE, null=True, blank=True, related_name='orders')


class SiteSettings(Model):
    delivery_price_regions = FloatField(db_default=0)
    delivery_price_tashkent_region = FloatField(db_default=0)
    delivery_price_tashkent = FloatField(db_default=0)
