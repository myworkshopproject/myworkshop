from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from core.models import BaseModel, LogModelMixin, SlugModel

FLATPAGE_DEFAULT_TEMPLATE = ""


class FlatPage(LogModelMixin, MPTTModel, SlugModel, BaseModel):

    # CHOICES

    REGULAR = "R"
    FULL_WIDTH = "W"
    FULL_PAGE = "P"

    FLATPAGE_TEMPLATE_CHOICES = [
        (REGULAR, _("Regular")),
        (FULL_WIDTH, _("Full width")),
        (FULL_PAGE, _("Full page")),
    ]

    DRAFT = "DR"
    PUBLIC = "PU"
    MEMBERS_ONLY = "ME"
    TRASH = "TR"

    VISIBILITY_CHOICES = [
        (DRAFT, _("draft")),
        (PUBLIC, _("public")),
        (MEMBERS_ONLY, _("members only")),
        (TRASH, _("trash")),
    ]

    # DATABASE FIELDS

    ## BaseModel fields replaced

    owner = None  # no need to use this field in this model

    ## automatic fields

    # history = HistoricalRecords()  # done in translation.py

    ## mandatory fields

    template = models.CharField(
        max_length=2,
        choices=FLATPAGE_TEMPLATE_CHOICES,
        default=REGULAR,
        verbose_name=_("template"),
    )

    visibility = models.CharField(
        max_length=2,
        choices=VISIBILITY_CHOICES,
        default=DRAFT,
        verbose_name=_("visibility"),
    )

    ## optional fields

    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,  # deletion of the parent is not permitted without deleting the child first!
        related_name="children",
    )

    body = models.TextField(
        blank=True, verbose_name=_("body"), default=FLATPAGE_DEFAULT_TEMPLATE
    )  # [i18n]

    # MANAGERS

    # META CLASS
    class Meta(BaseModel.Meta):
        verbose_name = _("flatpage")
        verbose_name_plural = _("flatpages")

    # TO STRING METHOD

    # SAVE METHOD

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        return reverse("flatpages:page-detail", kwargs={"slug": self.slug})

    # OTHER METHODS
