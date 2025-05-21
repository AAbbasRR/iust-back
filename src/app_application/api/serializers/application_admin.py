from django.db.models import Q, Case, When, Value, CharField
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, exceptions

from import_export import resources, fields

from app_application.models import (
    ApplicationModel,
    ReferralModel,
    DocumentModel,
    TimeLineModel,
)
from app_user.models import UserModel
from app_admin.models import AdminModel
from app_notification.models import NotificationModel

from utils.base_errors import BaseErrors
from utils.classes import ManageMailService

from docx import Document
from io import BytesIO
import tempfile
import subprocess
import os


class AdminApplicationListSerializer(serializers.ModelSerializer):
    degree = serializers.CharField(source="get_degree_display", read_only=True)
    faculty = serializers.SerializerMethodField(read_only=True)
    field_of_study = serializers.SerializerMethodField(read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)
    status_value = serializers.CharField(source="status", read_only=True)

    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = ApplicationModel
        fields = (
            "id",
            "tracking_id",
            "degree",
            "faculty",
            "field_of_study",
            "status",
            "status_value",
            "jalali_created_at",
            "user",
        )

    def __init__(self, *args, **kwargs):
        super(AdminApplicationListSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get("request")
        if self.request:
            self.admin_user = self.request.user

    def get_faculty(self, obj):
        return obj.faculty.fa_name

    def get_field_of_study(self, obj):
        return obj.field_of_study.fa_name

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "agent": obj.agent.email
            if obj.agent is not None and self.admin_user.is_superuser is True
            else None,
            "full_name": obj.user.user_profile.get_full_name(),
            "gender": obj.user.user_profile.get_gender_display(),
            "country": obj.user.user_address.country,
            "age": obj.user.user_profile.age,
            "applications_count": obj.user.user_application.count(),
        }


class AdminApplicationExportResource(resources.ModelResource):
    tracking_id = fields.Field(column_name=_("tracking_id"))
    degree = fields.Field(column_name=_("degree"))
    faculty = fields.Field(column_name=_("faculty"))
    field_of_study = fields.Field(column_name=_("field_of_study"))
    status = fields.Field(column_name=_("status"))
    jalali_created_at = fields.Field(column_name=_("jalali_created_at"))
    created_at = fields.Field(column_name=_("created_at"))
    user_id = fields.Field(column_name=_("user_id"))
    user_agent = fields.Field(column_name=_("user_agent"))
    user_full_name = fields.Field(column_name=_("user_full_name"))
    user_gender = fields.Field(column_name=_("user_gender"))
    user_country = fields.Field(column_name=_("user_country"))
    user_age = fields.Field(column_name=_("user_age"))
    user_applications_count = fields.Field(column_name=_("user_applications_count"))
    last_comment = fields.Field(column_name=_("last_comment"))
    last_commenter = fields.Field(column_name=_("last_commenter"))

    class Meta:
        model = ApplicationModel
        fields = (
            "tracking_id",
            "degree",
            "faculty",
            "field_of_study",
            "status",
            "jalali_created_at",
            "created_at",
            "user_id",
            "user_agent",
            "user_full_name",
            "user_gender",
            "user_country",
            "user_age",
            "user_applications_count",
            "last_comment",
            "last_commenter",
        )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def dehydrate_degree(self, obj):
        return obj.get_degree_display()

    def dehydrate_faculty(self, obj):
        return obj.faculty.fa_name

    def dehydrate_tracking_id(self, obj):
        return obj.tracking_id

    def dehydrate_field_of_study(self, obj):
        return obj.field_of_study.fa_name

    def dehydrate_status(self, obj):
        return obj.get_status_display()

    def dehydrate_jalali_created_at(self, obj):
        return obj.jalali_created_at()

    def dehydrate_created_at(self, obj):
        return obj.created_at()

    def dehydrate_user_id(self, obj):
        return obj.user.id

    def dehydrate_user_agent(self, obj):
        return (
            obj.agent.email
            if obj.agent is not None and self.user.is_superuser is True
            else None
        )

    def dehydrate_user_full_name(self, obj):
        return obj.user.user_profile.get_full_name()

    def dehydrate_user_gender(self, obj):
        return obj.user.user_profile.get_gender_display()

    def dehydrate_user_country(self, obj):
        return obj.user.user_address.country

    def dehydrate_user_age(self, obj):
        return obj.user.user_profile.age

    def dehydrate_user_applications_count(self, obj):
        return obj.user.user_application.count()

    def dehydrate_last_comment(self, obj):
        message = (
            obj.application_timeline.exclude(status="Referral")
            .order_by("-create_at")
            .first()
        )
        if message is None:
            return None
        return f"{message.get_status_display()}: {message.message}"

    def dehydrate_last_commenter(self, obj):
        message = (
            obj.application_timeline.exclude(status="Referral")
            .order_by("-create_at")
            .first()
        )
        if message is None:
            return None
        return f"{message.user.user_profile.get_full_name()} - {message.user.email}"


class AdminDocumentApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentModel
        fields = (
            "id",
            "jalali_created_at",
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
        )

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.request = self.context.get("request")
        if self.request:
            self.user = self.request.user

    def get_curriculum_vitae(self, obj):
        return obj.get_field_image_url("curriculum_vitae", self.request)

    def get_personal_photo(self, obj):
        return obj.get_field_image_url("personal_photo", self.request)

    def get_valid_passport(self, obj):
        return obj.get_field_image_url("valid_passport", self.request)

    def get_high_school_certificate(self, obj):
        return obj.get_field_image_url("high_school_certificate", self.request)

    def get_trans_script_high_school_certificate(self, obj):
        return obj.get_field_image_url(
            "trans_script_high_school_certificate", self.request
        )

    def get_bachelor_degree(self, obj):
        return obj.get_field_image_url("bachelor_degree", self.request)

    def get_trans_script_bachelor_degree(self, obj):
        return obj.get_field_image_url("trans_script_bachelor_degree", self.request)

    def get_master_degree(self, obj):
        return obj.get_field_image_url("master_degree", self.request)

    def get_trans_script_master_degree(self, obj):
        return obj.get_field_image_url("trans_script_master_degree", self.request)

    def get_supporting_letter(self, obj):
        return obj.get_field_image_url("supporting_letter", self.request)

    def get_second_supporting_letter(self, obj):
        return obj.get_field_image_url("second_supporting_letter", self.request)

    def get_third_supporting_letter(self, obj):
        return obj.get_field_image_url("third_supporting_letter", self.request)


class AdminApplicationTimeLineSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display", read_only=True)
    author = serializers.SerializerMethodField("get_author")

    class Meta:
        model = TimeLineModel
        fields = ("id", "status", "message", "jalali_created_at", "author")

    def get_author(self, obj):
        return {"full_name": obj.user.user_profile.get_full_name()}


class AdminRuleSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField("get_id")
    role_display = serializers.CharField(source="get_role_display", read_only=True)
    fields_display = serializers.CharField(source="get_fields_display", read_only=True)
    sub = serializers.SerializerMethodField("get_sub")
    username = serializers.SerializerMethodField("get_username")
    full_name = serializers.SerializerMethodField("get_full_name")

    class Meta:
        model = AdminModel
        fields = (
            "id",
            "role",
            "role_display",
            "sub",
            "username",
            "full_name",
            "fields_display",
        )

    def get_id(self, obj):
        return obj.user.id

    def get_sub(self, obj):
        return obj.user.sub

    def get_username(self, obj):
        return obj.user.username

    def get_full_name(self, obj):
        return obj.user.get_full_name()


