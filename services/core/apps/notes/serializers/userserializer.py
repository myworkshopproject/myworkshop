from attr import fields
from myapp.settings.auth import AUTH_USER_MODEL

from rest_framework import serializers
from .blockserializer import BlockSerializer

class UserSerializer(serializers.ModelSerializer):
    blocks = BlockSerializer(many=True, read_only=True)

    class Meta:
        model = AUTH_USER_MODEL
        fields = ['url', 'id', 'username', 'blocks']