from django.contrib import admin
from django.utils.translation import ugettext, ugettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from mptt.admin import DraggableMPTTAdmin
from simple_history.admin import SimpleHistoryAdmin
from core.admin import BaseAdminMixin, LogAdminMixin, SlugAdminMixin
from flatpages.models import FlatPage


class FlatPageAdmin(
    DraggableMPTTAdmin,
    LogAdminMixin,
    SlugAdminMixin,
    BaseAdminMixin,
    TranslationAdmin,
    SimpleHistoryAdmin,
):
    list_display = ("tree_actions", "indented_title", "slug")
    list_display_links = ("indented_title",)

    readonly_fields = []

    fieldsets = [
        (_("Mandatory"), {"fields": ("template",)}),
        (_("Optional"), {"fields": ("parent", "body")}),
    ]


admin.site.register(FlatPage, FlatPageAdmin)