class AdminDetailApplicationSerializer(serializers.ModelSerializer):
    degree_display = serializers.CharField(source="get_degree_display", read_only=True)
    faculty = serializers.SerializerMethodField(read_only=True)
    field_of_study = serializers.SerializerMethodField(read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)
    user = serializers.SerializerMethodField("get_user")
    application_document = serializers.SerializerMethodField("get_application_document")
    application_timeline = serializers.SerializerMethodField("get_application_timeline")
    staffs = serializers.SerializerMethodField("get_staffs")
    can_signature = serializers.SerializerMethodField("get_can_signature")
    can_referral = serializers.SerializerMethodField("get_can_referral")
    can_submit_application = serializers.SerializerMethodField(
        "get_can_submit_application"
    )
    status_value = serializers.CharField(source="status", read_only=True)
    application_file_url = serializers.SerializerMethodField("get_application_file_url")
    application_letter_url = serializers.SerializerMethodField(
        "get_application_letter_url"
    )

    class Meta:
        model = ApplicationModel
        fields = (
            "id",
            "tracking_id",
            "degree",
            "degree_display",
            "faculty",
            "field_of_study",
            "status",
            "status_value",
            "jalali_created_at",
            "application_document",
            "application_file_url",
            "application_letter_url",
            "application_timeline",
            "user",
            "staffs",
            "can_referral",
            "can_submit_application",
            "can_signature",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get("request")
        if self.request:
            self.user = self.request.user
            self.method = self.request.method
            if self.method in ["PUT", "PATCH"]:
                for field_name, field in self.fields.items():
                    field.required = False

    def get_faculty(self, obj):
        return obj.faculty.fa_name

    def get_field_of_study(self, obj):
        return obj.field_of_study.fa_name

    def get_application_letter_url(self, obj):
        return obj.application_letter_url(self.request)

    def get_application_file_url(self, obj):
        return obj.application_file_url(self.request)

    def get_user(self, obj):
        return {
            "full_name": obj.user.user_profile.get_full_name(),
            "gender": obj.user.user_profile.get_gender_display(),
            "country": obj.user.user_address.country,
            "city": obj.user.user_address.city,
            "age": obj.user.user_profile.age,
            "agent": obj.agent.email
            if obj.agent is not None and self.user.is_superuser is True
            else None,
            "applications_count": obj.user.user_application.count(),
        }

    def get_application_document(self, obj):
        try:
            return AdminDocumentApplicationSerializer(
                obj.application_document,
                many=False,
                read_only=True,
                context=self.context,
            ).data
        except:
            return None

    def get_application_timeline(self, obj):
        return AdminApplicationTimeLineSerializer(
            obj.application_timeline.all(),
            many=True,
            read_only=True,
            context=self.context,
        ).data

    def get_can_referral(self, obj):
        user_rule = self.user.user_admin.filter(
            Q(schools=obj.faculty)
            & Q(role=AdminModel.AdminRoleOptions.faculty_director)
            | (
                Q(fields=obj.field_of_study)
                & Q(role=AdminModel.AdminRoleOptions.department_head)
            )
        ).first()
        return self.user.is_superuser or user_rule is not None

    def get_can_submit_application(self, obj):
        user_rule = self.user.user_admin.filter(
            schools=obj.faculty, role=AdminModel.AdminRoleOptions.faculty_director
        ).first()
        return self.user.is_superuser or user_rule is not None

    def get_can_signature(self, obj):
        return self.user.is_superuser

    def get_staffs(self, obj):
        user_faculty_rule = self.user.user_admin.filter(
            role=AdminModel.AdminRoleOptions.faculty_director,
            schools=obj.faculty,
        ).first()
        superusers_data = []
        if self.user.is_superuser or user_faculty_rule is not None:
            superusers = UserModel.objects.filter(is_superuser=True).exclude(
                pk=self.user.id
            )
            for user in superusers:
                superusers_data.append(
                    {
                        "id": user.id,
                        "role": "superuser",
                        "role_display": _("Superuser"),
                        "sub": user.sub,
                        "username": user.username,
                        "full_name": user.get_full_name(),
                        "fields_display": _("Superuser"),
                    }
                )
        faculty_director = AdminModel.objects.filter(
            schools=obj.faculty, role=AdminModel.AdminRoleOptions.faculty_director
        ).exclude(user__pk=self.user.id)
        faculty_director_data = AdminRuleSerializer(faculty_director, many=True).data
        staffs = (
            AdminModel.objects.filter(
                schools=obj.faculty,
                role__in=[
                    AdminModel.AdminRoleOptions.department_head,
                    AdminModel.AdminRoleOptions.department_member,
                ],
            )
            .exclude(user__pk=self.user.id)
            .order_by("fields", "role")
        )
        staffs_data = AdminRuleSerializer(staffs, many=True).data
        return superusers_data + faculty_director_data + staffs_data


class AdminUpdateApplicationSerializer(serializers.ModelSerializer):
    message = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True,
        allow_null=True,
        write_only=True,
    )

    class Meta:
        model = ApplicationModel
        fields = ("status", "message")
        extra_kwargs = {"status": {"required": True}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get("request")
        if self.request:
            self.user = self.request.user
            self.method = self.request.method
            if self.method in ["PUT", "PATCH"]:
                for field_name, field in self.fields.items():
                    field.required = False

    def update(self, instance, validated_data):
        user_rule = self.user.user_admin.filter(
            schools=instance.faculty, role=AdminModel.AdminRoleOptions.faculty_director
        ).first()
        if self.user.is_superuser or user_rule is not None:
            instance.status = validated_data["status"]
            instance.save()
            time_line_status = TimeLineModel.TimeLineStatusOptions.NeedToEdit
            if (
                validated_data["status"]
                == ApplicationModel.ApplicationStatusOptions.Accepted
            ):
                time_line_status = TimeLineModel.TimeLineStatusOptions.Confirmation
            elif (
                validated_data["status"]
                == ApplicationModel.ApplicationStatusOptions.Rejected
            ):
                time_line_status = TimeLineModel.TimeLineStatusOptions.Rejection
            message = validated_data.pop(
                "message", "Final record of application status"
            )
            TimeLineModel.objects.create(
                user=self.user,
                application=instance,
                status=time_line_status,
                message=message,
            )
            ReferralModel.objects.filter(
                application=instance,
                is_enabled=True,
            ).update(is_enabled=False)
            notification_status = NotificationModel.NotificationStatusOptions.Warning
            notification_message = f"your application need to edit because: {message}"
            if instance.status == ApplicationModel.ApplicationStatusOptions.Accepted:
                notification_status = (
                    NotificationModel.NotificationStatusOptions.Success
                )
                notification_message = f"congratulations, your application approved"
            elif instance.status == ApplicationModel.ApplicationStatusOptions.Rejected:
                notification_status = NotificationModel.NotificationStatusOptions.Error
                notification_message = f"Unfortunately, your request has been rejected, due to: {notification_message}"
            NotificationModel.objects.create(
                user=instance.user,
                title=f"application {instance.tracking_id}",
                status=notification_status,
                message=notification_message,
            )
            return instance
        else:
            raise exceptions.ParseError(BaseErrors.user_cant_edit_application_status)


class AdminSubmitApplicationLetterSerializer(serializers.Serializer):
    application = serializers.IntegerField(required=True)
    count_semesters = serializers.IntegerField(required=True, min_value=1)
    fee = serializers.IntegerField(required=True, min_value=0)
    semesters_year = serializers.CharField(max_length=10, required=True)
    semesters_season = serializers.CharField(max_length=10, required=True)
    register_start_date = serializers.CharField(max_length=15, required=True)
    register_end_date = serializers.CharField(max_length=15, required=True)
    start_program_date = serializers.CharField(max_length=15, required=True)

    def validate_application(self, value):
        application_obj = ApplicationModel.objects.filter(pk=value).first()
        if application_obj is not None:
            return application_obj
        else:
            raise exceptions.NotFound(
                BaseErrors._change_error_variable(
                    "object_not_found", object=_("Application")
                )
            )

    def validate(self, attrs):
        replacements = {
            "<<created_at>>": str(attrs["application"].create_at.date()),
            "<<create_at>>": str(attrs["application"].create_at.date()),
            "<<tracking_id>>": str(attrs["application"].tracking_id),
            "<<gender>>": "Mr"
            if attrs["application"].user.user_profile.gender == "Male"
            else "Miss",
            "<<full_name>>": str(attrs["application"].full_name),
            "<<degree>>": str(attrs["application"].degree),
            "<<faculty>>": str(attrs["application"].faculty),
            "<<field_of_study>>": f"{str(attrs['application'].faculty).split('Department of ' if 'Department of ' in str(attrs['application'].faculty) else 'School of ')[1]} - {str(attrs['application'].field_of_study)}",
            "<<nationality>>": str(attrs["application"].user.user_profile.nationality),
            "<<passport_number>>": str(
                attrs["application"].user.user_profile.passport_number
            ),
            "<<avg_bachelor>>": str(attrs["application"].user.user_bachelor_degree.gpa),
            "<<avg_master>>": str(attrs["application"].user.user_master_degree.gpa),
            "<<count_semesters>>": str(attrs["count_semesters"]),
            "<<count_years>>": str(int(attrs["count_semesters"] / 2)),
            "<<fee>>": str(attrs["fee"]),
            "<<semesters_year>>": str(attrs["semesters_year"]),
            "<<semesters_season>>": str(attrs["semesters_season"]),
            "<<register_start_date>>": str(attrs["register_start_date"]),
            "<<register_end_date>>": str(attrs["register_end_date"]),
            "<<start_program_date>>": str(attrs["start_program_date"]),
        }

        doc = Document("letter.docx")
        for p in doc.paragraphs:
            for key, value in replacements.items():
                if key.strip() in p.text:
                    inline = p.runs
                    for i in range(len(inline)):
                        if key in inline[i].text:
                            text = inline[i].text.replace(key, value)
                            inline[i].text = text

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        for key, value in replacements.items():
                            if key in paragraph.text:
                                inline = paragraph.runs
                                for i in range(len(inline)):
                                    if key in inline[i].text:
                                        text = inline[i].text.replace(key, value)
                                        inline[i].text = text

        # Save DOCX to a temporary file
        doc_bytes_stream = BytesIO()
        doc.save(doc_bytes_stream)
        doc_bytes_stream.seek(0)

        with tempfile.NamedTemporaryFile(
            suffix=".docx", delete=False
        ) as temp_docx_file:
            temp_docx_file.write(doc_bytes_stream.getvalue())
            temp_docx_path = temp_docx_file.name

        # Save the DOCX file to the model
        attrs["application"].application_letter.save(
            "application_letter.docx",
            ContentFile(doc_bytes_stream.getvalue()),
            save=True,
        )

        # Convert DOCX to PDF using docx2pdf
        pdf_file_path = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name

        subprocess.run(
            ["unoconv", "-f", "pdf", "-o", pdf_file_path, temp_docx_path], check=True
        )

        # Read the PDF into memory
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
            pdf_stream = BytesIO(pdf_bytes)

            # Send email with PDF attachment
            subject = "Acceptance Letter"
            body = {
                "title": "acceptance_letter",
                "data": {
                    "title": "Acceptance Letter",
                    "description": "Congratulations, your application to study at IUST University has been approved. You can read more information in the attached file",
                },
            }

            user_email = ManageMailService(attrs["application"].user.email)
            user_email.send_email_to_user_with_attachments(
                subject,
                body,
                "application_letter.pdf",
                pdf_stream.read(),
                "application/pdf",
            )
            if attrs["application"].agent is not None:
                user_email = ManageMailService(attrs["application"].agent.email)
                user_email.send_email_to_user_with_attachments(
                    subject,
                    body,
                    "application_letter.pdf",
                    pdf_stream.read(),
                    "application/pdf",
                )
        # Clean up temporary files
        os.remove(temp_docx_path)
        if pdf_file_path and os.path.exists(pdf_file_path):
            os.remove(pdf_file_path)
        if pdf_stream:
            pdf_stream.close()
        doc_bytes_stream.close()

        attrs.pop("application")

        return attrs
