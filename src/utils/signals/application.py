from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import IntegrityError

from app_application.models import ApplicationModel, DocumentModel
from app_user.models import UserModel

from utils.functions import generate_number
from utils.classes import ManageMailService

from datetime import datetime
from jalali_date import date2jalali


@receiver(post_save, sender=ApplicationModel)
def create_application_handler(sender, instance, **kwargs):
    if kwargs["created"]:
        DocumentModel.objects.create(application=instance, user=instance.user)
        while True:
            try:
                date_now = datetime.now()
                jalali_year_now = date2jalali(date_now).year
                instance.tracking_id = (
                    f"{jalali_year_now}/{generate_number(instance.id)}"
                )
                instance.save()
                break
            except IntegrityError:
                pass
        superusers = UserModel.objects.filter(is_superuser=True)
        for user in superusers:
            superuser_mail = ManageMailService(user.email)
            user = instance.user
            superuser_mail.send_email_to_user(
                subject="اپلیکیشن جدید",
                content={
                    "title": "message",
                    "data": {
                        "title": f"یک اپلیکیشن جدید ثبت شده است.",
                        "description": f"یک اپلیکیشن جدید از کاربر {user.user_profile.get_full_name()}  با ایمیل {user.email} با کد رهگیری {instance.tracking_id} ایجاد شده است. ",
                    },
                },
            )
