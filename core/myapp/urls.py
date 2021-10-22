from django.contrib import admin
from django.urls import (
    include,
    path,
)
from rest_framework.routers import DefaultRouter

from accounts.viewsets import UserViewSet


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", include("accounts.urls")),
    path("", include("core.urls")),
]

router = DefaultRouter()

router.register(
    "users",
    UserViewSet,
    basename="users",
)

urlpatterns += [
    path("api/v1/", include((router.urls, "api"), namespace="api")),
    path(
        "api/v1/api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),
]
