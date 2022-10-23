import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

# from model_utils.managers import InheritanceManager

from core.models import LogMixin, NoteMixin
from labbook.models import Session


class Note(LogMixin, NoteMixin):
    # objects = InheritanceManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    session = models.ForeignKey(
        Session,
        blank=True,
        null=True,
        # If Session is deleted, Note wont be deleted but set to null:
        on_delete=models.SET_NULL,
        related_name="notes",
        related_query_name="note",
        verbose_name=_("session"),
    )

    class Meta(LogMixin.Meta, NoteMixin.Meta):
        verbose_name = _("note")
        verbose_name_plural = _("notes")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title if self.title else f"Note object ({self.id})"


class Task(models.Model):
    models.OneToOneField(
        Note,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    # priority
    # severity (bug) [whishlist, minor, normal, important, critique]
    # action
    # deadline
    # assignees
    # reviewers

    class Meta:
        verbose_name = _("task")
        verbose_name_plural = _("tasks")
