from django.db import models
from django.utils.translation import gettext_lazy as _

from utils import GeneralDateModel, GeneralMultiLanguageModel


class Faculty(GeneralDateModel, GeneralMultiLanguageModel):
    class Meta:
        verbose_name = _("Faculty")
        verbose_name_plural = _("Faculties")

    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))


class FieldOfStudy(GeneralDateModel, GeneralMultiLanguageModel):
    class Meta:
        verbose_name = _("Field of Study")
        verbose_name_plural = _("Fields of Study")

    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, verbose_name=_("Faculty")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    requires_an_interview = models.BooleanField(
        default=False, verbose_name=_("Require Interview")
    )
    max_members = models.PositiveSmallIntegerField(verbose_name=_("Max Members"))
