from django.db import models

from users.models import User


class Ads(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name="Название объявления",
        help_text="Введите название объявления",
        blank=True,
        null=True,
    )
    price = models.IntegerField(verbose_name="Цена", help_text="Введите цену")
    description = models.TextField(
        verbose_name="Описание", help_text="Напишите описание", blank=True, null=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]


class Review(models.Model):
    text = models.TextField(
        verbose_name="Отзыв", help_text="Напишите отзыв", blank=True, null=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор", blank=True, null=True
    )
    ad = models.ForeignKey(Ads, on_delete=models.CASCADE, verbose_name="Объявление")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзыва"
