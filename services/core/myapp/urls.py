from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.viewsets import UserViewSet

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("polls/", include("polls.urls")),
    path("notes/", include("notes.urls"))
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("accounts.urls")),
    path("", include("core.urls")),
)

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


if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))

    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
