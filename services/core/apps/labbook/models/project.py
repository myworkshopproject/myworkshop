import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from core.models import LogMixin, NoteMixin


class Project(MPTTModel, LogMixin, NoteMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    parent = TreeForeignKey(
        "self",
        # if parent is deleted, self will also be deleted:
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    class MPTTMeta:
        order_insertion_by = ["title"]

    class Meta(LogMixin.Meta, NoteMixin.Meta):
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def __str__(self):
        return self.title if self.title else f"Project object ({self.id})"
