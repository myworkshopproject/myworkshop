from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = "core"
    verbose_name = _("Core app")

    def ready(self):
        import core.signals.handlers  # noqa F401
