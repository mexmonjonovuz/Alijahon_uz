from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html

from apps.forms import CustomAdminAuthenticationForm
from apps.models import Category, Product, User, SiteSettings, Favorite, Competition, Order, District, Region
from apps.models.proxy.proxy import OrderNewProxyModel, OrderReadyProxyModel, OrderDeliverProxyModel, \
    OrderDeliveredProxyModel, OrderCantPhoneProxyModel, OrderCanceledProxyModel, OrderArchivedProxyModel, \
    UserProxyModel, UserOperatorProxyModel, UserManagerProxyModel, UserAdminProxyModel, UserDriverProxyModel
from apps.models.shop import Transaction

admin.site.site_title = "Alijahon Admin Paneli"
admin.site.site_header = "Alijahon Administratsiyasi"
admin.site.index_title = "Xush kelibsiz! Alijahon Admin Paneli"


@register(User)
class UserModelAdmin(UserAdmin):
    list_display = 'phone', 'type', 'is_staff',
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
    list_filter = 'status',


#
# @register(Operator)
# class OperatorStackedInline(StackedInline):
#     class Meta:
#         model = UserModelAdmin

@register(Region)
class ReginModelAdmin(ModelAdmin):
    pass


@register(District)
class DistrictModelAdmin(ModelAdmin):
    pass


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


def get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request, app_label)

    app_ordering = {
        "Apps": 1,
    }

    model_ordering = {
        'Users': -1,
        'Competition': 1,
        'SiteSettings': 2,
    }

    app_list = sorted(app_dict.values(), key=lambda x: app_ordering.get(x["name"], 1000))

    for app in app_list:
        app["models"].sort(key=lambda x: model_ordering.get(x['object_name'], 1000))

    return app_list


admin.AdminSite.get_app_list = get_app_list


@register(UserOperatorProxyModel)
class UserOperatorProxyModelUserAdmin(UserModelAdmin):
    pass


admin.site.login_form = CustomAdminAuthenticationForm
admin.site.unregister(Group)
admin.site.register(UserProxyModel)
# admin.site.register(UserOperatorProxyModel)
admin.site.register(UserManagerProxyModel)
admin.site.register(UserAdminProxyModel)
admin.site.register(UserDriverProxyModel)
admin.site.register(OrderNewProxyModel)
admin.site.register(OrderReadyProxyModel)
admin.site.register(OrderDeliverProxyModel)
admin.site.register(OrderDeliveredProxyModel)
admin.site.register(OrderCantPhoneProxyModel)

admin.site.register(OrderCanceledProxyModel)
admin.site.register(OrderArchivedProxyModel)
