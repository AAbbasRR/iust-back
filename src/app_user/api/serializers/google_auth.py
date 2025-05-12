from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from app_user.models import UserModel

import requests


class UserRegisterLoginGoogleAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=255, required=True)

    def validate(self, attrs):
        google_response = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            params={"access_token": attrs["access_token"]},
            timeout=5,
        )
        if google_response.status_code != 200:
            return serializers.ValidationError(_("Invalid Google Token"))

        user_info = google_response.json()
        email = user_info.get("email")
        password = user_info.get("sub")

        user = UserModel.objects.find_by_email(email=email)
        if user is None:
            user = UserModel.objects.register_user(
                email.lower(),
                password,
                False,
                True,
                is_active=True,
            )
        else:
            if user.is_active is False:
                user.is_active = True
                user.save()

        user.set_last_login()
        user_token = Token.objects.get(user=user)
        return {
            "id": user.id,
            "email": user.email,
            "auth_token": user_token.key,
            "is_agent": user.is_agent,
            "sso_signup": user.sso_signup,
        }
