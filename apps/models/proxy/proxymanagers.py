from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from django.db.models import Manager

user = get_user_model()


# FOR ORDER MODEL

class NewOrderManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=self.model.StatusType.NEW)


class ReadyOrderManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=self.model.StatusType.READY)


class DeliveringOrderManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=self.model.StatusType.DELIVERING)


class DeliveredOrderManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=self.model.StatusType.DELIVERED)


class CantPhoneOrderManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=self.model.StatusType.CANT_PHONE)


class BrokenOrderManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=self.model.StatusType.BROKEN)


class CanceledOrderManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=self.model.StatusType.CANCELED)


class ArchivedOrderManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=self.model.StatusType.ARCHIVED)


# for USER Model

class OperatorUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=user.Type.OPERATOR)


class ManagerUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=user.Type.MANAGER)


class AdminUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=user.Type.ADMIN)


class CurrierUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=user.Type.CURRIER)


class UserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=user.Type.USER)
