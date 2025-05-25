from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Settings(models.Model):
    class Meta:
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")

    start_register_date = models.DateField(
        verbose_name=_("Start register date"),
    )
    end_register_date = models.DateField(verbose_name=_("End register date"))
