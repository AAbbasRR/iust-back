from .register import (
    UserRegisterView,
    UserVerifyRegisterView,
    UserReSendRegisterOTPCodeView,
)
from .login import UserLoginView
from .google_auth import UserRegisterLoginGoogleAuthView
from .forget_password import (
    ForgetPasswordView,
    ValidateForgetPasswordOTPView,
    CompleteForgetPasswordView,
)
from .change_password import ChangePasswordView
from .profile import ProfileDetailUpdateView, ProfileInfoDetailUpdateView
from .address import AddressDetailUpdateView
from .user import UserProfileDetailView
from .admin_detail import AdminDetailDataView
from .agents_admin import (
    AdminAgentsListCreateAPIView,
    AdminAgentUpdateAPIView,
    AdminAgentRejectAccountAPIView,
    AdminAgentAcceptAccountAPIView,
)
from .users_admin import AdminAllUserView
