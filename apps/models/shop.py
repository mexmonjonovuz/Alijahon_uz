from django.db.models import TextChoices, IntegerField, CharField, SET_NULL, FloatField, Model, ImageField, \
    PositiveIntegerField, ForeignKey, CASCADE, BooleanField, DateField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import SlugBasedModel, TimeBasedModel, SlugTimeBasedModel
from .user import User


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

    @property
    def sale_price(self):
        return self.product.price - self.discount


class Order(TimeBasedModel):
    class StatusType(TextChoices):
        NEW = 'new', 'New'
        READY = "ready", 'Ready'
        DELIVER = "deliver", 'Deliver'
        DELIVERED = "delivered", 'Delivered'
        CANT_PHONE = "cant_phone", 'Cant_phone'
        BROKEN = "broken", 'Broken'
        CANCELED = "canceled", 'Canceled'
        ARCHIVED = "archived", 'Archived'

    quantity = IntegerField(db_default=1)
    status = CharField(max_length=50, choices=StatusType.choices, default=StatusType.NEW)
    full_name = CharField(max_length=255)
    phone_number = CharField(max_length=20)
    stream = ForeignKey('apps.Stream', SET_NULL, null=True, blank=True, related_name='orders', verbose_name=_('stream'))
    region = ForeignKey('apps.Region', SET_NULL, null=True, blank=True, related_name='orders', verbose_name=_('region'))
    district = ForeignKey('apps.District', SET_NULL, null=True, blank=True, related_name='orders',
                          verbose_name=_('district'))
    product = ForeignKey('apps.Product', CASCADE, related_name='orders', verbose_name=_('product'))
    user = ForeignKey('apps.User', SET_NULL, null=True, blank=True, related_name='orders')
    operator = ForeignKey('apps.User', SET_NULL, null=True, blank=True, verbose_name=_('operator'),
                          related_name='currier_order', limit_choices_to={'type': User.Type.OPERATOR})
    currier = ForeignKey('apps.User', SET_NULL, null=True, blank=True, verbose_name=_('currier'),
                         related_name='operator_order', limit_choices_to={'type': User.Type.DRIVER})
    referral_user = ForeignKey('apps.User', SET_NULL, null=True, blank=True, related_name='referral_user')
    send_order_date = DateField(null=True, blank=True)
    address = CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.status


class Favorite(SlugTimeBasedModel):
    user = ForeignKey('apps.User', CASCADE, related_name='likes')
    product = ForeignKey('apps.Product', CASCADE, related_name='products')

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = _('Likes')
        unique_together = ('user', 'product')

    @property
    def favorite_count(self):
        return self.user.likes.count()


class Competition(TimeBasedModel):
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


class Transaction(TimeBasedModel):
    class Status(TextChoices):
        PROCESS = 'process', 'Process'
        CANCELED = 'canceled', 'Canceled'
        PAID = 'paid', 'Paid'
        ERROR = 'error', 'Error'

    user = ForeignKey('apps.User', SET_NULL, null=True)
    status = CharField(max_length=10, choices=Status.choices, default=Status.PROCESS)
    card_number = CharField(max_length=19)
    amount = PositiveIntegerField(db_default=0)
    text = CharField(max_length=255, null=True, blank=True)
    check_image = ImageField(upload_to='transaction/%Y/%m/%d', null=True, blank=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = _("Transactions")


class SiteSettings(Model):
    operator_sum = PositiveIntegerField(db_default=0, verbose_name=_('Operators price'))
    delivery_price_regions = FloatField(db_default=0)
    delivery_price_tashkent_region = FloatField(db_default=0)
    delivery_price_tashkent = FloatField(db_default=0)
    minimum_sum = IntegerField(db_default=1000, verbose_name=_('Minimum transaction sum'))
    operator_repression = IntegerField(db_default=0, verbose_name=_('Operators repression sum'))

    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = _('Site Settings')
