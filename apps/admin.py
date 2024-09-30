from django.contrib import admin
from django.contrib.admin import AdminSite, StackedInline
from django.contrib.admin import ModelAdmin, register
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apps.forms import CustomAdminAuthenticationForm
from apps.models import Category, Product, User, Region, District, SiteSettings, Favorite, Competition, Operator
from apps.proxy import OrderNewProxyModel, OrderReadyProxyModel, OrderDeliverProxyModel, \
    OrderDeliveredProxyModel, OrderCantPhoneProxyModel, OrderCanceledProxyModel, OrderArchivedProxyModel, \
    UserProxyModel, UserOperatorProxyModel, UserManagerProxyModel, UserAdminProxyModel, UserDriverProxyModel


@register(User)
class UserModelAdmin(UserAdmin):
    list_display = 'phone', 'type', 'is_staff',
    ordering = 'phone',
    # add_form = UserAuthenticatedForm
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


# @register(Operator)
# class OperatorStackedInline(StackedInline):
#     pass


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


@register(Competition)
class CompetitionModelAdmin(ModelAdmin):
    pass


class MyAdminSite(AdminSite):
    admin.site.index_title = _('Alijahon Title')
    admin.site.site_header = _('Alijahon Site Administration')
    admin.site.site_title = _('Alijahon Site Management')

    def get_app_list(self, request, app_label=None):
        app_dict = self._build_app_dict(request, app_label)

        app_ordering = {
            "Authentication and Authorization": 1,
            "Apps": 2,
            "Catalog": 3,
            "Site Management": 4,
            "Competitions": 5,
            "User Roles": 6,
            "Orders": 7,
        }
        model_ordering = {
            "Groups": 1,
            "Users": 2,

            # Apps
            "Apps": 1,

            # Catalog
            "Categorys": 1,
            "Products": 2,
            "Regions": 3,
            "Districts": 4,
            "Favorites": 5,

            # Site Management
            "Site settingss": 1,

            # Competitions
            "Competitions": 1,

            # User Roles
            "Foydalanuvchilar uchun": 1,
            "Operatorlar uchun": 2,
            "Managerlar uchun": 3,
            "Adminlar uchun": 4,
            "Yetqazuvchilar uchun": 5,

            # Orders
            "Yangi buyurtmalar": 1,
            "Buyurtmalar tayyor": 2,
            "Yetkazib berishga tayyor buyurtmalar": 3,
            "Yetkazib berilgan buyurtmalar": 4,
            "Telefon orqali bog‘lanib bo‘lmagan buyurtmalar": 5,
            "Bekor qilingan buyurtmalar": 6,
            "Arxivlangan buyurtmalar": 7,
        }

        app_list = sorted(
            app_dict.values(),
            key=lambda x: app_ordering.get(x["name"], 1000)
        )

        for app in app_list:
            app["models"].sort(
                key=lambda x: model_ordering.get(x["name"].upper(), 1000)
            )

        return app_list

    admin.AdminSite.get_app_list = get_app_list


admin.site.login_form = CustomAdminAuthenticationForm
# admin.site.unregister(Group)
admin.site.register(UserProxyModel)
admin.site.register(UserOperatorProxyModel)
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
