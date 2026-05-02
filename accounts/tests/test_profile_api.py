import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from ..models import profiles, User


@pytest.fixture
def user_object():
    user = User.objects.create_user(
        username="pytest_profile",
        password="qazwsx123890",
    )
    return user

@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestProfile:

    def test_get_profile_status_200(self, api_client, user_object):
        url = reverse("accounts:all-api-urls:profile-urls:profile-api")
        api_client.force_login(user=user_object)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_put_profile_status_200(self, api_client, user_object):
        url = reverse("accounts:all-api-urls:profile-urls:profile-api")
        api_client.force_login(user=user_object)
        data = {
        "first_name": "pytest",
        "last_name": "proifle",
        "country": "america",
        "phone": "238575"
        }
        response = api_client.put(url, data)
        assert response.status_code == 200
    
    def test_patch_profile_status_200(self, api_client, user_object):
        url = reverse("accounts:all-api-urls:profile-urls:profile-api")
        api_client.force_login(user=user_object)
        data = {
        "first_name": "pytest",
        }
        response = api_client.patch(url, data)
        assert response.status_code == 200