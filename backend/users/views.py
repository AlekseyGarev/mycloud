import logging

from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from storage.models import File
from storage.serializers import FileSerializer
from users.models import User
from users.serializers import (
    AdminUserUpdateSerializer,
    UserRegisterSerializer,
    UserSerializer,
)

logger = logging.getLogger("users")


def get_csrf_token(request):
    return JsonResponse({"csrfToken": get_token(request)})


class IsAdminUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "register"

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        logger.info("Зарегистрирован новый пользователь: %s", user.username)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"

    def post(self, request):
        username = request.data.get("username", "").strip()
        password = request.data.get("password", "")
        if not username or not password:
            return Response(
                {"detail": "Укажите логин и пароль"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(request, username=username, password=password)
        if user is None:
            logger.warning("Неудачная попытка входа для пользователя: %s", username)
            return Response(
                {"detail": "Неверный логин или пароль"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        login(request, user)
        logger.info("Пользователь %s вошел в систему", username)
        return Response(UserSerializer(user).data)


class LogoutView(APIView):
    def post(self, request):
        username = request.user.username
        logout(request)
        logger.info("Пользователь %s вышел из системы", username)
        return Response({"detail": "Успешный выход из системы"})


class CurrentUserView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class AdminUserListView(APIView):
    permission_classes = [IsAdminUserPermission]

    def get(self, request):
        users = User.objects.annotate(
            files_count_value=Count("files"),
            total_size_value=Sum("files__size"),
        ).order_by("-id")
        return Response(UserSerializer(users, many=True).data)


class AdminUserDetailView(APIView):
    permission_classes = [IsAdminUserPermission]

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND
            )
        if user.pk == request.user.pk and request.data.get("is_admin") is False:
            return Response(
                {"detail": "Нельзя снять права администратора у самого себя"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = AdminUserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(
            "Администратор %s изменил права пользователя %s",
            request.user.username,
            user.username,
        )
        return Response(UserSerializer(user).data)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND
            )
        if user.pk == request.user.pk:
            return Response(
                {"detail": "Нельзя удалить самого себя"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        username = user.username
        user.delete()
        logger.info(
            "Администратор %s удалил пользователя %s", request.user.username, username
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminUserFilesView(APIView):
    permission_classes = [IsAdminUserPermission]

    def get(self, request, user_id):
        if not User.objects.filter(pk=user_id).exists():
            return Response(
                {"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND
            )
        files = File.objects.filter(user_id=user_id).select_related("user")
        return Response(
            FileSerializer(files, many=True, context={"request": request}).data
        )
