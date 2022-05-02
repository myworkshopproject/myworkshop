from django.urls import path

from fake.views import PublicationView

app_name = "fake"

urlpatterns = [
    path("", PublicationView.as_view(), name="publication-list"),
]
