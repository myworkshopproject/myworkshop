import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import LogMixin, NoteMixin
from labbook.models import Session

# Doublon ????
class Task(LogMixin):
    class Meta(LogMixin.Meta):
        verbose_name = _("task")
        verbose_name_plural = _("tasks")


class Block(LogMixin, NoteMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    session = models.ForeignKey(
        Session,
        blank=True,
        null=True,
        # If Session is deleted, Block wont be deleted but set to null:
        on_delete=models.SET_NULL,
        related_name="blocks",
        related_query_name="block",
        verbose_name=_("session"),
    )

    task = models.OneToOneField(
        Task,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta(LogMixin.Meta, NoteMixin.Meta):
        verbose_name = _("block")
        verbose_name_plural = _("blocks")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title if self.title else f"Block object ({self.id})"


# class Assignee(LogMixin):
#     # user

#     # role [reviewer, etc.]

#     class Meta(LogMixin.Meta):
#         verbose_name = _("action")
#         verbose_name_plural = _("actions")
#         ordering = ["-created_at"]


# class Action(LogMixin):

#     # block

#     # assignee (optionnel)

#     # deadline (optionnel)

#     # priority [low, normal, high]

#     # severity [whishlist, minor, normal, important, critique]

#     ACTION_TODO = "todo"
#     ACTION_READY = "ready"
#     ACTION_IN_PROGRESS = "in-progress"
#     ACTION_READY_FOR_TEST = "ready-for-test"
#     ACTION_DOING = "doing"
#     ACTION_DONE = "done"

#     ACTION_CHOICES = [
#         (ACTION_TODO, _("To do")),
#         (ACTION_READY, _("Ready")),
#         (ACTION_IN_PROGRESS, _("In Progress")),
#         (ACTION_READY_FOR_TEST, _("Ready for Test")),
#         (ACTION_DOING, _("Doing")),
#         (ACTION_DONE, _("Done")),
#     ]

#     action = models.CharField(
#         max_length=32,
#         choices=ACTION_CHOICES,
#         default=ACTION_TODO,
#         verbose_name=_("action"),
#     )

#     class Meta(LogMixin.Meta):
#         verbose_name = _("action")
#         verbose_name_plural = _("actions")
#         ordering = ["-created_at"]
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["block", "assignee"], name="block_assignee_unique"
#             )
#         ]


# TASK_BLOCK_TYPES = [
#     Block.BLOCK_TYPE_TODO,
#     Block.BLOCK_TYPE_READY,
# ]


# class TaskManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(block_type__in=TASK_BLOCK_TYPES)


# class Task(Block):
#     objects = TaskManager()

#     class Meta:
#         proxy = True

#         verbose_name = _("task")
#         verbose_name_plural = _("tasks")

#     def __str__(self):
#         return self.title if self.title else f"Task object ({self.id})"

#     def save(self, *args, **kwargs):
#         self.block_type = TASK_BLOCK_TYPES[0]
#         super(Task, self).save(*args, **kwargs)
