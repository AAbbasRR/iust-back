from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers, exceptions

from utils import RedisKeys, Redis, BaseErrors, ManageMailService

UserModel = get_user_model()


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(ForgetPasswordSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate_email(self, value):
        user_obj = UserModel.objects.find_by_email(value.lower())
        if user_obj is None:
            raise exceptions.NotFound(BaseErrors.user_not_found)
        self.user = user_obj
        return value.lower()

    def validate(self, attrs):
        redis_management = Redis(
            self.user.email, f"{RedisKeys.forget_password}_otp_code"
        )
        if redis_management.exists():
            raise exceptions.ParseError(
                {
                    "message": BaseErrors.otp_code_has_already_been_sent,
                    "time": redis_management.get_expire(),
                }
            )
        else:
            manage_email_obj = ManageMailService(self.user.email)
            manage_email_obj.send_otp_code(RedisKeys.forget_password)
            return True


class ValidateForgetPasswordOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
    )
    otp_code = serializers.IntegerField(
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(ValidateForgetPasswordOTPSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate_email(self, value):
        user_obj = UserModel.objects.find_by_email(value)
        if user_obj is None:
            raise exceptions.NotFound(BaseErrors.user_not_found)
        self.user = user_obj
        return value

    def validate(self, attrs):
        redis_management = Redis(
            self.user.email, f"{RedisKeys.forget_password}_otp_code"
        )
        result_check_validate = redis_management.validate(attrs["otp_code"])
        if result_check_validate is None:
            raise exceptions.ParseError(BaseErrors.otp_code_expired)
        else:
            if result_check_validate is False:
                raise exceptions.ParseError(BaseErrors.invalid_otp_code)
            else:
                redis_management.delete()
                redis_management = Redis(self.user.email, RedisKeys.forget_password)
                redis_management.set_status_value(True)
                redis_management.set_expire(
                    redis_management.expire_times["forget_password"]
                )
                return True


class CompleteForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
    )
    re_password = serializers.CharField(
        required=True,
        write_only=True,
    )

    def __init__(self, *args, **kwargs):
        super(CompleteForgetPasswordSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate_email(self, value):
        user_obj = UserModel.objects.find_by_email(value)
        if user_obj is None:
            raise exceptions.NotFound(BaseErrors.user_not_found)
        self.user = user_obj
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["re_password"]:
            raise exceptions.ParseError(BaseErrors.passwords_did_not_match)
        redis_management = Redis(self.user.email, RedisKeys.forget_password)
        if redis_management.get_status_value():
            self.user.change_password(attrs["password"])
            redis_management.delete()
            return True
        else:
            raise exceptions.ParseError(
                BaseErrors.user_dont_have_forget_password_permission
            )
