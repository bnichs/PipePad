import logging
from pprint import pprint

from dynaconf import Dynaconf, LazySettings


logger = logging.getLogger(__name__)


DEFAULT_SETTING_FILES = [
    'settings.toml', '.secrets.toml',
    "/tmp/pytest-of-ben/pytest-131/test_override0/test_override"
]


# def get_settings(settings_files=None) -> LazySettings:
#     settings_files = settings_files or DEFAULT_SETTING_FILES
#     print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
#
#     settings = Dynaconf(
#         envvar_prefix="DYNACONF",
#         settings_files=settings_files,
#     )
#     return settings
#
#
# settings = get_settings()

logger.debug("loading with settings files %s", DEFAULT_SETTING_FILES)
print(DEFAULT_SETTING_FILES)

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=DEFAULT_SETTING_FILES,
)

pprint(settings.as_dict())


# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
