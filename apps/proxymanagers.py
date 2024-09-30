# from django.db.models import Manager
#
# from apps.models import User
#
#
# class NewOrderManager(Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(status=self.model.Status.NEW)
#
#
# class ReadyOrderManager(Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(status=self.model.Status.READY)
#
#
# class DeliverOrderManager(Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(status=self.model.Status.DELIVER)
#
#
# class DeliveredOrderManager(Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(status=self.Order.status.DELIVERED)
#
#
# class CantPhoneOrderManager(Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(status=self.model.Status.CANT_PHONE)
#
#
# class CanceledOrderManager(Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(status=self.model.Status.CANCELED)
#
#
# class ArchivedOrderManager(Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(status=self.model.Status.ARCHIVED)
#
#
# class OperatorUserManager(Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(user__type=User.Type.OPERATOR)
#
#
# class ManagerUserManager(Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(user__type=User.Type.MANAGER)
#
#
# class AdminUserManager(Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(user__type=User.Type.ADMIN)
#
#
# class DriverUserManager(Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(user__type=User.Type.DRIVER)
#
#
# class UserManager(Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(user__type=User.Type.USER)
