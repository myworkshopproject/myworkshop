from django.contrib import admin
from django.utils.translation import gettext as _
from mptt.admin import DraggableMPTTAdmin

from labbook.models import Project


class ProjectAdmin(DraggableMPTTAdmin):
    fieldsets = (
        (
            _("info fields"),
            {
                "classes": ("collapse",),
                "fields": (
                    "id",
                    "owner",
                    "created_at",
                    "changed_by",
                    "changed_at",
                ),
            },
        ),
        (
            None,
            {
                "fields": (
                    (
                        "title",
                        "parent",
                    ),
                    "tags",
                    "content",
                ),
            },
        ),
    )

    readonly_fields = (
        "id",
        "owner",
        "created_at",
        "changed_by",
        "changed_at",
    )

    list_display = (
        "tree_actions",
        "indented_title",
        "tags",
        "owner",
        "created_at",
    )

    list_display_links = ("indented_title",)

    search_fields = (
        "title",
        "tags",
        "content",
    )

    list_filter = (
        "owner",
        "changed_by",
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user

        obj.changed_by = request.user

        super().save_model(request, obj, form, change)


admin.site.register(Project, ProjectAdmin)
