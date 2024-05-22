from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from app_user.models import UserModel
from app_admin.models import AdminModel
from app_admin.api.serializers.oauth import data

import csv
import codecs


class Command(BaseCommand):
    help = "Command for Create All Staffs"

    def handle(self, *args, **options):
        staffs_path = "staffs.csv"
        with open(staffs_path, "rb") as staffs_file:
            staff_reader = csv.reader(codecs.iterdecode(staffs_file, "utf-8"))
            staff_header = next(staff_reader)
            for row in staff_reader:
                _object_dict = {key: value for key, value in zip(staff_header, row)}
                try:
                    user_obj, created = UserModel.objects.get_or_create(
                        username=_object_dict["username"],
                        is_active=True,
                        is_staff=True,
                    )
                    user_obj.save()

                    if created:
                        find_school = list(
                            filter(
                                lambda item: item["label"] == _object_dict["perName"],
                                data["Master"]["items"],
                            )
                        )
                        if len(find_school) > 0:
                            fields_school = list(
                                filter(
                                    lambda item: item["label"]
                                    == _object_dict["groupname"],
                                    data["Master"]["data"][find_school[0]["value"]],
                                )
                            )
                            if len(fields_school) == 0:
                                print(data["Master"]["data"][find_school[0]["value"]])
                                print(_object_dict["groupname"])
                            if len(fields_school) > 0:
                                role = AdminModel.AdminRoleOptions.department_member
                                if bool(_object_dict["isgrouphead"]):
                                    role = AdminModel.AdminRoleOptions.department_head
                                if bool(_object_dict["isdepchief"]):
                                    role = AdminModel.AdminRoleOptions.faculty_director
                                AdminModel.objects.create(
                                    user=user_obj,
                                    role=role,
                                    schools=find_school[0]["value"],
                                    fields=fields_school[0]["value"],
                                )
                    user_profile = user_obj.user_profile
                    user_profile.first_name = _object_dict["firstname"]
                    user_profile.last_name = _object_dict["lastname"]
                    user_profile.save()
                except IntegrityError:
                    pass
