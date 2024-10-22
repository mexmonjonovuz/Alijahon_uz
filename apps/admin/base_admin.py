from django.contrib import admin
from django.contrib.admin import ModelAdmin, register, StackedInline
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from apps.models import Category, Product, User, SiteSettings, Favorite, Competition, Order, District, Region, \
    Transaction, Operator
from apps.models.proxy.proxy import UserProxyModel, UserOperatorProxyModel, UserManagerProxyModel, UserAdminProxyModel, \
    UserCurrierProxyModel, OrderNewProxyModel, OrderReadyProxyModel, OrderDeliverProxyModel, OrderDeliveredProxyModel, \
    OrderCantPhoneProxyModel, OrderBrokenProxyModel, OrderCanceledProxyModel, OrderArchivedProxyModel


class OperatorStackedInline(StackedInline):
    model = Operator
    extra = 1
    max_num = 3


@register(User)
class UserModelAdmin(UserAdmin):
    list_display = 'phone', 'type', 'is_staff',
    inlines = [OperatorStackedInline]
    ordering = 'phone',
    fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "password", "email"),
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


@register(Category)
class CategoryModelAdmin(ModelAdmin):
    list_display = 'name', 'show_image',

    @admin.display(description='rasm')
    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="25" height="25" />', obj.image.url)
        return "No Image"

    show_image.allow_tags = True


@register(Product)
class ProductModelAdmin(ModelAdmin):
    list_display = 'name', 'show_image',

    @admin.display(description='rasm')
    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="30" height="30" />', obj.image.url)
        return "No Image"

    show_image.allow_tags = True


@register(Order)
class OrderModelAdmin(ModelAdmin):
    list_display = 'full_name', 'phone_number', 'status',


@register(Region)
class ReginModelAdmin(ModelAdmin):
    list_display = 'name',


@register(District)
class DistrictModelAdmin(ModelAdmin):
    list_display = 'name',


@register(SiteSettings)
class SiteSettingsModelAdmin(ModelAdmin):
    pass


@register(Favorite)
class FavouriteModelAdmin(ModelAdmin):
    pass


@register(Transaction)
class TransactionModelAdmin(ModelAdmin):
    pass


@register(Competition)
class CompetitionModelAdmin(ModelAdmin):
    pass


# PROXY USER

@register(UserProxyModel)
class UserProxyModelAdmin(ModelAdmin):
    list_display = 'phone', 'type',


@register(UserOperatorProxyModel)
class UserOperatorProxyModelAdmin(ModelAdmin):
    pass


@register(UserManagerProxyModel)
class UserManagerProxyModelAdmin(ModelAdmin):
    pass


@register(UserAdminProxyModel)
class UserAdminProxyModelAdmin(ModelAdmin):
    pass


@register(UserCurrierProxyModel)
class UserCurrierProxyModelAdmin(ModelAdmin):
    pass


# PROXY ORDER

@register(OrderNewProxyModel)
class OrderNewProxyModelAdmin(ModelAdmin):
    pass


@register(OrderReadyProxyModel)
class OrderReadyProxyModelAdmin(ModelAdmin):
    pass


@register(OrderDeliverProxyModel)
class OrderDeliverProxyModelAdmin(ModelAdmin):
    pass


@register(OrderDeliveredProxyModel)
class OrderDeliveredProxyModelAdmin(ModelAdmin):
    pass


@register(OrderCantPhoneProxyModel)
class OrderCantPhoneProxyModelAdmin(ModelAdmin):
    pass


@register(OrderBrokenProxyModel)
class OrderBrokenProxyModelAdmin(ModelAdmin):
    pass


@register(OrderCanceledProxyModel)
class OrderCanceledProxyModelAdmin(ModelAdmin):
    pass


@register(OrderArchivedProxyModel)
class OrderArchivedProxyModelAdmin(ModelAdmin):
    pass
