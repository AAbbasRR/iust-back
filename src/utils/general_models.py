from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from Abrat.settings import DATE_INPUT_FORMATS, TIME_INPUT_FORMATS

from jalali_date import datetime2jalali
from datetime import timedelta


class GeneralDateModel(models.Model):
    create_at = models.DateTimeField(verbose_name=_("Created Time"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated Time"), auto_now=True)

    def created_at(self):
        return self.create_at.strftime(f"{DATE_INPUT_FORMATS} - {TIME_INPUT_FORMATS}")

    def jalali_created_at(self, tehran_time=True):
        if tehran_time is True:
            return datetime2jalali(
                self.create_at + timedelta(hours=3, minutes=30)
            ).strftime(f"{DATE_INPUT_FORMATS} - {TIME_INPUT_FORMATS}")
        else:
            return datetime2jalali(self.create_at).strftime(
                f"{DATE_INPUT_FORMATS} - {TIME_INPUT_FORMATS}"
            )

    class Meta:
        abstract = True


class GeneralAddressModel(models.Model):
    country = models.CharField(
        max_length=35,
        null=True,
        blank=True,
        verbose_name=_("Country"),
    )
    state = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name=_("City"),
    )
    city = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name=_("City"),
    )

    class Meta:
        abstract = True


class GeneralEducationModel(GeneralAddressModel):
    date_of_graduation = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Date Of Graduation"),
    )
    gpa = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
        verbose_name=_("GPA"),
    )
    field_of_study = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("Field Of Study"),
    )

    def save(self, *args, **kwargs):
        self.gpa = round(self.gpa, 2)
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class GeneralMultiLanguageModel(GeneralAddressModel):
    fa_name = models.CharField(max_length=64, verbose_name=_("Faculty Name"))
    en_name = models.CharField(max_length=64, verbose_name=_("English Name"))
    ar_name = models.CharField(max_length=64, verbose_name=_("Arabic Name"))

    class Meta:
        abstract = True
