from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    # account registration
    path("register/", views.RegisterAPIView.as_view(), name="registration-api"),

    # simple token operations
    path("token/login/", views.CustomObtainAuthToken.as_view(), name="token-login"),
    path("token/logout/", views.DiscardAuthToken.as_view(), name='token-logout'),


    # jwt

    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt-create"),


    # reset password

    path("reset-password/", views.ResetPasswordAPIView.as_view(), name="reset-password")



    # account reset password
]