from django.utils.translation import gettext_lazy as _

from apps.models import Order, User


class OrderNewProxyModel(Order):
    class Meta:
        proxy = True
        verbose_name = _('Yangi buyurtma')
        verbose_name_plural = _('Yangi buyurtmalar')


class OrderReadyProxyModel(Order):
    class Meta:
        proxy = True
        verbose_name = _('Buyurtma tayyor')
        verbose_name_plural = _('Buyurtmalar tayyor')


class OrderDeliverProxyModel(Order):
    class Meta:
        proxy = True
        verbose_name = _('Yetkazib berishga tayyor')
        verbose_name_plural = _('Yetkazib berishga tayyor buyurtmalar')


class OrderDeliveredProxyModel(Order):
    class Meta:
        proxy = True
        verbose_name = _('Yetkazib berildi')
        verbose_name_plural = _('Yetkazib berilgan buyurtmalar')


class OrderCantPhoneProxyModel(Order):
    class Meta:
        proxy = True
        verbose_name = _('Telefon orqali bog‘lanib bo‘lmadi')
        verbose_name_plural = _('Telefon orqali bog‘lanib bo‘lmagan buyurtmalar')


class OrderCanceledProxyModel(Order):
    class Meta:
        proxy = True
        verbose_name = _('Bekor qilingan buyurtma')
        verbose_name_plural = _('Bekor qilingan buyurtmalar')


class OrderArchivedProxyModel(Order):
    class Meta:
        proxy = True
        verbose_name = _('Arxivlangan buyurtma')
        verbose_name_plural = _('Arxivlangan buyurtmalar')


class UserOperatorProxyModel(User):
    class Meta:
        proxy = True
        verbose_name = _('Operator')
        verbose_name_plural = _('Operatorlar uchun')


class UserManagerProxyModel(User):
    class Meta:
        proxy = True
        verbose_name = _('Manager')
        verbose_name_plural = _('Managerlar uchun')


class UserAdminProxyModel(User):
    class Meta:
        proxy = True
        verbose_name = _('Admin')
        verbose_name_plural = _('Adminlar uchun')


class UserDriverProxyModel(User):
    class Meta:
        proxy = True
        verbose_name = _('Yetqazuvchi')
        verbose_name_plural = _('Yetqazuvchilar uchun')


class UserProxyModel(User):
    class Meta:
        proxy = True
        verbose_name = _('Foydalanuvchi')
        verbose_name_plural = _('Foydalanuvchilar uchun')
