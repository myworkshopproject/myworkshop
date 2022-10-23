from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LabbookConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "labbook"
    verbose_name = _("Labbook")
