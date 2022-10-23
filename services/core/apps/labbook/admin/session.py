from django.contrib import admin
from django.utils.translation import gettext as _

from core.admin import HasLogAdminInlineMixin
from labbook.admin import BlockAdminInline
from labbook.models import Session


class SessionAdmin(HasLogAdminInlineMixin, admin.ModelAdmin):
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
                        "project",
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
        "__str__",
        "project",
        "tags",
        "owner",
        "created_at",
        "changed_by",
        "changed_at",
    )

    search_fields = (
        "title",
        "tags",
        "content",
    )

    list_filter = (
        "project",
        "owner",
        "changed_by",
    )

    inlines = (BlockAdminInline,)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user

        obj.changed_by = request.user

        super().save_model(request, obj, form, change)


admin.site.register(Session, SessionAdmin)
