from os.path import join

from decouple import config

# application log settings
# https://docs.djangoproject.com/en/4.2/topics/logging/

LOG_BASE_DIR = config("LOG_BASE_DIR", "")
LOGS_PREFIX = "app.out."

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        }
    },
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] %(levelname)s %(name)s [%("
            "pathname)s:%(lineno)d] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.FileHandler",  # NOSONAR
            "filename": join(LOG_BASE_DIR, f"{LOGS_PREFIX}console.log"),
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
        "logfile_cocaber": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": join(LOG_BASE_DIR, f"{LOGS_PREFIX}cocaber.log"),
        },
        "logfile_api": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": join(LOG_BASE_DIR, f"{LOGS_PREFIX}api.log"),
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.db.backends": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
        "django.request": {
            "handlers": ["mail_admins", "console"],
            "level": "WARNING",
            "propagate": True,
        },
        "cocaber": {
            "handlers": ["logfile_cocaber"],
            "level": "DEBUG",
        },
        "integrations": {
            "handlers": ["logfile_integrations"],
            "level": "DEBUG",
        },
        "api": {
            "handlers": ["logfile_api"],
            "level": "DEBUG",
        },
    },
}
