from django.urls import include, path
from .accounts import *
from .profiles import *



urlpatterns = [
    path("", include("accounts.api.v1.urls.accounts"), name="account-urls"),
    path("profile/", include("accounts.api.v1.urls.profiles")),
]