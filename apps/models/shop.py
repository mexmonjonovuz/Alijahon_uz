from django.db.models import TextChoices, IntegerField, CharField, SET_NULL, FloatField, Model, ImageField, \
    PositiveIntegerField, ForeignKey, CASCADE, BooleanField, DateField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import SlugBasedModel, TimeBasedModel, SlugTimeBasedModel
from .user import User


class Category(SlugBasedModel):
    image = ImageField(upload_to='categories/%Y/%m/%d', verbose_name=_("Category image"))

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = _('Categories')


class Product(SlugTimeBasedModel):
    description = CKEditor5Field('Text', config_name='extends')
    image = ImageField(upload_to='products/%Y/%m/%d/', verbose_name=_("image"))
    price = PositiveIntegerField(db_default=0, verbose_name=_("price"))
    quantity = PositiveIntegerField(db_default=0, verbose_name=_("quantity"))
    discount_price = PositiveIntegerField(db_default=0, verbose_name=_("discount_price"))
    # stream_discount = PositiveIntegerField(db_default=0,verbose_name=_("discount_stream_price"))
    category = ForeignKey('apps.Category', CASCADE)

    class Meta:
        ordering = 'created_at',
        verbose_name = 'Product'
        verbose_name_plural = _('Products')


class Stream(TimeBasedModel):
    name = CharField(max_length=255, verbose_name=_("stream"))
    visit_count = PositiveIntegerField(db_default=0, verbose_name=_("visit_count"))
    discount = PositiveIntegerField(db_default=0, verbose_name=_("discount"))
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
        NEW = 'new', _('New')
        READY = "ready", _('Ready')
        DELIVERING = "delivering", _('Delivering')
        DELIVERED = "delivered", _('Delivered')
        CANT_PHONE = "cant_phone", _('Cant_phone')
        BROKEN = "broken", _('Broken')
        CANCELED = "canceled", _('Canceled')
        ARCHIVED = "archived", _('Archived')

    quantity = IntegerField(db_default=1, verbose_name=_("quantity"))
    status = CharField(max_length=50, choices=StatusType.choices, default=StatusType.NEW, verbose_name=_("status"))
    full_name = CharField(max_length=255, verbose_name=_("full name"))
    phone_number = CharField(max_length=20, verbose_name=_("phone number"))
    stream = ForeignKey('apps.Stream', SET_NULL, null=True, blank=True, related_name='orders', verbose_name=_('stream'))
    region = ForeignKey('apps.Region', SET_NULL, null=True, blank=True, related_name='orders', verbose_name=_('region'))
    district = ForeignKey('apps.District', SET_NULL, null=True, blank=True, related_name='orders',
                          verbose_name=_('district'))
    product = ForeignKey('apps.Product', CASCADE, related_name='orders', verbose_name=_('product'))
    user = ForeignKey('apps.User', SET_NULL, null=True, blank=True, related_name='orders')
    operator = ForeignKey('apps.User', SET_NULL, null=True, blank=True, verbose_name=_('operator'),
                          related_name='operator_order', limit_choices_to={'type': User.Type.OPERATOR})
    currier = ForeignKey('apps.User', SET_NULL, null=True, blank=True, verbose_name=_('currier'),
                         related_name='currier_order', limit_choices_to={'type': User.Type.CURRIER})
    referral_user = ForeignKey('apps.User', SET_NULL, null=True, blank=True, related_name='referral_user')
    send_order_date = DateField(null=True, blank=True, verbose_name=_("send order date"))
    address = CharField(max_length=255, null=True, blank=True, verbose_name=_("address for order"))
    comment_operator = CharField(max_length=255, null=True, blank=True,
                                 verbose_name=_("the operator's comment for the order"))

    def __str__(self):
        return self.status

    @property
    def order_count(self):
        return self.status.count('new')


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
    image = ImageField(upload_to='competition/%Y/%m/%d', verbose_name=_("Competition image"))
    start_date = DateField(null=True, blank=True, verbose_name=_("Competition start time"))
    end_date = DateField(null=True, blank=True, verbose_name=_("Competition end time"))
    is_active = BooleanField(db_default=False, verbose_name=_("Active competitions"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Competition'
        verbose_name_plural = _('Competitions')


class Transaction(TimeBasedModel):
    class Status(TextChoices):
        PROCESS = 'process', _('Process')
        CANCELED = 'canceled', _('Canceled')
        PAID = 'paid', _('Paid')
        ERROR = 'error', _('Error')

    user = ForeignKey('apps.User', SET_NULL, null=True)
    status = CharField(max_length=10, choices=Status.choices, default=Status.PROCESS,
                       verbose_name=_("Transaction status"))
    card_number = CharField(max_length=19, verbose_name=_("Transaction card for user"))
    amount = PositiveIntegerField(db_default=0, verbose_name=_("Transaction amount"))
    text = CharField(max_length=255, null=True, blank=True, verbose_name=_("Transaction description"))
    check_image = ImageField(upload_to='transaction/%Y/%m/%d', null=True, blank=True,
                             verbose_name=_("Transaction image check"))

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = _("Transactions")


class SiteSettings(Model):
    operator_sum = PositiveIntegerField(db_default=0, verbose_name=_('Operators price'))
    delivery_price_regions = FloatField(db_default=0, verbose_name=_("delivery price for regions"))
    delivery_price_tashkent_region = FloatField(db_default=0, verbose_name=_("delivery price for tashkent regions"))
    delivery_price_tashkent = FloatField(db_default=0, verbose_name=_("delivery price for tashkent"))
    minimum_sum = IntegerField(db_default=1000, verbose_name=_('Minimum transaction sum'))
    operator_repression = IntegerField(db_default=0, verbose_name=_('Operators repression sum'))

    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = _('Site Settings')

    @property
    def operator_rep(self):
        return self.operator_repression
