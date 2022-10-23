from django.contrib import admin
from django.utils.translation import gettext as _

from labbook.models import Block, Task


class BlockAdminInline(admin.StackedInline):
    model = Block
    extra = 0
    show_change_link = True

    fields = (
        "title",
        "tags",
        "content",
    )


class BlockAdmin(admin.ModelAdmin):
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
                        "task",
                        "title",
                        "session",
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
        "session",
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
        "session__project",
        "session",
        "owner",
        "changed_by",
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user

        obj.changed_by = request.user

        super().save_model(request, obj, form, change)


admin.site.register(Block, BlockAdmin)


class TaskAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user

        obj.changed_by = request.user

        super().save_model(request, obj, form, change)


admin.site.register(Task, TaskAdmin)
