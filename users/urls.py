from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (ResetPasswordConfirmView, ResetPasswordView,
                         UserCreateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register "),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("reset_password/", ResetPasswordView.as_view(), name="reset_password"),
    path(
        "reset_password_confirm/",
        ResetPasswordConfirmView.as_view(),
        name="reset_password_confirm",
    ),
]
