from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, Model, ForeignKey, CASCADE, ImageField, TextChoices
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.managers import CustomUserManager


class Region(Model):
    name = CharField(max_length=255)


class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey('Region', CASCADE, related_name='districts')


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
    telegram_id = CharField(max_length=30, blank=True, null=True)
    bio = CKEditor5Field('Text', config_name='basic', null=True, blank=True)
    district = ForeignKey('District', CASCADE, blank=True, null=True)
    image = ImageField(upload_to='user/%Y/%m/%d/', default='apps/assets/img/team/default.jpg', blank=True)
    type = CharField(max_length=25, choices=Type.choices, default=Type.USER)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []
