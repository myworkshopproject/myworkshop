from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from accounts.serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        return User.public_objects.all()

    serializer_class = UserSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    search_fields = [
        "username",
        "first_name",
        "last_name",
        "source",
        "metadata",
        "date_joined",
    ]

    ordering_fields = [
        "username",
        "first_name",
        "last_name",
        "date_joined",
    ]
