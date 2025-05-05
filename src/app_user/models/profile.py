from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from Abrat.settings import DEBUG
from app_user.models import UserModel

from utils.general_models import GeneralDateModel


class ProfileManager(models.Manager):
    pass


def profile_image_directory_path(instance, filename):
    return "profile_images/user_{0}/{1}".format(instance.user.email, filename)


class Profile(GeneralDateModel):
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ["-id"]

    class ProfileGenderOptions(models.TextChoices):
        Male = "Male", _("Male")
        FeMale = "FeMale", _("FeMale")
        Other = "Other", _("Other")

    class ProfileLanguageOptions(models.TextChoices):
        Weak = "Weak", _("Weak")
        Good = "Good", _("Good")
        Excellent = "Excellent", _("Excellent")

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_profile",
        verbose_name=_("User"),
    )
    profile = models.ImageField(
        upload_to=profile_image_directory_path,
        null=True,
        blank=True,
        verbose_name=_("Profile"),
    )
    phone_number = models.CharField(
        max_length=50, null=True, verbose_name=_("Phone Number")
    )
    iran_phone_number = models.CharField(
        max_length=50, null=True, blank=True, verbose_name=_("Iran Phone Number")
    )
    first_name = models.CharField(
        max_length=100, null=True, verbose_name=_("First Name")
    )
    last_name = models.CharField(max_length=100, null=True, verbose_name=_("Last Name"))
    birth_date = models.DateField(
        null=True,
        verbose_name=_("Birth Date"),
    )
    age = models.PositiveIntegerField(default=1, verbose_name=_("Age"))
    gender = models.CharField(
        max_length=6,
        choices=ProfileGenderOptions.choices,
        default=ProfileGenderOptions.Male,
        verbose_name=_("Gender"),
    )
    nationality = models.CharField(
        max_length=50, null=True, verbose_name=_("Nationality")
    )
    mother_language = models.CharField(
        max_length=50, null=True, verbose_name=_("Mother Language")
    )
    other_languages = models.CharField(
        max_length=150,
        null=True,
        verbose_name=_("Other Languages"),
    )
    english_status = models.CharField(
        max_length=9,
        choices=ProfileLanguageOptions.choices,
        default=ProfileLanguageOptions.Good,
        verbose_name=_("English Status"),
    )
    persian_status = models.CharField(
        max_length=9,
        choices=ProfileLanguageOptions.choices,
        default=ProfileLanguageOptions.Good,
        verbose_name=_("Persian Status"),
    )
    passport_number = models.CharField(
        max_length=10, null=True, blank=True, verbose_name=_("Passport Number")
    )

    objects = ProfileManager()

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        self.age = self.get_age()
        super().save(*args, **kwargs)

    def profile_url(self, request):
        try:
            if self.profile is None or self.profile == "":
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
                return website_url + self.profile.url
        except ValueError:
            return None

    def get_full_name(self):
        return f'{self.first_name if self.first_name is not None else ""} {self.last_name if self.last_name is not None else ""}'

    def get_age(self):
        today = timezone.now().date()
        try:
            age = (
                today.year
                - self.birth_date.year
                - (
                    (today.month, today.day)
                    < (self.birth_date.month, self.birth_date.day)
                )
            )
        except AttributeError:
            age = 1
        return age
