from django.contrib.admin import ModelAdmin

from apps.admin.apps_admin import site_register
from apps.models.proxy.proxy import OrderNewProxyModel, OrderReadyProxyModel, OrderDeliverProxyModel, \
    OrderDeliveredProxyModel, \
    OrderCantPhoneProxyModel, OrderBrokenProxyModel, OrderCanceledProxyModel, OrderArchivedProxyModel


@site_register(OrderNewProxyModel)
class OrderNewProxyModelAdmin(ModelAdmin):
    pass


@site_register(OrderReadyProxyModel)
class OrderReadyProxyModelAdmin(ModelAdmin):
    pass


@site_register(OrderDeliverProxyModel)
class OrderDeliverProxyModelAdmin(ModelAdmin):
    pass


@site_register(OrderDeliveredProxyModel)
class OrderDeliveredProxyModelAdmin(ModelAdmin):
    pass


@site_register(OrderCantPhoneProxyModel)
class OrderCantPhoneProxyModelAdmin(ModelAdmin):
    pass


@site_register(OrderBrokenProxyModel)
class OrderBrokenProxyModelAdmin(ModelAdmin):
    pass


@site_register(OrderCanceledProxyModel)
class OrderCanceledProxyModelAdmin(ModelAdmin):
    pass


@site_register(OrderArchivedProxyModel)
class OrderArchivedProxyModelAdmin(ModelAdmin):
    pass
