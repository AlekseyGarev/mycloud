import logging

from django.conf import settings
from django.http import FileResponse
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from storage.models import File
from storage.serializers import FileSerializer, PublicFileSerializer
from users.models import User

logger = logging.getLogger("storage")


def is_admin(user):
    return bool(
        user.is_authenticated
        and (getattr(user, "is_admin", False) or user.is_superuser)
    )


def get_accessible_file(pk, user):
    try:
        item = File.objects.select_related("user").get(pk=pk)
    except File.DoesNotExist:
        return None
    return item if item.user_id == user.id or is_admin(user) else None


class FileListUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        target_user_id = request.query_params.get("user_id")
        if target_user_id:
            if not is_admin(request.user):
                return Response(
                    {"detail": "Доступ запрещен"}, status=status.HTTP_403_FORBIDDEN
                )
            if not User.objects.filter(pk=target_user_id).exists():
                return Response(
                    {"detail": "Пользователь не найден"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            files = File.objects.filter(user_id=target_user_id)
        else:
            files = File.objects.filter(user=request.user)
        return Response(
            FileSerializer(
                files.select_related("user"), many=True, context={"request": request}
            ).data
        )

    def post(self, request):
        files = request.FILES.getlist("files") or request.FILES.getlist("file")
        if not files:
            return Response(
                {"detail": "Файлы не переданы"}, status=status.HTTP_400_BAD_REQUEST
            )
        if len(files) > settings.MAX_FILES_PER_UPLOAD:
            return Response(
                {
                    "detail": f"За один раз можно загрузить не более {settings.MAX_FILES_PER_UPLOAD} файлов."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        oversized = [f.name for f in files if f.size > settings.MAX_UPLOAD_FILE_SIZE]
        if oversized:
            return Response(
                {"detail": f"Превышен максимальный размер файла: {oversized[0]}"},
                status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            )

        target_user = request.user
        target_user_id = request.data.get("user_id")
        if target_user_id:
            if not is_admin(request.user):
                return Response(
                    {"detail": "Доступ запрещен"}, status=status.HTTP_403_FORBIDDEN
                )
            try:
                target_user = User.objects.get(pk=target_user_id)
            except User.DoesNotExist:
                return Response(
                    {"detail": "Пользователь не найден"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        comment = request.data.get("comment", "").strip()
        custom_name = request.data.get("original_name", "").strip()
        created = []
        for uploaded in files:
            original_name = (
                custom_name if len(files) == 1 and custom_name else uploaded.name
            )
            name_serializer = FileSerializer(
                data={"original_name": original_name, "comment": comment}
            )
            try:
                original_name = name_serializer.fields["original_name"].run_validation(
                    original_name
                )
            except Exception as exc:
                return Response(
                    {"original_name": [str(getattr(exc, "detail", exc))]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            item = File.objects.create(
                user=target_user,
                original_name=original_name,
                file=uploaded,
                size=uploaded.size,
                comment=comment,
            )
            created.append(item)
            logger.info(
                "Пользователь %s загрузил файл %s (ID %s) в хранилище %s",
                request.user.username,
                item.original_name,
                item.id,
                target_user.username,
            )

        data = FileSerializer(created, many=True, context={"request": request}).data
        return Response(
            data[0] if len(data) == 1 else data, status=status.HTTP_201_CREATED
        )


class FileDetailView(APIView):
    def patch(self, request, pk):
        item = get_accessible_file(pk, request.user)
        if item is None:
            return Response(
                {"detail": "Файл не найден или доступ запрещен"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = FileSerializer(
            item, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(
            "Файл ID %s обновлен пользователем %s", item.id, request.user.username
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        item = get_accessible_file(pk, request.user)
        if item is None:
            return Response(
                {"detail": "Файл не найден или доступ запрещен"},
                status=status.HTTP_404_NOT_FOUND,
            )
        original_name = item.original_name
        item.delete()
        logger.info(
            "Файл %s (ID %s) удален пользователем %s",
            original_name,
            pk,
            request.user.username,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class FileShareView(APIView):
    def post(self, request, pk):
        item = get_accessible_file(pk, request.user)
        if item is None:
            return Response(
                {"detail": "Файл не найден или доступ запрещен"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {
                "special_link": str(item.share_token),
                "public_url": request.build_absolute_uri(f"/share/{item.share_token}"),
            }
        )


class FileDownloadView(APIView):
    def get(self, request, pk):
        item = get_accessible_file(pk, request.user)
        if item is None:
            return Response(
                {"detail": "Файл не найден или доступ запрещен"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if not item.file or not item.file.storage.exists(item.file.name):
            logger.error("Физический файл отсутствует для записи ID %s", item.id)
            return Response(
                {"detail": "Файл отсутствует на сервере"},
                status=status.HTTP_404_NOT_FOUND,
            )
        item.last_downloaded_at = timezone.now()
        item.save(update_fields=["last_downloaded_at"])
        return FileResponse(
            item.file.open("rb"), as_attachment=True, filename=item.original_name
        )


class PublicFileInfoView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, share_token):
        try:
            item = File.objects.get(share_token=share_token)
        except File.DoesNotExist:
            return Response(
                {"detail": "Файл по данной ссылке не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(PublicFileSerializer(item).data)


class PublicFileDownloadView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "public_download"

    def get(self, request, share_token):
        try:
            item = File.objects.get(share_token=share_token)
        except File.DoesNotExist:
            return Response(
                {"detail": "Файл по данной ссылке не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if not item.file or not item.file.storage.exists(item.file.name):
            return Response(
                {"detail": "Файл отсутствует на сервере"},
                status=status.HTTP_404_NOT_FOUND,
            )
        item.last_downloaded_at = timezone.now()
        item.save(update_fields=["last_downloaded_at"])
        logger.info("Публичное скачивание файла ID %s", item.id)
        return FileResponse(
            item.file.open("rb"), as_attachment=True, filename=item.original_name
        )
