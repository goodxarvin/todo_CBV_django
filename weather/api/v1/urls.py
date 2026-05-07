from django.urls import path
from . import views 
app_name = "weather-api-urls"

urlpatterns = [
    path("info/", views.InfoExampleAPIView.as_view(), name="info-example")
]