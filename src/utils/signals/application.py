from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import IntegrityError

from app_application.models import ApplicationModel

from utils.functions import generate_number

from datetime import datetime
from jalali_date import date2jalali


@receiver(post_save, sender=ApplicationModel)
def create_application_handler(sender, instance, **kwargs):
    if kwargs["created"]:
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
