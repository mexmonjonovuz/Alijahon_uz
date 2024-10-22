from django.contrib import admin

from apps.admin.apps_admin import get_app_list
from .base_admin import UserModelAdmin, CategoryModelAdmin, ProductModelAdmin, OrderModelAdmin, ReginModelAdmin, \
    DistrictModelAdmin, SiteSettingsModelAdmin, FavouriteModelAdmin, TransactionModelAdmin, CompetitionModelAdmin, \
    OperatorStackedInline

# sorted apps
admin.AdminSite.get_app_list = get_app_list
