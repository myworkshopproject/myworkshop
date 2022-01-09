import os
import shutil
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


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
    new_filename = slugify(instance.site.name) + ext.lower()
    return os.path.join(instance.get_storage_relative_path(), new_filename)


class SiteCustomization(models.Model):
    # history = HistoricalRecords()  # done in translation.py

    site = models.OneToOneField(
        Site,
        # if Site is deleted, SiteCustomization will also be deleted:
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_("site"),
    )

    is_open_for_signup = models.BooleanField(
        default=True, verbose_name=_("is open for signup")
    )

    tagline = models.CharField(  # [i18n]
        blank=True,
        max_length=255,
        verbose_name=_("tagline"),
        help_text=_("A few words to describe this very website."),
    )

    description = models.TextField(  # [i18n]
        blank=True,
        max_length=2048,
        verbose_name=_("description"),
        help_text=_("A short text to describe this very website."),
    )

    image = models.ImageField(
        blank=True,
        null=True,
        upload_to=image_path,
        storage=OverwriteStorage(),
        verbose_name=_("featured image"),
    )

    fontawesome_site_icon = models.CharField(
        max_length=255,
        verbose_name=_("fontawesome site icon"),
        help_text=_(
            "Get icon name from <a href='https://fontawesome.com/'>Font Awesome</a>."
        ),
        default="fas fa-tools",
    )

    class Meta:
        verbose_name = _("site customization")
        verbose_name_plural = _("site customizations")
        ordering = ["site"]

    def __str__(self):
        return self.site.name if self.site.name else str(_("unknown"))

    def save(self, *args, **kwargs):
        super(SiteCustomization, self).save(*args, **kwargs)

        # Clear cached content
        Site.objects.clear_cache()

    def get_storage_relative_path(self):
        return os.path.join("sites", str(self.site.id))

    def get_storage_absolute_path(self):
        return os.path.join(settings.MEDIA_ROOT, self.get_storage_relative_path())


@receiver(post_delete, sender=SiteCustomization)
def storage_delete(sender, instance, **kwargs):
    """
    When deleting a SiteCustomization object, deletes all the files linked to this
    object.
    """
    shutil.rmtree(
        instance.get_storage_absolute_path(),
        ignore_errors=True,
        onerror=None,
    )
