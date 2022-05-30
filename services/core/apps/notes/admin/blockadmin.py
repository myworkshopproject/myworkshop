from django.contrib import admin

from ordered_model.admin import OrderedTabularInline
from notes.models import BlockPublicationThroughModel, Block

class BlockPublicationTabularInline(OrderedTabularInline):
    model = BlockPublicationThroughModel
    fields = ('block', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    ordering = ('order',)
    extra = 1

admin.site.register(Block)