from django.contrib import admin
from django.contrib.auth.models import Group

from apps.forms import CustomAdminAuthenticationForm

admin.site.site_title = "Alijahon Admin Paneli"
admin.site.site_header = "Alijahon Administratsiyasi"
admin.site.index_title = "Xush kelibsiz! Alijahon Admin Paneli"


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

    app_list.extend(new_apps.values())
    return app_list


admin.AdminSite.get_app_list = get_app_list

admin.site.login_form = CustomAdminAuthenticationForm
admin.site.unregister(Group)
