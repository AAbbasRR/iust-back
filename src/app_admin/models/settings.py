from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Settings(models.Model):
    class Meta:
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")

    fa_signup_terms = models.TextField(
        verbose_name=_("Farsi Signup terms"),
    )
    en_signup_terms = models.TextField(
        verbose_name=_("English Signup terms"),
    )
    ar_signup_terms = models.TextField(
        verbose_name=_("Arabic Signup terms"),
    )
    fa_before_sign_text = models.TextField(
        verbose_name=_("Farsi Before sign text"),
    )
    en_before_sign_text = models.TextField(
        verbose_name=_("English Before sign text"),
    )
    ar_before_sign_text = models.TextField(
        verbose_name=_("Arabic Before sign text"),
    )
    fa_before_new_application_text = models.TextField(
        verbose_name=_("Farsi Before new application text"),
    )
    en_before_new_application_text = models.TextField(
        verbose_name=_("English Before new application text"),
    )
    ar_before_new_application_text = models.TextField(
        verbose_name=_("Arabic Before new application text"),
    )
    admin_application_text = models.TextField(verbose_name=_("Admin application text"))
    start_application_date = models.DateField(
        verbose_name=_("Start application date"),
    )
    end_application_date = models.DateField(verbose_name=_("End application date"))
