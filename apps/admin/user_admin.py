from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from apps.admin.apps_admin import site_register
from apps.models import Category, Product, User, SiteSettings, Favorite, Competition, Order, District, Region, \
    Transaction, Operator
from apps.models.proxy.proxy import UserProxyModel, UserOperatorProxyModel, UserManagerProxyModel, UserAdminProxyModel, \
    UserCurrierProxyModel


class OperatorStackedInline(StackedInline):
    model = Operator
    extra = 1
    max_num = 3


@site_register(User)
class UserModelAdmin(UserAdmin):
    list_display = 'phone', 'type', 'is_staff',
    inlines = [OperatorStackedInline]
    ordering = 'phone',
    search_fields = ("phone", "first_name", "last_name")
    fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "password"),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "password1", "password2"),
            },
        ),
    )

    class Media:
        js = (
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jquery.inputmask/5.0.6/jquery.inputmask.min.js",
            "admin/js/phone_input.js"
        )


@site_register(Category)
class CategoryModelAdmin(ModelAdmin):
    list_display = 'name', 'show_image',

    @admin.display(description='rasm')
    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="25" height="25" />', obj.image.url)
        return "No Image"

    show_image.allow_tags = True


@site_register(Product)
class ProductModelAdmin(ModelAdmin):
    list_display = 'name', 'show_image',

    @admin.display(description='rasm')
    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="30" height="30" />', obj.image.url)
        return "No Image"

    show_image.allow_tags = True


@site_register(Order)
class OrderModelAdmin(ModelAdmin):
    list_display = 'full_name', 'phone_number', 'status',


@site_register(Region)
class ReginModelAdmin(ModelAdmin):
    list_display = 'name',


@site_register(District)
class DistrictModelAdmin(ModelAdmin):
    list_display = 'name',


@site_register(SiteSettings)
class SiteSettingsModelAdmin(ModelAdmin):
    pass


@site_register(Favorite)
class FavouriteModelAdmin(ModelAdmin):
    pass


@site_register(Transaction)
class TransactionModelAdmin(ModelAdmin):
    pass


@site_register(Competition)
class CompetitionModelAdmin(ModelAdmin):
    pass


# PROXY USER

@site_register(UserProxyModel)
class UserProxyModelAdmin(UserModelAdmin):
    list_display = 'phone', 'type',


@site_register(UserOperatorProxyModel)
class UserOperatorProxyModelAdmin(UserModelAdmin):
    pass


@site_register(UserManagerProxyModel)
class UserManagerProxyModelAdmin(ModelAdmin):
    pass


@site_register(UserAdminProxyModel)
class UserAdminProxyModelAdmin(ModelAdmin):
    pass


@site_register(UserCurrierProxyModel)
class UserCurrierProxyModelAdmin(ModelAdmin):
    pass
