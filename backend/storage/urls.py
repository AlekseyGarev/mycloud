from django.urls import path
from storage.views import (
    FileDetailView,
    FileDownloadView,
    FileListUploadView,
    FileShareView,
    PublicFileDownloadView,
    PublicFileInfoView,
)

urlpatterns = [
    path("files/", FileListUploadView.as_view(), name="file-list-upload"),
    path("files/<int:pk>/", FileDetailView.as_view(), name="file-detail"),
    path("files/<int:pk>/download/", FileDownloadView.as_view(), name="file-download"),
    path("files/<int:pk>/share/", FileShareView.as_view(), name="file-share"),
    path(
        "public/files/<uuid:share_token>/",
        PublicFileInfoView.as_view(),
        name="public-file-info",
    ),
    path(
        "public/files/<uuid:share_token>/download/",
        PublicFileDownloadView.as_view(),
        name="public-file-download",
    ),
]
