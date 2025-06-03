from django.contrib.auth import get_user_model

from rest_framework import serializers, exceptions

from app_application.models import ApplicationModel, TimeLineModel, ReferralModel
from app_user.api.serializers.profile import ProfileSerializer
from app_user.api.serializers.address import AddressSerializer
from app_education.api.serializers.high_school import HighSchoolSerializer
from app_education.api.serializers.bachelor_degree import BachelorDegreeSerializer
from app_education.api.serializers.master_degree import MasterDegreeSerializer
from app_occupation.api.serializers.latest_occupation import LatestOccupationSerializer

from utils.classes import ManageMailService
from utils.base_errors import BaseErrors

UserModel = get_user_model()


class ApplicationSerializer(serializers.ModelSerializer):
    user_detail = serializers.SerializerMethodField("get_user_detail")
    admin_message = serializers.SerializerMethodField("get_admin_message")
    degree_display = serializers.CharField(source="get_degree_display", read_only=True)
    faculty_display = serializers.SerializerMethodField("get_faculty_display")
    field_of_study_display = serializers.SerializerMethodField(
        "get_field_of_study_display"
    )
    application_documents = serializers.SerializerMethodField(
        "get_application_documents"
    )

    class Meta:
        model = ApplicationModel
        fields = (
            "id",
            "tracking_id",
            "full_name",
            "comments",
            "applied_program",
            "financial_self_support",
            "degree",
            "degree_display",
            "faculty",
            "faculty_display",
            "field_of_study",
            "field_of_study_display",
            "status",
            "created_at",
            "application_documents",
            "user_detail",
            "admin_message",
            "step",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "tracking_id": {"read_only": True},
            "full_name": {"required": False},
            "comments": {"required": False},
            "applied_program": {"required": False},
            "financial_self_support": {"required": False},
            "degree": {"required": False},
            "faculty": {"required": False},
            "field_of_study": {"required": False},
            "status": {"read_only": True},
            "created_at": {"read_only": True},
        }

    def __init__(self, *args, **kwargs):
        super(ApplicationSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get("request")
        if self.request:
            self.user = self.request.user
            self.method = self.request.method
            try:
                if self.user.is_agent:
                    self.fields["email"] = serializers.EmailField(
                        required=True, write_only=True
                    )
            except Exception:
                pass

    def get_application_documents(self, obj):
        try:
            application_document = obj.application_documents
            return {
                "id": application_document.id,
                "curriculum_vitae": application_document.get_field_image_url(
                    "curriculum_vitae", self.request
                ),
                "personal_photo": application_document.get_field_image_url(
                    "personal_photo", self.request
                ),
                "valid_passport": application_document.get_field_image_url(
                    "valid_passport", self.request
                ),
                "high_school_certificate": application_document.get_field_image_url(
                    "high_school_certificate", self.request
                ),
                "trans_script_high_school_certificate": application_document.get_field_image_url(
                    "trans_script_high_school_certificate", self.request
                ),
                "bachelor_degree": application_document.get_field_image_url(
                    "bachelor_degree", self.request
                ),
                "trans_script_bachelor_degree": application_document.get_field_image_url(
                    "trans_script_bachelor_degree", self.request
                ),
                "master_degree": application_document.get_field_image_url(
                    "master_degree", self.request
                ),
                "trans_script_master_degree": application_document.get_field_image_url(
                    "trans_script_master_degree", self.request
                ),
                "supporting_letter": application_document.get_field_image_url(
                    "supporting_letter", self.request
                ),
                "second_supporting_letter": application_document.get_field_image_url(
                    "second_supporting_letter", self.request
                ),
                "third_supporting_letter": application_document.get_field_image_url(
                    "third_supporting_letter", self.request
                ),
            }
        except Exception:
            return {
                "id": application_document.id,
                "curriculum_vitae": "",
                "personal_photo": "",
                "valid_passport": "",
                "high_school_certificate": "",
                "trans_script_high_school_certificate": "",
                "bachelor_degree": "",
                "trans_script_bachelor_degree": "",
                "master_degree": "",
                "trans_script_master_degree": "",
                "supporting_letter": "",
                "second_supporting_letter": "",
                "third_supporting_letter": "",
            }

    def get_user_detail(self, obj):
        return {
            "email": obj.user.email,
            "profile": ProfileSerializer(
                obj.user.user_profile, many=False, read_only=True, context=self.context
            ).data,
            "address": AddressSerializer(
                obj.user.user_address, many=False, read_only=True, context=self.context
            ).data,
            "high_school": HighSchoolSerializer(
                obj.user.user_high_school,
                many=False,
                read_only=True,
                context=self.context,
            ).data,
            "bachelor_degree": BachelorDegreeSerializer(
                obj.user.user_bachelor_degree,
                many=False,
                read_only=True,
                context=self.context,
            ).data,
            "master_degree": MasterDegreeSerializer(
                obj.user.user_master_degree,
                many=False,
                read_only=True,
                context=self.context,
            ).data,
            "latest_occupation": LatestOccupationSerializer(
                obj.user.user_latest_occupation,
                many=False,
                read_only=True,
                context=self.context,
            ).data,
        }

    def get_admin_message(self, obj):
        if obj.status == ApplicationModel.ApplicationStatusOptions.NeedToEdit:
            last_timeline = TimeLineModel.objects.filter(
                application=obj,
                status=TimeLineModel.TimeLineStatusOptions.NeedToEdit,
            ).last()
            if last_timeline is not None:
                return last_timeline.message
        return ""

    def get_faculty_display(self, obj):
        return getattr(obj.faculty, f"{self.request.LANGUAGE_CODE}_name")

    def get_field_of_study_display(self, obj):
        return getattr(obj.field_of_study, f"{self.request.LANGUAGE_CODE}_name")

    def create(self, validated_data):
        agent = None
        if self.user.is_agent:
            user_email = validated_data.pop("email")
            agent = self.user
            self.user = UserModel.objects.find_by_email(email=user_email)
            if self.user is None:
                self.user = UserModel.objects.create_user_with_pass(
                    email=user_email, password=self.user.password
                )
        find_application = ApplicationModel.objects.filter(
            user__user_profile__passport_number=self.user.user_profile.passport_number,
            status=ApplicationModel.ApplicationStatusOptions.Current,
            degree=validated_data["degree"],
            faculty=validated_data["faculty"],
            field_of_study=validated_data["field_of_study"],
        ).first()
        if find_application is None:
            application_obj = ApplicationModel.objects.create(
                user=self.user, agent=agent, **validated_data
            )
            have_document = False
            try:
                if application_obj.application_document is not None:
                    have_document = True
            except:
                pass
            if (
                application_obj.degree is not None
                and application_obj.field_of_study is not None
                and application_obj.faculty is not None
                # and application_obj.financial_self_support is not None
                # and application_obj.applied_program is not None
                and application_obj.full_name is not None
                and have_document
            ):
                user_mail = ManageMailService(application_obj.user.email)
                user_mail.send_email_to_user(
                    subject="New Application",
                    content={
                        "title": "message",
                        "data": {
                            "title": "Your Application successfully Created.",
                            "description": f"You have created a new application with a tracking code {application_obj.tracking_id}, please wait while it is checked. ",
                        },
                    },
                )
                application_obj.status = (
                    ApplicationModel.ApplicationStatusOptions.Current
                )
                application_obj.save()
                application_obj.update_application_file()
            return application_obj
        else:
            raise exceptions.ParseError(BaseErrors.cant_create_duplicate_application)

    def update(self, instance, validated_data):
        find_application = None
        try:
            find_application = (
                ApplicationModel.objects.filter(
                    user__user_profile__passport_number=instance.user.user_profile.passport_number,
                    status=ApplicationModel.ApplicationStatusOptions.Current,
                    degree=validated_data["degree"],
                    faculty=validated_data["faculty"],
                    field_of_study=validated_data["field_of_study"],
                )
                .exclude(id=instance.id)
                .first()
            )
        except KeyError:
            pass
        if find_application is None:
            for field_name in validated_data:  # update application fields
                setattr(instance, field_name, validated_data[field_name])
            have_document = False
            try:
                if instance.application_document is not None:
                    have_document = True
            except:
                pass
            if (
                instance.degree is not None
                and instance.field_of_study is not None
                and instance.faculty is not None
                # and instance.financial_self_support is not None
                # and instance.applied_program is not None
                and instance.full_name is not None
                and have_document
            ):
                if (
                    instance.status
                    == ApplicationModel.ApplicationStatusOptions.NeedToEdit
                ):
                    last_comment_in_application = TimeLineModel.objects.filter(
                        application=instance,
                        status=TimeLineModel.TimeLineStatusOptions.Investigation,
                    ).last()
                    if last_comment_in_application is not None:
                        ReferralModel.objects.create(
                            application=instance,
                            origin_user=instance.user,
                            destination_user=last_comment_in_application.user,
                        )
                        TimeLineModel.objects.create(
                            application=instance,
                            user=instance.user,
                            status=TimeLineModel.TimeLineStatusOptions.Referral,
                            message="رفع ایرادات از سمت کاربر",
                        )
                else:
                    user_mail = ManageMailService(instance.user.email)
                    user_mail.send_email_to_user(
                        subject="New Application",
                        content={
                            "title": "message",
                            "data": {
                                "title": "Your Application successfully Created.",
                                "description": f"You have created a new application with a tracking code {instance.tracking_id}, please wait while it is checked. ",
                            },
                        },
                    )
                instance.status = ApplicationModel.ApplicationStatusOptions.Current
            instance.save()
            instance.update_application_file()
            return instance
        else:
            raise exceptions.ParseError(BaseErrors.cant_create_duplicate_application)
