from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import CharField, Model, ForeignKey, CASCADE, ImageField, TextChoices, SET_NULL, BooleanField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from apps.models import TimeBasedModel
from apps.models.managers import CustomUserManager


class User(AbstractUser):
    class Type(TextChoices):
        OPERATOR = 'operator', 'Operator'
        MANAGER = 'manager', 'Manager'
        ADMIN = 'admin_side', 'Admin_side'
        DRIVER = 'currier', "Currier"
        USER = 'user', 'User'

    username = None
    email = None
    phone = CharField(max_length=12, unique=True)
    address = CharField(max_length=255, blank=True, null=True)
    telegram_id = CharField(max_length=30, blank=True, null=True, unique=True, validators=[
        RegexValidator(regex=r'^\d+$', message="Telegram ID must contain only numbers.")])
    bio = CKEditor5Field('Text', config_name='basic', null=True, blank=True)
    district = ForeignKey('District', CASCADE, blank=True, null=True)
    image = ImageField(upload_to='user/%Y/%m/%d/', default='default.jpg', blank=True)
    type = CharField(max_length=25, choices=Type.choices, default=Type.USER)
    # balance = PositiveIntegerField(db_default=0, verbose_name=_('foydalanuvchi balansi'))
    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone


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


class Region(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey('apps.Region', CASCADE, related_name='districts')

    def __str__(self):
        return self.name
