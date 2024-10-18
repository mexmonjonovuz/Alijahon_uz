from django.utils.translation import gettext_lazy as _

from apps.models import Order, User
from apps.models.proxy.proxymanagers import AdminUserManager, ManagerUserManager, CurrierUserManager, UserManager, \
    OperatorUserManager, ArchivedOrderManager, CanceledOrderManager, CantPhoneOrderManager, DeliveredOrderManager, \
    DeliveringOrderManager, ReadyOrderManager, NewOrderManager


class OrderNewProxyModel(Order):
    objects = NewOrderManager()

    class Meta:
        proxy = True
        verbose_name = _('New Order')
        verbose_name_plural = _('New Orders')


class OrderReadyProxyModel(Order):
    objects = ReadyOrderManager()

    class Meta:
        proxy = True
        verbose_name = _('Order ready')
        verbose_name_plural = _('Orders ready')


class OrderDeliverProxyModel(Order):
    objects = DeliveringOrderManager()

    class Meta:
        proxy = True
        verbose_name = _('Ready to ship')
        verbose_name_plural = _('Orders Ready to ship')


class OrderDeliveredProxyModel(Order):
    objects = DeliveredOrderManager()

    class Meta:
        proxy = True
        verbose_name = _('Delivered')
        verbose_name_plural = _('Orders Delivered')


class OrderCantPhoneProxyModel(Order):
    objects = CantPhoneOrderManager()

    class Meta:
        proxy = True
        verbose_name = _('Cant to Phone')
        verbose_name_plural = _('Cant to Phone')


class OrderCanceledProxyModel(Order):
    objects = CanceledOrderManager()

    class Meta:
        proxy = True
        verbose_name = _('Order Canceled')
        verbose_name_plural = _('Orders Canceled')


class OrderArchivedProxyModel(Order):
    objects = ArchivedOrderManager()

    class Meta:
        proxy = True
        verbose_name = _('Archived Order')
        verbose_name_plural = _('Archived Order')


class UserOperatorProxyModel(User):
    objects = OperatorUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Operator')
        verbose_name_plural = _('Operators')


class UserManagerProxyModel(User):
    objects = ManagerUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Manager')
        verbose_name_plural = _('Managers')


class UserAdminProxyModel(User):
    objects = AdminUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Admin')
        verbose_name_plural = _('Admins')


class UserCurrierProxyModel(User):
    objects = CurrierUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Currier')
        verbose_name_plural = _("Currier's")


class UserProxyModel(User):
    objects = UserManager()

    class Meta:
        proxy = True
        verbose_name = _('User')
        verbose_name_plural = _('Users')
