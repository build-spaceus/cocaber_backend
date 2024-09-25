from django.urls import path

from api.v1.auth.views import (
    LoginSendOTPView,
    LoginTokenRefreshView,
    LoginVerifyOTPView,
    LogoutView,
    ProfileView,
)

urlpatterns = [
    path(
        "login/send-otp/",
        LoginSendOTPView.as_view(),
        name="internal-v1-login-send-otp",
    ),
    path(
        "login/verify-otp/",
        LoginVerifyOTPView.as_view(),
        name="internal-v1-login-verify-otp",
    ),
    path(
        "login/refresh/",
        LoginTokenRefreshView.as_view(),
        name="internal-v1-token-refresh-otp",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="internal-v1-logout",
    ),
    path(
        "profile/",
        ProfileView.as_view(),
        name="internal-v1-profile",
    ),
]
