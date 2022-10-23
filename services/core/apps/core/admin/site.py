from django.contrib import admin
from django.contrib.sites.models import Site
from modeltranslation.admin import TranslationAdmin
from simple_history.admin import SimpleHistoryAdmin

from core.models import SiteCustomization


class SiteAdmin(SimpleHistoryAdmin):
    pass


admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)


class SiteCustomizationAdmin(TranslationAdmin, SimpleHistoryAdmin):
    pass


admin.site.register(SiteCustomization, SiteCustomizationAdmin)
