from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import EMAIL_HOST_USER
from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    qureset = User.objects.all()


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"http://localhost:8000/users/reset_password_confirm/?uid={uid}&token={token}"

        # Создаем HTML-сообщение
        message = f"""
            <html>
                <body>
                    <p>Здравствуйте!</p>
                    <p>Чтобы сбросить пароль, перейдите по следующей ссылке:</p>
                    <p><a>{reset_link}</a></p>
                </body>
            </html>
            """

        # Отправка электронной почты с ссылкой для сброса пароля
        send_mail(
            subject="Восстановление пароля",
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
            html_message=message,
        )

        return Response(
            {"message": "Ссылка для сброса пароля отправлена на вашу почту."},
            status=status.HTTP_200_OK,
        )


class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        try:
            uid_decoded = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid_decoded)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response(
                {"message": "Пароль успешно изменен."}, status=status.HTTP_200_OK
            )

        return Response(
            {"error": "Неверная ссылка или токен."}, status=status.HTTP_400_BAD_REQUEST
        )
