from rest_framework import serializers, exceptions

from app_application.models import DocumentModel, ApplicationModel

from utils import BaseErrors


class DocumentsSerializer(serializers.ModelSerializer):
    tracking_id = serializers.CharField(max_length=12, required=False, write_only=True)

    class Meta:
        model = DocumentModel
        fields = (
            "id",
            "tracking_id",
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
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def __init__(self, *args, **kwargs):
        super(DocumentsSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get("request")
        if self.request:
            self.user = self.request.user
            self.method = self.request.method
            if self.method in ["PUT", "PATCH"]:
                for field_name, field in self.fields.items():
                    field.required = False

    def validate_tracking_id(self, value):
        if self.user.is_agent:
            application_obj = ApplicationModel.objects.filter(
                tracking_id=value, agent=self.user
            ).first()
        else:
            application_obj = ApplicationModel.objects.filter(
                tracking_id=value, user=self.user
            ).first()
        if application_obj is not None:
            self.user = application_obj.user
            return application_obj
        else:
            raise exceptions.NotFound(BaseErrors.tracking_id_not_found)

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

    def create(self, validated_data):
        application_obj = validated_data.pop("tracking_id", None)
        try:
            if application_obj.application_document is not None:
                application_obj.application_document.delete()
        except:
            pass
        document_obj = DocumentModel.objects.create(
            application=application_obj, user=self.user, **validated_data
        )
        application_obj.update_application_file()
        return document_obj

    def update(self, instance, validated_data):
        try:
            application_obj = validated_data.pop("tracking_id")
        except Exception:
            application_obj = None
        validated_data["application"] = application_obj
        for field_name in validated_data:  # update document fields
            setattr(instance, field_name, validated_data[field_name])
        instance.save()
        application_obj.update_application_file()
        return instance
