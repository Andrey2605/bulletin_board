import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ads.models import Ads, Review
from users.models import User


@pytest.mark.django_db
class AdsCaseTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru", password="password")
        self.client.force_authenticate(user=self.user)

    def test_create_ads(self):
        response = self.client.post(
            reverse("ads:ads-list"),
            {
                "title": "New Ads",
                "price": 150,
                "description": "Description of new ads.",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "New Ads"

    def test_list_ads(self):
        # Создаем несколько объявлений
        Ads.objects.create(
            title="Ads 1", price=100, description="First ads", author=self.user
        )
        Ads.objects.create(
            title="Ads 2", price=200, description="Second ads", author=self.user
        )

        response = self.client.get(reverse("ads:ads-list"))

        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_ads(self):
        ads = Ads.objects.create(
            title="Test Ads",
            price=100,
            description="Test description",
            author=self.user,
        )

        response = self.client.get(reverse("ads:ads-detail", args=[ads.id]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Test Ads"

    def test_update_ads(self):
        ads = Ads.objects.create(
            title="Old Title",
            price=100,
            description="Old description",
            author=self.user,
        )

        response = self.client.patch(
            reverse("ads:ads-detail", args=[ads.id]), {"title": "Updated Title"}
        )

        ads.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert ads.title == "Updated Title"

    def test_delete_ads(self):
        ads = Ads.objects.create(
            title="To be deleted",
            price=100,
            description="Delete this ads",
            author=self.user,
        )

        response = self.client.delete(reverse("ads:ads-detail", args=[ads.id]))

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class ReviewCaseTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru", password="password")
        self.ads = Ads.objects.create(title="Test", price=100, description="Test")
        self.client.force_authenticate(user=self.user)

    def test_create_review(self):
        response = self.client.post(
            reverse("ads:review-list"),
            {"text": "New Review", "author": self.user.id, "ad": self.ads.id},
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["text"] == "New Review"

    def test_list_review(self):
        # Создаем несколько объявлений
        Review.objects.create(text="Review 1", author=self.user, ad=self.ads)
        Review.objects.create(text="Review 2", author=self.user, ad=self.ads)

        response = self.client.get(reverse("ads:review-list"))

        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_review(self):
        review = Review.objects.create(
            text="Test Review", author=self.user, ad=self.ads
        )

        response = self.client.get(reverse("ads:review-detail", args=[review.id]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["text"] == "Test Review"

    def test_update_review(self):
        review = Review.objects.create(text="Old Title", author=self.user, ad=self.ads)

        response = self.client.patch(
            reverse("ads:review-detail", args=[review.id]), {"text": "Updated Title"}
        )

        review.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert review.text == "Updated Title"

    def test_delete_review(self):
        review = Review.objects.create(
            text="To be deleted", author=self.user, ad=self.ads
        )

        response = self.client.delete(reverse("ads:review-detail", args=[review.id]))

        assert response.status_code == status.HTTP_204_NO_CONTENT
