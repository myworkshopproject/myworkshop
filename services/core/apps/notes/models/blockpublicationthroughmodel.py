from ordered_model.models import OrderedModel

from django.db import models

from .block import Block
from .publication import Publication

class BlockPublicationThroughModel(OrderedModel):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    order_with_respect_to = 'publication'