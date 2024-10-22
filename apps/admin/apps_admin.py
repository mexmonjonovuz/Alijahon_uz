from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.forms import CustomAdminAuthenticationForm


class MyAdminSite(AdminSite):
    site_header = _("Alijahon Admin Paneli")
    site_title = _("Alijahon Administratsiyasi")
    index_title = _("Xush kelibsiz! Alijahon Admin Paneli")
    login_form = CustomAdminAuthenticationForm

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        urls = [
                   path('valijon', self.admin_view(self.custom_page), name='valijon')
               ] + urls
        return urls

    def custom_page(self, request):
        context = {"text": "Hello python",
                   "page_name": "Custom Page",
                   "app_list": self.get_app_list(request),
                   **self.each_context(request),
                   }

        return TemplateResponse(request, "admin/custom_page.html", context)

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
            "OrderBrokenProxyModel": "Order Status",
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

        stats = {
            'name': 'Valijonga uish',
            'admin_url': reverse('admin:valijon'),
            'object_name': 'Stats',
            'perms': {'delete': False, 'add': False, 'change': False},
            'add_url': ''
        }

        app_list.extend(new_apps.values())
        app_list[-1]['models'].append(stats)

        return app_list


admin_site = MyAdminSite()


def site_register(*models, site=None):
    def _model_admin_wrapper(admin_class):
        if not models:
            raise ValueError("At least one model must be passed to register.")

        admin_site.register(models, admin_class=admin_class)
        return admin_class

    return _model_admin_wrapper
