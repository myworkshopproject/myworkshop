from django.db import models

from .block import Block

class Publication(models.Model):
    name = models.CharField(max_length=100)
    block = models.ManyToManyField(Block, through='BlockPublicationThroughModel')