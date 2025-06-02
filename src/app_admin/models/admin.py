from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from app_education.models import FacultyModel, FacultyGroupsModel

UserModel = get_user_model()


class AdminManager(models.Manager):
    pass


class Admin(models.Model):
    class AdminRoleOptions(models.TextChoices):
        faculty_director = "faculty_director", _("Faculty Director")
        department_head = "department_head", _("Department Head")
        department_member = "department_member", _("Department Member")

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_admin",
        verbose_name=_("User"),
    )
    role = models.CharField(
        max_length=17,
        choices=AdminRoleOptions.choices,
        default=AdminRoleOptions.department_member,
        verbose_name=_("Role"),
    )
    faculties = models.ForeignKey(
        FacultyModel,
        on_delete=models.CASCADE,
        verbose_name=_("Schools")
    )
    fields = models.ForeignKey(
        FacultyGroupsModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Fields"),
    )

    objects = AdminManager()
