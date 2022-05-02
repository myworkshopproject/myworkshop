from django.urls import path

from accounts import views

app_name = "accounts"

urlpatterns = [
    path("users/", views.UserListView.as_view(), name="user-list"),
    path("users/<str:pk>/", views.UserDetailView.as_view(), name="user-detail"),
    path("accounts/profile/", views.ProfileView.as_view(), name="profile"),
]
