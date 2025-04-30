import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient  # Импортируем APIClient
from ads.models import Ads, Review
from users.models import User

@pytest.fixture
def user():
    return User.objects.create(email="test@mail.ru", password="password")

@pytest.fixture
def authenticated_client(user):
    client = APIClient()  # Создаем экземпляр APIClient
    client.force_authenticate(user=user)  # Аутентифицируем пользователя
    return client

@pytest.fixture
def ads_instance(user):
    return Ads.objects.create(title="Test Ads", price=100, description="Test description", author=user)

@pytest.mark.django_db
def test_create_ads(authenticated_client):
    response = authenticated_client.post(
        reverse("ads:ads-list"),
        {
            "title": "New Ads",
            "price": 150,
            "description": "Description of new ads.",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "New Ads"

@pytest.mark.django_db
def test_list_ads(authenticated_client, user):
    Ads.objects.create(title="Ads 1", price=100, description="First ads", author=user)
    Ads.objects.create(title="Ads 2", price=200, description="Second ads", author=user)

    response = authenticated_client.get(reverse("ads:ads-list"))

    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_retrieve_ads(authenticated_client, ads_instance):
    response = authenticated_client.get(reverse("ads:ads-detail", args=[ads_instance.id]))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Test Ads"

@pytest.mark.django_db
def test_update_ads(authenticated_client, ads_instance):
    response = authenticated_client.patch(
        reverse("ads:ads-detail", args=[ads_instance.id]), {"title": "Updated Title"}
    )

    ads_instance.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert ads_instance.title == "Updated Title"

@pytest.mark.django_db
def test_delete_ads(authenticated_client, ads_instance):
    response = authenticated_client.delete(reverse("ads:ads-detail", args=[ads_instance.id]))

    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.fixture
def review_instance(user, ads_instance):
    return Review.objects.create(text="Test Review", author=user, ad=ads_instance)

@pytest.mark.django_db
def test_create_review(authenticated_client, ads_instance, user):
    response = authenticated_client.post(
        reverse("ads:review-list"),
        {"text": "New Review", "author": user.id, "ad": ads_instance.id},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["text"] == "New Review"

@pytest.mark.django_db
def test_list_review(authenticated_client, review_instance):
    Review.objects.create(text="Review 1", author=review_instance.author, ad=review_instance.ad)
    Review.objects.create(text="Review 2", author=review_instance.author, ad=review_instance.ad)

    response = authenticated_client.get(reverse("ads:review-list"))

    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_retrieve_review(authenticated_client, review_instance):
    response = authenticated_client.get(reverse("ads:review-detail", args=[review_instance.id]))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["text"] == "Test Review"

@pytest.mark.django_db
def test_update_review(authenticated_client, review_instance):
    response = authenticated_client.patch(
        reverse("ads:review-detail", args=[review_instance.id]), {"text": "Updated Title"}
    )

    review_instance.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert review_instance.text == "Updated Title"

@pytest.mark.django_db
def test_delete_review(authenticated_client, review_instance):
    response = authenticated_client.delete(reverse("ads:review-detail", args=[review_instance.id]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
