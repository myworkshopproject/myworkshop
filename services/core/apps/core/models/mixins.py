from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import get_sentinel_user

# MYAPP_DESCRIPTION_MAX_LENGTH = 2048
MYAPP_TAG_MAX_LENGTH = 64
MYAPP_TITLE_MAX_LENGTH = 256


class LogMixin(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # If the related user is deleted, sets the owner to the "deleted" user:
        on_delete=models.SET(get_sentinel_user),
        related_name="%(app_label)s_%(class)ss_as_owner",
        related_query_name="%(app_label)s_%(class)s_as_owner",
        verbose_name=_("owner"),
        help_text=_(
            "The owner of this very object. By default it's the creator of the object."
        ),
        limit_choices_to={"is_active": True},
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("creation date"),
        help_text=_("When was this object created?"),
    )

    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # If the related user is deleted, sets the editor to the "deleted" user:
        on_delete=models.SET(get_sentinel_user),
        related_name="%(app_label)s_%(class)ss_as_changed_by",
        related_query_name="%(app_label)s_%(class)s_as_changed_by",
        verbose_name=_("last editor"),
        help_text=_("Who last modified this object?"),
    )

    changed_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("last modification date"),
        help_text=_("When was this object last modified?"),
    )

    class Meta:
        abstract = True
        ordering = ["-changed_at"]


class NoteMixin(models.Model):
    title = models.CharField(
        blank=True,
        max_length=MYAPP_TITLE_MAX_LENGTH,
        verbose_name=_("title"),
    )

    # description = models.TextField(
    #     blank=True,
    #     max_length=MYAPP_DESCRIPTION_MAX_LENGTH,
    #     verbose_name=_("description"),
    #     help_text=_("Raw text (styling with Markdown is not supported)."),
    # )

    tags = ArrayField(
        models.CharField(
            max_length=MYAPP_TAG_MAX_LENGTH,
            blank=True,
        ),
        blank=True,
        default=list,
        help_text=_("Comma-separated list of tags."),
    )

    content = models.TextField(
        blank=True,
        verbose_name=_("content"),
        help_text=_("Styling with Markdown is supported."),
    )

    class Meta:
        abstract = True
        ordering = ["title"]

    def save(self, *args, **kwargs):
        if self.tags is None:
            self.tags = []
        super(NoteMixin, self).save(*args, **kwargs)
