from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView
from .. import views

app_name = "account-urls"

urlpatterns = [
    # account registration
    path("register/", views.RegisterAPIView.as_view(), name="registration-api"),

    # simple token operations
    path("token/login/", views.CustomObtainAuthToken.as_view(), name="token-login"),
    path("token/logout/", views.DiscardAuthToken.as_view(), name='token-logout'),

    #verification

    path("verify-account/<str:access_jwt>", views.VerificationTokenAPIView.as_view(), name="verify-account"),
    path("verify-resend/", views.ResendVerificationAPIView.as_view(), name="verify-resend"),

    # jwt

    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),


    # reset password

    path("reset-password/", views.ResetPasswordAPIView.as_view(), name="reset-password"),

    # forgot password

    path("forgot-password/", views.ForgotPasswordAPIView.as_view(), name="forgot-password"),
    path("new-password/<str:reset_pass_jwt>", views.NewPasswordForgotAPIView.as_view(), name="new-password"),
    
]