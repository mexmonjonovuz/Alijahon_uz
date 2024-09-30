from django.db.models import TextChoices, IntegerField, CharField, SET_NULL, FloatField, Model, ImageField, \
    PositiveIntegerField, ForeignKey, CASCADE, BooleanField, DateField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import SlugBasedModel, TimeBasedModel, SlugTimeBasedModel


class Category(SlugBasedModel):
    image = ImageField(upload_to='categories/%Y/%m/%d')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = _('Categories')


class Product(SlugTimeBasedModel):
    description = CKEditor5Field('Text', config_name='extends')
    image = ImageField(upload_to='products/%Y/%m/%d/')
    price = PositiveIntegerField(db_default=0)
    quantity = PositiveIntegerField(db_default=0)
    discount_price = PositiveIntegerField(db_default=0)
    category = ForeignKey('apps.Category', CASCADE)

    class Meta:
        ordering = 'created_at',
        verbose_name = 'Product'
        verbose_name_plural = _('Products')


class Stream(TimeBasedModel):
    name = CharField(max_length=255)
    visit_count = PositiveIntegerField(db_default=0)
    discount = PositiveIntegerField(db_default=0)
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
    stream = ForeignKey('apps.Stream', SET_NULL, null=True, blank=True, related_name='orders', verbose_name='oqim')
    region = ForeignKey('apps.Region', SET_NULL, null=True, blank=True, related_name='orders', verbose_name='viloyat')
    district = ForeignKey('apps.District', SET_NULL, null=True, blank=True, related_name='orders', verbose_name='tuman')
    product = ForeignKey('apps.Product', CASCADE, related_name='orders', verbose_name='mahsulot')
    user = ForeignKey('apps.User', SET_NULL, null=True, blank=True, related_name='orders')
    # operator = ForeignKey('apps.User', SET_NULL, null=True, blank=True, related_name='orders')
    # currier = ForeignKey('apps.User', SET_NULL, null=True, blank=True, related_name='orders')

    def __str__(self):
        return self.status


class SiteSettings(Model):
    operator_sum = PositiveIntegerField(db_default=0, verbose_name="operator uchun to'lanadigan sum")
    delivery_price_regions = FloatField(db_default=0)
    delivery_price_tashkent_region = FloatField(db_default=0)
    delivery_price_tashkent = FloatField(db_default=0)
    minimum_sum = IntegerField(db_default=1000, verbose_name="eng kam yechib olinishi mumkun bo'lgam summa")


class Favorite(SlugTimeBasedModel):
    user = ForeignKey('apps.User', CASCADE, related_name='likes')
    product = ForeignKey('apps.Product', CASCADE, related_name='products')

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = _('Likes')

    @property
    def favorite_count(self):
        return self.user.likes.count()


class Meta:
    unique_together = ('user', 'product')


class Competition(Model):
    title = CKEditor5Field('text', config_name='extends')
    description = CKEditor5Field('text', config_name='extends')
    image = ImageField(upload_to='competition/%Y/%m/%d')
    start_date = DateField(null=True, blank=True)
    end_date = DateField(null=True, blank=True)
    is_active = BooleanField(db_default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Competition'
        verbose_name_plural = _('Competitions')


class Operator(TimeBasedModel):
    class Role(TextChoices):
        Operator = 'operator', _('Operator')
        SUPPORT = 'support', _('Support')

    user = ForeignKey('apps.User', on_delete=SET_NULL, null=True, blank=True, related_name='operators',
                      verbose_name=_('User'))
    role = CharField(max_length=20, choices=Role.choices, default=Role.SUPPORT, verbose_name=_('Role'))
    phone_number = CharField(max_length=20, blank=True, null=True, verbose_name=_('Phone Number'))
    is_active = BooleanField(default=False, verbose_name=_('Is Active'))
    passport = CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    class Meta:
        verbose_name = _('Operator')
        verbose_name_plural = _('Operators')
        unique_together = ('user', 'role')


class Transaction(TimeBasedModel):
    class Status(TextChoices):
        PROCESS = 'process', 'Process'
        CANCELED = 'canceled', 'Canceled'
        PAID = 'paid', 'Paid'
        ERROR = 'error', 'Error'

    user = ForeignKey('apps.User', SET_NULL, null=True)
    status = CharField(max_length=10, choices=Status.choices, default=Status.PROCESS)
    card_number = CharField(max_length=16)
    amount = PositiveIntegerField(db_default=0)
    text = CKEditor5Field('Text', config_name='extends', null=True, blank=True)
    check_image = ImageField(upload_to='transaction/%Y/%m/%d', null=True, blank=True)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = _('Transactions')
