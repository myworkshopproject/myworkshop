from myapp.settings.auth import AUTH_USER_MODEL

from rest_framework import viewsets

from serializers import UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = AUTH_USER_MODEL.objects.all()
    serializer_class = UserSerializer