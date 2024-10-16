from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

USER = get_user_model()


# @receiver(post_save, sender=USER)
# def send_email_create_account(sender, instance, created, **kwargs):
#     if created:
#         send_mail(
#             subject="Welcome!",
#             message="Hello, My Friend! Your account has been created.",
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[instance.email],
#         )


@receiver(post_save, sender=USER)
def transaction_to_user(sender, instance, *args, **kwargs):
    pass
