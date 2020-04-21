from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MaterializedPathsConfig(AppConfig):
    name = 'materialized_paths'
    verbose_name = _("Materialized paths")
