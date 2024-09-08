from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, Model, ForeignKey, CASCADE
from django_ckeditor_5.fields import CKEditor5Field


class Region(Model):
    name = CharField(max_length=255)


class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey('Region', CASCADE, related_name='districts')


class User(AbstractUser):
    phone = CharField(max_length=12, unique=True)
    address = CharField(max_length=255, blank=True, null=True)
    telegram_id = CharField(max_length=30, blank=True, null=True)
    bio = CKEditor5Field('Text', config_name='basic', null=True, blank=True)
    district = ForeignKey('District', CASCADE, blank=True, null=True)
