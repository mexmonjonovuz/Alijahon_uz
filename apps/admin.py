from django.contrib import admin
from django.contrib.admin import ModelAdmin, register, StackedInline
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html

from apps.forms import CustomAdminAuthenticationForm
from apps.models import Category, Product, User, SiteSettings, Favorite, Competition, Order, District, Region, \
    Transaction, Operator
from apps.models.proxy.proxy import OrderNewProxyModel, OrderReadyProxyModel, OrderDeliverProxyModel, \
    OrderDeliveredProxyModel, OrderCantPhoneProxyModel, OrderCanceledProxyModel, OrderArchivedProxyModel, \
    UserProxyModel, UserOperatorProxyModel, UserManagerProxyModel, UserAdminProxyModel, UserCurrierProxyModel

admin.site.site_title = "Alijahon Admin Paneli"
admin.site.site_header = "Alijahon Administratsiyasi"
admin.site.index_title = "Xush kelibsiz! Alijahon Admin Paneli"


class OperatorStackedInline(StackedInline):
    model = Operator
    extra = 1


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


def get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request)
    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
    if not request.user.is_superuser:
        return app_list
    models = app_list[0].pop('models')
    app_list[0]['models'] = list()

    new_apps = {
        'Order Status': {
            'name': "Order Status",
            "app_label": 'Order Status',
            'models': list()
        },
        'Users App': {
            'name': "Users App",
            "app_label": 'Users App',
            'models': list()
        },
        'SiteSettings': {
            'name': "SiteSettings App",
            "app_label": 'SiteSettings',
            'models': list()
        },
    }
    model_order = {
        'Orders': "Order Status",
        "OrderNewProxyModel": "Order Status",
        "OrderReadyProxyModel": "Order Status",
        "OrderDeliverProxyModel": "Order Status",
        "OrderDeliveredProxyModel": "Order Status",
        "OrderCantPhoneProxyModel": "Order Status",
        "OrderCanceledProxyModel": "Order Status",
        "OrderArchivedProxyModel": "Order Status",
        'UserOperatorProxyModel': "Users App",
        "UserProxyModel": "Users App",
        "UserCurrierProxyModel": "Users App",
        "Categories": "Others",
        "Products": "Others",
        "Regions": "Regions",
        "Districts": "Regions",
        "UserManagerProxyModel": "Users App",
        "UserAdminProxyModel": "Users App",
        "Transactions": "SiteSettings",
        'SiteSettings': "SiteSettings",
        "Likes": "SiteSettings",
        'Competition': "SiteSettings",
    }
    for model__ in models:
        if model__['object_name'] in model_order.keys():
            new_apps[model_order[model__['object_name']]]['models'].append(model__)
        else:
            app_list[0]['models'].append(model__)

    app_list.extend(new_apps.values())
    return app_list


admin.AdminSite.get_app_list = get_app_list

admin.site.login_form = CustomAdminAuthenticationForm
admin.site.unregister(Group)

# USER
admin.site.register(UserProxyModel)
admin.site.register(UserOperatorProxyModel)
admin.site.register(UserManagerProxyModel)
admin.site.register(UserAdminProxyModel)
admin.site.register(UserCurrierProxyModel)

# ORDER
admin.site.register(OrderNewProxyModel)
admin.site.register(OrderReadyProxyModel)
admin.site.register(OrderDeliverProxyModel)
admin.site.register(OrderDeliveredProxyModel)
admin.site.register(OrderCantPhoneProxyModel)
admin.site.register(OrderCanceledProxyModel)
admin.site.register(OrderArchivedProxyModel)
