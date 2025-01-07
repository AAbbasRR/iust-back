from django.urls import path

from .views import *

app_name = "app_user"
urlpatterns = [
    # register and active account
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path(
        "register/active_account/",
        UserVerifyRegisterView.as_view(),
        name="user_active_account",
    ),
    path(
        "register/resent_activate_code/",
        UserReSendRegisterOTPCodeView.as_view(),
        name="user_resent_active_code",
    ),
    # login
    path("login/", UserLoginView.as_view(), name="user_login"),
    # forget password
    path("forget_password/", ForgetPasswordView.as_view(), name="user_forget_password"),
    path(
        "forget_password/validate/",
        ValidateForgetPasswordOTPView.as_view(),
        name="user_validate_forget_password",
    ),
    path(
        "forget_password/complete/",
        CompleteForgetPasswordView.as_view(),
        name="user_complete_forget_password",
    ),
    # admin staffs
    path("agents/list/", AdminAgentsListAPIView.as_view(), name="admin_agents_list"),
    path(
        "agents/update/<int:pk>/",
        AdminAgentUpdateAPIView.as_view(),
        name="admin_agents_update",
    ),
    path(
        "agents/list_applications/",
        AdminAgentListApplicationsAPIView.as_view(),
        name="admin_agents_applications_list",
    ),
    # change password
    path("change_password/", ChangePasswordView.as_view(), name="user_change_password"),
    # manage profile account
    path(
        "profile/detail_update/",
        ProfileDetailUpdateView.as_view(),
        name="user_detail_update_profile",
    ),
    path(
        "profile/info/detail_update/",
        ProfileInfoDetailUpdateView.as_view(),
        name="user_info_detail_update_profile",
    ),
    # manage address account
    path(
        "address/detail_update/",
        AddressDetailUpdateView.as_view(),
        name="user_detail_update_address",
    ),
    # user details
    path("user/detail/", UserProfileDetailView.as_view(), name="user_detail"),
    # admin details
    path("admin/detail/", AdminDetailDataView.as_view(), name="admin_detail"),
]
