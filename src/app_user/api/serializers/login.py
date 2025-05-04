from django.contrib.auth import get_user_model

from rest_framework import exceptions, serializers
from rest_framework.authtoken.models import Token

from utils import BaseErrors, ManageMailService, RedisKeys

UserModel = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
    )

    def validate_email(self, value):
        return value.lower()

    def validate(self, attrs):
        user_obj = UserModel.objects.find_by_email(email=attrs["email"])
        if user_obj is None or user_obj.check_password(attrs["password"]) is False:
            raise exceptions.ParseError(BaseErrors.invalid_email_or_password)
        else:
            if user_obj.is_active is False:
                manage_email_obj = ManageMailService(user_obj.email)
                manage_email_obj.send_otp_code(RedisKeys.activate_account)
                raise exceptions.ParseError(BaseErrors.user_account_not_active)
            else:
                if not user_obj.locked:
                    user_obj.set_last_login()
                    user_token = Token.objects.get(user=user_obj)
                    return {
                        "id": user_obj.id,
                        "email": user_obj.email,
                        "auth_token": user_token.key,
                        "is_agent": user_obj.is_agent,
                        "sso_signup": user_obj.sso_signup,
                    }
                else:
                    raise exceptions.ParseError(BaseErrors.user_account_is_locked)
