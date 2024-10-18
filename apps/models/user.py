from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import CharField, Model, ForeignKey, CASCADE, ImageField, TextChoices, SET_NULL, \
    PositiveIntegerField, DateField, OneToOneField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from apps.models import TimeBasedModel
from apps.models.managers import CustomUserManager


class User(AbstractUser):
    class Type(TextChoices):
        OPERATOR = 'operator', _('Operator')
        MANAGER = 'manager', _('Manager')
        ADMIN = 'admin_side', _('Admin_side')
        CURRIER = 'currier', _("Currier")
        USER = 'user', _('User')

    username = None
    email = None
    phone = CharField(max_length=12, unique=True, verbose_name=_("phone number"))
    address = CharField(max_length=255, blank=True, null=True, verbose_name=_("address"))
    telegram_id = CharField(max_length=30, blank=True, null=True, unique=True, validators=[
        RegexValidator(regex=r'^\d+$', message="Telegram ID must contain only numbers.")],
                            verbose_name=_("telegram id"))
    bio = CKEditor5Field('Text', config_name='extends', null=True, blank=True)
    district = ForeignKey('District', CASCADE, blank=True, null=True)
    image = ImageField(upload_to='user/%Y/%m/%d/', default='default.jpg', blank=True, verbose_name=_("image"))
    type = CharField(max_length=25, choices=Type.choices, default=Type.USER, verbose_name=_("user type"))
    balance = PositiveIntegerField(db_default=0, verbose_name=_('user balance'))
    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone


class Operator(TimeBasedModel):
    user = OneToOneField('apps.User', on_delete=SET_NULL, null=True, blank=True, related_name='operators',
                         verbose_name=_('User'), limit_choices_to={'type': 'Operator'})
    passport = CharField(max_length=30, unique=True, verbose_name=_("passport for operator"))
    start_date = DateField(null=True, blank=True, verbose_name=_('time to start work'))
    end_date = DateField(null=True, blank=True, verbose_name=_('time to end work'))

    class Meta:
        verbose_name = _('Operator')
        verbose_name_plural = _('Operators')


class Region(Model):
    name = CharField(max_length=255, verbose_name=_("region name"))

    def __str__(self):
        return self.name


class District(Model):
    name = CharField(max_length=255, verbose_name=_("district name"))
    region = ForeignKey('apps.Region', CASCADE, related_name='districts')

    def __str__(self):
        return self.name
