import pytest
from accounts.models import User
from rest_framework.test import APIClient
from ..models import Objective
from django.urls import reverse


@pytest.fixture
def user_object():
    user = User.objects.create_user(
        username="arvin",
        password="qazwsx123890",
    )
    return user


@pytest.fixture
def objective_object(user_object):
    objective = Objective.objects.create(
        owner=user_object,
        title="test title",
        description="test description",
    )
    return objective


@pytest.mark.django_db
class TestObjectiveAPI:

    client = APIClient()

    def test_objective_list_status_200(self, user_object):
        url = reverse("home:api-v1:objective-list")
        self.client.force_login(user=user_object)
        response = self.client.get(url)
        assert response.status_code == 200

    def test_objective_list_status_401(self):
        url = reverse("home:api-v1:objective-list")
        response = self.client.get(url)
        assert response.status_code == 401

    def test_objective_create_status_201(self, user_object):
        url = reverse("home:api-v1:objective-list")
        self.client.force_login(user=user_object)
        data = {
            "title": "test pytest",
            "description": "test des 2",
            "status": False,
        }
        response = self.client.post(url, data=data)
        assert response.status_code == 201

    def test_objective_detail_status_200(self, user_object, objective_object):
        url = reverse(
            "home:api-v1:objective-detail", kwargs={"pk": objective_object.pk}
        )
        self.client.force_login(user=user_object)
        response = self.client.get(url)
        assert response.status_code == 200

    def test_objective_detail_status_401(self, objective_object):
        url = reverse(
            "home:api-v1:objective-detail", kwargs={"pk": objective_object.pk}
        )
        response = self.client.get(url)
        assert response.status_code == 401

    def test_objectove_update_put_status_200(self, user_object, objective_object):
        url = reverse(
            "home:api-v1:objective-detail", kwargs={"pk": objective_object.pk}
        )
        self.client.force_login(user=user_object)
        data = {
            "title": "test pytest",
            "description": "test des 2",
            "status": False,
        }
        response = self.client.put(url, data=data)
        assert response.status_code == 200

    def test_objective_update_put_status_400(self, user_object, objective_object):
        url = reverse(
            "home:api-v1:objective-detail", kwargs={"pk": objective_object.pk}
        )
        self.client.force_login(user=user_object)
        data = {
            "description": "test des 2",
            "status": False,
        }
        response = self.client.put(url, data=data)
        assert response.status_code == 401

    def test_objective_update_patch_status_200(self, user_object, objective_object):
        url = reverse(
            "home:api-v1:objective-detail", kwargs={"pk": objective_object.pk}
        )
        self.client.force_login(user=user_object)
        data = {
            "description": "test des 2",
            "status": False,
        }
        response = self.client.patch(url, data=data)
        assert response.status_code == 200

    def test_objective_delete_status_204(self, user_object, objective_object):
        url = reverse(
            "home:api-v1:objective-detail", kwargs={"pk": objective_object.pk}
        )
        self.client.force_login(user=user_object)
        response = self.client.delete(url)
        assert response.status_code == 204
