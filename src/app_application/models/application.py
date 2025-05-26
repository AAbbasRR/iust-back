from django.db import models
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _

from Abrat.settings import DEBUG

from app_user.models import UserModel
from app_education.models import FacultyModel, FieldOfStudyModel

from utils import GeneralDateModel

import fitz
from functools import reduce


class ApplicationManager(models.Manager):
    def find_with_tracking_id(self, tracking_id):
        return self.filter(tracking_id=tracking_id).first()


def application_file_directory_path(instance, filename):
    return "application_file/{0}/{1}".format(instance.tracking_id, filename)


class Application(GeneralDateModel):
    class Meta:
        verbose_name = _("Application")
        verbose_name_plural = _("Applications")
        ordering = ["-id"]

    class ApplicationStatusOptions(models.TextChoices):
        Not_Completed = "Not_Completed", _("Not Completed")
        Current = "Current", _("Current")
        Accepted = "Accepted", _("Accepted")
        Rejected = "Rejected", _("Rejected")
        NeedToEdit = "Need_To_Edit", _("Need To Edit")

    class ApplicationDegreeOptions(models.TextChoices):
        Bachelor = "Bachelor", _("Bachelor")
        Master = "Master", _("Master")
        PHD = "P.H.D", _("PhD")

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_application",
        verbose_name=_("User"),
    )
    agent = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="agent_applications",
        null=True,
        blank=True,
        verbose_name=_("Agent Email"),
    )
    tracking_id = models.CharField(
        max_length=12,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Tracking ID"),
    )
    full_name = models.CharField(
        max_length=50, null=True, blank=True, verbose_name=_("Full Name")
    )
    comments = models.TextField(null=True, blank=True, verbose_name=_("Comments"))
    applied_program = models.BooleanField(
        null=True, blank=True, verbose_name=_("Applied Program")
    )
    financial_self_support = models.BooleanField(
        default=False, verbose_name=_("Financial Self Support")
    )
    status = models.CharField(
        max_length=13,
        choices=ApplicationStatusOptions.choices,
        default=ApplicationStatusOptions.Not_Completed,
        verbose_name=_("Status"),
    )
    degree = models.CharField(
        max_length=8,
        choices=ApplicationDegreeOptions.choices,
        default=ApplicationDegreeOptions.Bachelor,
        verbose_name=_("Degree"),
    )
    faculty = models.ForeignKey(
        FacultyModel,
        on_delete=models.PROTECT,
        related_name="faculty_applications",
        verbose_name=_("Faculty"),
    )
    field_of_study = models.ForeignKey(
        FieldOfStudyModel,
        on_delete=models.PROTECT,
        related_name="field_of_study_applications",
        verbose_name=_("Field Of Study"),
    )
    step = models.IntegerField(default=3, verbose_name=_("step"))
    application_file = models.FileField(
        upload_to=application_file_directory_path,
        null=True,
        blank=True,
        verbose_name=_("Application File"),
    )
    application_letter = models.FileField(
        upload_to=application_file_directory_path,
        null=True,
        blank=True,
        verbose_name=_("Application Letter"),
    )

    objects = ApplicationManager()

    def __str__(self):
        return self.tracking_id

    def application_file_url(self, request):
        try:
            if self.application_file is None or self.application_file == "":
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
                return website_url + self.application_file.url
        except ValueError:
            return None

    def application_letter_url(self, request):
        try:
            if self.application_letter is None or self.application_letter == "":
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
                return website_url + self.application_letter.url
        except ValueError:
            return None

    def update_application_file(self):
        try:
            pdf_document = fitz.open("final.pdf")

            page_0_points = {
                "user__user_profile__first_name": fitz.Point(175, 105),
                "user__user_profile__last_name": fitz.Point(445, 105),
                "user__user_profile__nationality": fitz.Point(175, 140),
                "user__user_profile__birth_date": fitz.Point(445, 122),
                "user__user_profile__mother_language": fitz.Point(445, 140),
                "user__user_profile__other_languages": fitz.Point(175, 157),
                "user__email": fitz.Point(445, 175),
                "user__user_address__postal_code": fitz.Point(175, 192),
                "user__user_profile__phone_number": fitz.Point(445, 192),
                "user__user_address__country": fitz.Point(175, 209),
                "user__user_address__country_code": fitz.Point(445, 209),
                "user__user_address__city": fitz.Point(175, 226),
                "user__user_address__city_code": fitz.Point(445, 226),
                "user__user_address__address": fitz.Point(175, 245),
                "faculty__en_name": fitz.Point(363, 309),
                "field_of_study__en_name": fitz.Point(465, 309),
                "user__user_high_school__field_of_study": fitz.Point(175, 360),
                "user__user_high_school__gpa": fitz.Point(445, 360),
                "user__user_high_school__country": fitz.Point(175, 377),
                "user__user_high_school__city": fitz.Point(445, 377),
                "user__user_bachelor_degree__field_of_study": fitz.Point(175, 415),
                "user__user_bachelor_degree__date_of_graduation": fitz.Point(445, 415),
                "user__user_bachelor_degree__university": fitz.Point(175, 430),
                "user__user_bachelor_degree__gpa": fitz.Point(445, 430),
                "user__user_bachelor_degree__country": fitz.Point(175, 448),
                "user__user_bachelor_degree__city": fitz.Point(445, 448),
                "user__user_master_degree__field_of_study": fitz.Point(175, 484),
                "user__user_master_degree__date_of_graduation": fitz.Point(445, 484),
                "user__user_master_degree__university": fitz.Point(175, 502),
                "user__user_master_degree__gpa": fitz.Point(445, 502),
                "user__user_master_degree__country": fitz.Point(175, 520),
                "user__user_master_degree__city": fitz.Point(445, 520),
                "user__user_latest_occupation__occupation": fitz.Point(175, 555),
                "user__user_latest_occupation__organization": fitz.Point(445, 555),
                "user__user_latest_occupation__country": fitz.Point(175, 572),
                "user__user_latest_occupation__from_date": fitz.Point(445, 572),
                "user__user_latest_occupation__to_date": fitz.Point(490, 572),
            }
            page_1_points = {
                "full_name": fitz.Point(175, 110),
                "create_at__date.": fitz.Point(445, 110),
                "comments": fitz.Point(175, 128),
            }
            page_0_boolean_points = {
                "user__user_profile__gender": {
                    "Male": fitz.Point(175, 122),
                    "Female": fitz.Point(210, 122),
                },
                "user__user_profile__english_status": {
                    "Weak": fitz.Point(444, 157),
                    "Good": fitz.Point(482, 157),
                    "Excellent": fitz.Point(522, 157),
                },
                "user__user_profile__persian_status": {
                    "Weak": fitz.Point(177, 174),
                    "Good": fitz.Point(214, 174),
                    "Excellent": fitz.Point(255, 174),
                },
                "degree": {
                    "Bachelor": fitz.Point(175, 308),
                    "Master": fitz.Point(222, 308),
                    "P.H.D": fitz.Point(262, 308),
                },
                "application_document__curriculum_vitae": {
                    "True": fitz.Point(310, 608),
                    "False": fitz.Point(355, 608),
                },
                "application_document__personal_photo": {
                    "True": fitz.Point(310, 625),
                    "False": fitz.Point(355, 625),
                },
                "application_document__valid_passport": {
                    "True": fitz.Point(310, 642),
                    "False": fitz.Point(355, 643),
                },
                "application_document__master_degree": {
                    "True": fitz.Point(310, 659),
                    "False": fitz.Point(355, 660),
                },
                "application_document__bachelor_degree": {
                    "True": fitz.Point(310, 677),
                    "False": fitz.Point(355, 678),
                },
                "application_document__high_school_certificate": {
                    "True": fitz.Point(310, 695),
                    "False": fitz.Point(355, 695),
                },
                "application_document__trans_script_master_degree": {
                    "True": fitz.Point(310, 712),
                    "False": fitz.Point(355, 712),
                },
                "application_document__trans_script_bachelor_degree": {
                    "True": fitz.Point(310, 730),
                    "False": fitz.Point(355, 729),
                },
                "application_document__trans_script_high_school_certificate": {
                    "True": fitz.Point(310, 747),
                    "False": fitz.Point(355, 747),
                },
            }
            page_1_boolean_points = {
                "financial_self_support": {
                    "True": fitz.Point(311, 59),
                    "False": fitz.Point(356, 59),
                },
                "application_document__supporting_letter": {
                    "True": fitz.Point(311, 76),
                    "False": fitz.Point(356, 76),
                },
            }

            for index in range(2):
                page = pdf_document.load_page(index)
                text_points = locals()[f"page_{index}_points"]
                for text_points_key in text_points:
                    callable_value = text_points_key.split(".")
                    nested_attrs = callable_value[0].split("__")
                    nested_obj = reduce(getattr, nested_attrs, self)
                    value = nested_obj if nested_obj is not None else ""
                    if len(callable_value) > 1:
                        value = value()
                    page.insert_text(
                        text_points[text_points_key],
                        str(value),
                        fontsize=8,
                        color=(0, 0, 0),
                    )
                boolean_points = locals()[f"page_{index}_boolean_points"]
                for boolean_points_key in boolean_points:
                    callable_value = boolean_points_key.split(".")
                    nested_attrs = callable_value[0].split("__")
                    try:
                        nested_obj = reduce(getattr, nested_attrs, self)
                        if nested_attrs[0] == "application_document":
                            value = True if nested_obj != "" else False
                        else:
                            value = nested_obj
                    except:
                        value = False
                    if len(callable_value) > 1:
                        value = value()
                    page.insert_text(
                        boolean_points[boolean_points_key][str(value)],
                        "X",
                        fontsize=10,
                        color=(0, 0, 0),
                    )

            document = self.application_document

            # List of file fields to check
            file_fields = [
                "curriculum_vitae",
                "personal_photo",
                "valid_passport",
                "high_school_certificate",
                "trans_script_high_school_certificate",
                "bachelor_degree",
                "trans_script_bachelor_degree",
                "master_degree",
                "trans_script_master_degree",
                "supporting_letter",
                "second_supporting_letter",
                "third_supporting_letter",
            ]

            # Function to convert an image file to a PDF
            def image_to_pdf(image_path, field_name):
                img_doc = fitz.open()  # Create a new empty PDF
                page_width, page_height = 595, 842  # A4 size
                img_doc.new_page(width=page_width, height=page_height)

                img_page = img_doc.load_page(0)

                # Add the image to the page
                img_rect = fitz.Rect(
                    50, 50, page_width - 50, page_height - 150
                )  # Leave some margin
                img_page.insert_image(img_rect, filename=image_path)

                # Add the file name below the image
                text_position = fitz.Point(
                    img_rect.x0 + 10, img_rect.y1 + 10
                )  # Below the image
                img_page.insert_text(
                    text_position, field_name, fontsize=12, color=(0, 0, 0)
                )  # Black text
                return img_doc

            # Append non-null files to the PDF
            for field in file_fields:
                file = getattr(document, field)
                if file:  # If the file field is not null
                    file_path = file.path
                    file_extension = file_path.split(".")[-1].upper()
                    if file_extension in ["JPEG", "PNG", "JPG"]:
                        additional_pdf = image_to_pdf(file_path, field)
                    elif file_extension == "PDF":
                        additional_pdf = fitz.open(file_path)
                    else:
                        continue

                    pdf_document.insert_pdf(additional_pdf)
                    additional_pdf.close()

            pdf_bytes = pdf_document.write()

            self.application_file.save(
                "application_file.pdf", ContentFile(pdf_bytes), save=True
            )

            pdf_document.close()
        except Exception:
            pass
