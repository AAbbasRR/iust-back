from django.contrib.auth import get_user_model

from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator

from utils import Redis, BaseErrors, RedisKeys, ManageMailService

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=UserModel.objects.all(),
                message=BaseErrors.user_account_with_email_exists,
            )
        ],
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
    )
    sso_signup = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = UserModel
        fields = ("email", "password", "is_agent")

    def create(self, validated_data):
        user = UserModel.objects.register_user(
            validated_data["email"],
            validated_data["password"],
            validated_data["is_agent"],
            validated_data["sso_signup"],
        )
        return user


class UserVerifyRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
    )
    otp_code = serializers.IntegerField(
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(UserVerifyRegisterSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate_email(self, value):
        user_obj = UserModel.objects.find_by_email(value)
        if user_obj is None:
            raise exceptions.NotFound(BaseErrors.user_not_found)
        self.user = user_obj
        return value

    def validate(self, attrs):
        redis_management = Redis(
            self.user.email, f"{RedisKeys.activate_account}_otp_code"
        )
        result_check_validate = redis_management.validate(attrs["otp_code"])
        if result_check_validate is None:
            raise exceptions.ParseError(BaseErrors.otp_code_expired)
        else:
            if result_check_validate is False:
                raise exceptions.ParseError(BaseErrors.invalid_otp_code)
            else:
                redis_management.delete()
                self.user.activate()
                return True


class UserReSendRegisterOTPCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(UserReSendRegisterOTPCodeSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate_email(self, value):
        user_obj = UserModel.objects.find_by_email(value)
        if user_obj is None:
            raise exceptions.NotFound(BaseErrors.user_not_found)
        self.user = user_obj
        return value

    def validate(self, attrs):
        if self.user.is_active:
            raise exceptions.ParseError(BaseErrors.user_account_is_active)
        redis_management = Redis(
            self.user.email, f"{RedisKeys.activate_account}_otp_code"
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
            manage_email_obj.send_otp_code(RedisKeys.activate_account)
            return True
