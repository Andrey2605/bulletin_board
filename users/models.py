from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("user", "User"),
        ("admin", "Admin"),
    )

    username = None
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя пользователя",
        help_text="Введите имя",
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия пользователя",
        help_text="Введите фамилию",
        blank=True,
        null=True,
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона",
        blank=True,
        null=True,
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default="user")
    image = models.ImageField(
        upload_to="media/", verbose_name="Аватар", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
