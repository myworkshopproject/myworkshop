from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User

        fields = [
            "url",
            "title",
            "description",
            "tags",
            "username",
            "first_name",
            "last_name",
            "image",
            # "source",
            # "metadata",
            # "toc",
            # "html",
            "date_joined",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:users-detail"},
        }
