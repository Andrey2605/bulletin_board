from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from ads.models import Ads, Review
from ads.paginators import CustomPagination
from ads.serializers import AdsSerializer, ReviewSerializer


class AdsViewSet(ModelViewSet):
    serializer_class = AdsSerializer
    queryset = Ads.objects.all()
    pagination_class = CustomPagination

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("title",)  # Укажите поля, по которым хотите фильтровать

    def get_permissions(self):
        if self.request.method == "GET":
            if self.action == "list":
                return [
                    permissions.AllowAny()
                ]  # Анонимные пользователи могут получать список объявлений
            else:
                return [
                    permissions.IsAuthenticated()
                ]  # Остальные действия требуют аутентификации

        if self.request.user.is_staff:
            return [
                permissions.IsAuthenticated()
            ]  # Администраторы могут выполнять все действия

        return [
            permissions.IsAuthenticated()
        ]  # Остальные пользователи должны быть аутентифицированы

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        ads = self.get_object()
        if ads.author != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Вы не можете редактировать это объявление.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Вы не можете удалить это объявление.")
        instance.delete()


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [
                permissions.IsAuthenticated()
            ]  # Только аутентифицированные пользователи могут получать список комментариев

        if self.request.user.is_staff:
            return [
                permissions.IsAuthenticated()
            ]  # Администраторы могут выполнять все действия

        return [
            permissions.IsAuthenticated()
        ]  # Остальные пользователи должны быть аутентифицированы

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        review = self.get_object()
        if review.author != self.request.user:
            raise PermissionDenied("Вы не можете редактировать этот комментарий.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("Вы не можете удалить этот комментарий.")
        instance.delete()
