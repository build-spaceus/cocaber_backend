from django.db import models
from django.utils.translation import gettext_lazy as _


class AuthTypes(models.TextChoices):
    SIGNATURE_AUTH = "signature", _("Signature")
    OAUTH_2 = "oauth_2", _("OAUTH 2.0")
    OPEN_ENDPOINTS = "open_api", _("Open Endpoints")
