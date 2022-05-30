from rest_framework import viewsets
from rest_framework import permissions

from notes.serializers import BlockSerializer
from notes.models.block import Block
from notes.permissions import IsOwnerOrReadOnly

class BlockViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)