from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from app_application.models import DocumentModel

import os


@receiver(post_delete, sender=DocumentModel)
def delete_document_handler(sender, instance, **kwargs):
    file_field_names = [
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
    ]
    for field_name in file_field_names:
        if getattr(instance, field_name):
            document_path = getattr(instance, field_name).path
            os.remove(document_path)


@receiver(pre_save, sender=DocumentModel)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    else:
        try:
            pre_obj = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return False

        file_field_names = [
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
        ]
        # for field_name in file_field_names:
        #     if getattr(instance, field_name):
        #         document_path = getattr(pre_obj, field_name).path
        #         os.remove(document_path)
