from django.db import models

from myapp.settings.auth import AUTH_USER_MODEL

PARA = "paragraph"
HEAD = "header"
LIST = "list"
DELI = "delimiter"
IMAG = "image"

TYPES_CHOICES = (
    (PARA, "paragraph"),
    (HEAD, "header"),
    (LIST, "list"),
    (DELI, "delimiter"),
    (IMAG, "image"),
)


class Block(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(AUTH_USER_MODEL, related_name='blocks', on_delete=models.CASCADE)
    type = models.CharField(max_length=9, choices=TYPES_CHOICES, default="paragraph")
    data = models.JSONField()