import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import LogMixin, NoteMixin
from labbook.models import Project


class Session(LogMixin, NoteMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    project = models.ForeignKey(
        Project,
        # Prevent deletion of Session:
        on_delete=models.PROTECT,
        related_name="sessions",
        related_query_name="session",
        verbose_name=_("project"),
    )

    class Meta(LogMixin.Meta, NoteMixin.Meta):
        verbose_name = _("session")
        verbose_name_plural = _("sessions")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title if self.title else f"Session object ({self.id})"
