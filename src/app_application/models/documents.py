from django.db import models
from django.utils.translation import gettext_lazy as _

from Abrat.settings import DEBUG

from app_application.models import ApplicationModel
from app_user.models import UserModel

from utils import GeneralDateModel
from utils.validators import validate_image_file

import os


class DocumentManager(models.Manager):
    pass


def document_image_directory_path(instance, filename):
    return "application_documents/user_{0}/{1}".format(instance.user.email, filename)


class Document(GeneralDateModel):
    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
        ordering = ["-id"]

    application = models.OneToOneField(
        ApplicationModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="application_document",
        verbose_name=_("Application"),
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_documents",
        verbose_name=_("User"),
    )
    curriculum_vitae = models.FileField(
        upload_to=document_image_directory_path,
        validators=[
            validate_image_file,
        ],
        null=True,
        blank=True,
        verbose_name=_("Curriculum Vitae"),
    )
    personal_photo = models.FileField(
        upload_to=document_image_directory_path,
        validators=[
            validate_image_file,
        ],
        null=True,
        blank=True,
        verbose_name=_("Personal photo"),
    )
    valid_passport = models.FileField(
        upload_to=document_image_directory_path,
        validators=[
            validate_image_file,
        ],
        null=True,
        blank=True,
        verbose_name=_("Valid"),
    )
    high_school_certificate = models.FileField(
        upload_to=document_image_directory_path,
        validators=[
            validate_image_file,
        ],
        null=True,
        blank=True,
        verbose_name=_("High School Certificate"),
    )
    trans_script_high_school_certificate = models.FileField(
        upload_to=document_image_directory_path,
        validators=[
            validate_image_file,
        ],
        null=True,
        blank=True,
        verbose_name=_("Trans Script High School Certificate"),
    )
    bachelor_degree = models.FileField(
        upload_to=document_image_directory_path,
        validators=[
            validate_image_file,
        ],
        null=True,
        blank=True,
        verbose_name=_("Bachelor Degree"),
    )
    trans_script_bachelor_degree = models.FileField(
        upload_to=document_image_directory_path,
        validators=[
            validate_image_file,
        ],
        null=True,
        blank=True,
        verbose_name=_("Trans Script Bachelor Degree"),
    )
    master_degree = models.FileField(
        upload_to=document_image_directory_path,
        validators=[
            validate_image_file,
        ],
        null=True,
        blank=True,
        verbose_name=_("Master Degree"),
    )
    trans_script_master_degree = models.FileField(
        upload_to=document_image_directory_path,
        validators=[
            validate_image_file,
        ],
        null=True,
        blank=True,
        verbose_name=_("Trans Script Master Degree"),
    )
    supporting_letter = models.FileField(
        upload_to=document_image_directory_path,
        validators=[
            validate_image_file,
        ],
        null=True,
        blank=True,
        verbose_name=_("Supporting Letter"),
    )
    second_supporting_letter = models.FileField(
        upload_to=document_image_directory_path,
        validators=[
            validate_image_file,
        ],
        null=True,
        blank=True,
        verbose_name=_("Supporting Letter"),
    )
    third_supporting_letter = models.FileField(
        upload_to=document_image_directory_path,
        validators=[
            validate_image_file,
        ],
        null=True,
        blank=True,
        verbose_name=_("Supporting Letter"),
    )

    objects = DocumentManager()

    def get_field_image_url(self, field_name, request):
        if getattr(self, field_name) is None or getattr(self, field_name) == "":
            return None
        else:
            host = request.get_host()
            protocol = request.build_absolute_uri().split(host)[0]
            protocol = (
                protocol
                if DEBUG
                else protocol.replace("http", "https")
                if protocol.split(":")[0] == "http"
                else protocol
            )
            website_url = protocol + host
            return website_url + getattr(self, field_name).url

    def get_field_file_name(self, field_name):
        return os.path.basename(getattr(self, field_name).name)
