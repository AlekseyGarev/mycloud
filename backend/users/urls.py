from django.urls import path
from users.views import (
    AdminUserDetailView,
    AdminUserFilesView,
    AdminUserListView,
    CurrentUserView,
    LoginView,
    LogoutView,
    RegisterView,
    get_csrf_token,
)

urlpatterns = [
    path("auth/csrf/", get_csrf_token, name="csrf"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/me/", CurrentUserView.as_view(), name="me"),
    path("admin/users/", AdminUserListView.as_view(), name="admin-users"),
    path(
        "admin/users/<int:pk>/", AdminUserDetailView.as_view(), name="admin-user-detail"
    ),
    path(
        "admin/users/<int:user_id>/files/",
        AdminUserFilesView.as_view(),
        name="admin-user-files",
    ),
]
