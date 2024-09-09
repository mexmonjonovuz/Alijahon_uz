from django.contrib.admin import ModelAdmin, register
from django.contrib.auth.admin import UserAdmin

from apps.models import Category, Product, User


@register(User)
class UserModelAdmin(UserAdmin):
    ordering = 'phone',

@register(Category)
class CategoryModelAdmin(ModelAdmin):
    exclude = 'slug',


@register(Product)
class ProductModelAdmin(ModelAdmin):
    pass
