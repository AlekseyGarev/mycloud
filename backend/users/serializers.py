import re

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, trim_whitespace=False
    )
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(required=True, allow_blank=False, max_length=255)

    class Meta:
        model = User
        fields = ("id", "username", "full_name", "email", "password")

    def validate_username(self, value):
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]{3,19}", value):
            raise serializers.ValidationError(
                "Логин должен начинаться с латинской буквы, содержать только латинские буквы и цифры и иметь длину 4–20 символов."
            )
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким логином уже существует."
            )
        return value

    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует."
            )
        return value

    def validate_password(self, value):
        if (
            len(value) < 6
            or not re.search(r"[A-Z]", value)
            or not re.search(r"\d", value)
            or not re.search(r"[^A-Za-z0-9]", value)
        ):
            raise serializers.ValidationError(
                "Пароль должен содержать минимум 6 символов, хотя бы одну заглавную букву, одну цифру и один специальный символ."
            )
        try:
            validate_password(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(list(exc.messages)) from exc
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    files_count = serializers.SerializerMethodField()
    total_size = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "full_name",
            "email",
            "is_admin",
            "is_superuser",
            "storage_path",
            "files_count",
            "total_size",
        )
        read_only_fields = fields

    def get_files_count(self, obj):
        annotated = getattr(obj, "files_count_value", None)
        return annotated if annotated is not None else obj.files.count()

    def get_total_size(self, obj):
        annotated = getattr(obj, "total_size_value", None)
        if annotated is not None:
            return annotated or 0
        return sum(obj.files.values_list("size", flat=True))


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("is_admin",)
