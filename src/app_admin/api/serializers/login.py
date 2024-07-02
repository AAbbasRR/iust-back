from rest_framework import exceptions, serializers
from rest_framework.authtoken.models import Token

from app_user.models import UserModel

from utils import BaseErrors


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
    )

    def validate(self, attrs):
        user_obj = UserModel.objects.find_admin_by_email(email=attrs["email"])
        if user_obj is None or user_obj.check_password(attrs["password"]) is False:
            raise exceptions.ParseError(BaseErrors.invalid_email_or_password)
        else:
            user_obj.set_last_login()
            user_token = Token.objects.get(user=user_obj)
            return {
                "id": user_obj.id,
                "sub": user_obj.sub,
                "email": user_obj.email,
                "is_superuser": user_obj.is_superuser,
                "is_staff": user_obj.is_staff,
                "username": user_obj.username,
                "picurl": user_obj.picurl,
                "full_name": user_obj.get_full_name(),
                "auth_token": user_token.key,
                "can_issuance_letter": user_obj.can_issuance_letter,
                "is_agent": user_obj.is_agent,
            }
