from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FakeConfig(AppConfig):
    name = "fake"
    verbose_name = _("Fake app")
