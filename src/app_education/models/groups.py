from django.db import models
from django.utils.translation import gettext_lazy as _

from app_education.models import FacultyModel, FieldOfStudyModel


class FacultyGroups(models.Model):
    class Meta:
        verbose_name = _("Faculty Group")
        verbose_name_plural = _("Faculty Groups")

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    faculty = models.ForeignKey(FacultyModel, on_delete=models.CASCADE, verbose_name=_("Faculty"))
    fields = models.ManyToManyField(FieldOfStudyModel, verbose_name=_("Fields"))