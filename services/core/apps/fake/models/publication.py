from django.db import models


class Publication(models.Model):

    text = models.TextField()

    class Meta:
        verbose_name = "Publication"
