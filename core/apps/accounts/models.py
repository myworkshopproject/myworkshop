import os
import shutil
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image
from textwrap import shorten

from core.validators import UsernameValidator
from utils.markdown import md_convert


class OverwriteStorage(FileSystemStorage):
    """
    Update get_available_name to remove any previously stored file (if any)
    before returning the name.
    """

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def image_path(instance, filename):
    root, ext = os.path.splitext(filename)
    new_filename = instance.username + ext.lower()
    return os.path.join(instance.get_storage_relative_path(), new_filename)


SENTINEL_USER_USERNAME = "deleted"


def get_sentinel_user():
    return User.objects.get_or_create(username=SENTINEL_USER_USERNAME, is_active=False)[
        0
    ]


def get_worker_user(hostname):
    username = "worker_{}".format(hostname)
    return User.objects.get_or_create(username=username, is_active=False)[0]


class PublicUserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class User(AbstractUser):
    # history = HistoricalRecords()  # done in translation.py

    username_validator = UsernameValidator()

    username = models.CharField(
        _("username"),
        primary_key=True,
        max_length=20,
        unique=True,
        help_text=_("Required. 20 characters or fewer. Letters, digits and _ only."),
        validators=[username_validator],
        error_messages={"unique": _("A user with that username already exists.")},
    )

    first_name = models.CharField(
        _("first name"),
        max_length=150,
        blank=True,
    )

    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=True,
    )

    image = models.ImageField(
        blank=True,
        null=True,
        upload_to=image_path,
        storage=OverwriteStorage(),
        verbose_name=_("profile picture"),
    )

    source = models.TextField(
        blank=True,
        max_length=2048,
        verbose_name=_("biography"),
        help_text=_("A few words to describe yourself (You can use Markdown syntax)."),
    )

    metadata = models.JSONField(default=dict, blank=True)
    toc = models.JSONField(default=list, editable=False)
    html = models.TextField(blank=True, editable=False)

    # MANAGERS
    objects = BaseUserManager()
    public_objects = PublicUserManager()

    class Meta(AbstractUser.Meta):
        ordering = ["-date_joined"]

    def save(self, *args, **kwargs):
        if self.metadata is None:
            self.metadata = {}

        if self.toc is None:
            self.toc = {}

        self.source, title, self.html, self.metadata, self.toc = md_convert(self.source)

        super(User, self).save(*args, **kwargs)

        # Crop to square, if needed:
        if self.image:
            image = Image.open(self.image.path)
            width, height = image.size
            if width != height:
                min_length = min(image.size)
                image = image.crop(
                    (
                        (width - min_length) // 2,
                        (height - min_length) // 2,
                        (width + min_length) // 2,
                        (height + min_length) // 2,
                    )
                )
                image.save(self.image.path)

    def get_absolute_url(self):
        return reverse("accounts:profile")

    def get_public_url(self):
        return reverse("accounts:user-detail", kwargs={"pk": self.pk})

    def get_avatar_url(self):
        if self.image:
            return self.image.url
        try:
            return self.socialaccount_set.all()[0].get_avatar_url()
        except IndexError:
            return None

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name, self.last_name)
        else:
            return self.username

    @property
    def title(self):
        return _("{full_name} profile page").format(full_name=self.get_full_name())

    @property
    def description(self):
        if "description" in self.metadata:
            if self.metadata["description"][0]:
                return shorten(self.metadata["description"][0], width=255)

        return _("Profile of {full_name}.").format(full_name=self.get_full_name())

    @property
    def tags(self):
        if "tag" in self.metadata:
            if len(self.metadata["tag"]):
                return self.metadata["tag"]
        return None

    def get_storage_relative_path(self):
        return os.path.join("users", str(self.username))

    def get_storage_absolute_path(self):
        return os.path.join(settings.MEDIA_ROOT, self.get_storage_relative_path())


@receiver(post_delete, sender=User)
def storage_delete(sender, instance, **kwargs):
    """When deleting a User object, deletes all the files linked to this object."""

    shutil.rmtree(
        instance.get_storage_absolute_path(),
        ignore_errors=True,
        onerror=None,
    )
