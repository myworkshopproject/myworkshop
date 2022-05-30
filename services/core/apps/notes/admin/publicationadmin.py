from django.contrib import admin

from ordered_model.admin import OrderedInlineModelAdminMixin
from notes.models import Publication
from .blockadmin import BlockPublicationTabularInline

class PublicationAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    model = Publication
    list_display = ('name',)
    inlines = (BlockPublicationTabularInline,)

admin.site.register(Publication, PublicationAdmin)