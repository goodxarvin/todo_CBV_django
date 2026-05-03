import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from ..models import User
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def user_object():
    user = User.objects.create_user(
        username="test_pytest",
        password="qazwsx123890",
    )
    return user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestAccountAPI:

    def test_registration_status_201(self, api_client):
        url = reverse("accounts:all-api-urls:account-urls:registration-api")
        data = {
            "username": "test_registartion",
            "password": "qazwsx123890",
            "password1": "qazwsx123890",
        }
        response = api_client.post(url, data=data)
        assert response.status_code == 201

    def test_authtoken_login_status_201(self, api_client, user_object):
        url = reverse("accounts:all-api-urls:account-urls:token-login")
        data = {
            "username": "test_pytest",
            "password": "qazwsx123890",
        }
        response = api_client.post(url, data=data)
        assert response.status_code == 201

    def test_authtoken_logout_status_204(self, api_client, user_object):
        url = reverse("accounts:all-api-urls:account-urls:token-logout")
        token = Token.objects.create(user=user_object)
        api_client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = api_client.post(url)
        assert response.status_code == 204

    def test_reset_password_status_200(self, api_client, user_object):
        url = reverse("accounts:all-api-urls:account-urls:reset-password")
        api_client.force_login(user=user_object)
        data = {
            "old_pass": "qazwsx123890",
            "new_pass": "string123",
            "confirm_pass": "string123",
        }
        response = api_client.post(url, data=data)
        assert response.status_code == 200

    def test_reset_password_status_400(self, api_client, user_object):
        url = reverse("accounts:all-api-urls:account-urls:reset-password")
        api_client.force_login(user=user_object)
        data = {
            "old_pass": "qazwsx12890",
            "new_pass": "string123",
            "confirm_pass": "string123",
        }
        response = api_client.post(url, data=data)
        assert response.status_code == 400

    def test_jwt_create_status_200(self, api_client, user_object):
        url = reverse("accounts:all-api-urls:account-urls:jwt-create")
        data = {
            "username": "test_pytest",
            "password": "qazwsx123890",
        }
        response = api_client.post(url, data=data)
        assert response.status_code == 200

    def test_jwt_refresh_status_200(self, api_client, user_object):
        url = reverse("accounts:all-api-urls:account-urls:jwt-refresh")
        refresh_token = RefreshToken.for_user(user_object)
        refresh_token_str = str(refresh_token)
        data = {"refresh": refresh_token_str}
        response = api_client.post(url, data=data)
        assert response.status_code == 200

    def test_jwt_access_verify_status_200(self, api_client, user_object):
        url = reverse("accounts:all-api-urls:account-urls:jwt-verify")
        str_access_token = str(RefreshToken.for_user(user_object).access_token)
        data = {"token": str_access_token}
        response = api_client.post(url, data=data)
        assert response.status_code == 200

    def test_jwt_refresh_verify_status_200(self, api_client, user_object):
        url = reverse("accounts:all-api-urls:account-urls:jwt-verify")
        str_refresh_token = str(RefreshToken.for_user(user_object))
        data = {"token": str_refresh_token}
        response = api_client.post(url, data=data)
        assert response.status_code == 200

    def test_forgot_password_status_200(self, api_client, user_object):
        url = reverse("accounts:all-api-urls:account-urls:forgot-password")
        data = {"username": "test_pytest"}
        response = api_client.post(url, data)
        print(response.data)
        assert response.status_code == 200

    def test_new_password_forgot_200(self, api_client, user_object):
        str_access_token = str(RefreshToken.for_user(user_object).access_token)
        url = reverse(
            "accounts:all-api-urls:account-urls:new-password",
            kwargs={"reset_pass_jwt": str_access_token},
        )
        data = {
            "new_pass": "string123",
            "confirm_pass": "string123",
        }
        response = api_client.post(url, data)
        assert response.status_code == 200

    def test_new_password_forgot_400(self, api_client, user_object):
        str_access_token = str(RefreshToken.for_user(user_object).access_token)
        url = reverse(
            "accounts:all-api-urls:account-urls:new-password",
            kwargs={"reset_pass_jwt": str_access_token},
        )
        data = {
            "new_pass": "string13",
            "confirm_pass": "string123",
        }
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_verify_resend_status_200(self, api_client, user_object):
        url = reverse("accounts:all-api-urls:account-urls:verify-resend")
        api_client.force_login(user=user_object)
        response = api_client.post(url)
        assert response.status_code == 200

    def test_verify_account_status_200(self, api_client, user_object):
        str_access_token = str(RefreshToken.for_user(user_object).access_token)
        url = reverse(
            "accounts:all-api-urls:account-urls:verify-account",
            kwargs={"access_jwt": str_access_token},
        )
        response = api_client.get(url)
        assert response.status_code == 200

    def test_verify_account_status_400(self, api_client, user_object):
        # str_access_token = str(RefreshToken.for_user(user_object).access_token)
        url = reverse(
            "accounts:all-api-urls:account-urls:verify-account",
            kwargs={"access_jwt": "test_400"},
        )
        response = api_client.get(url)
        assert response.status_code == 400
