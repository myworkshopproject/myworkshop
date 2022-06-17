from django.db import models

from myapp.settings.auth import AUTH_USER_MODEL

class Block(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(AUTH_USER_MODEL, related_name='blocks', on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    data = models.JSONField()
    pos = models.IntegerField()