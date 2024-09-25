from django.db import models

from core.models import CreatedModel, DatedModel
from integrations.constants import AuthTypes


class ApiIntegration(DatedModel, CreatedModel):
    client_name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    auth_type = models.CharField(
        max_length=255,
        choices=AuthTypes.choices,
        default=AuthTypes.OPEN_ENDPOINTS,
    )
    auth_credentials = models.JSONField(blank=True, null=True)
    base_url = models.URLField(max_length=255)

    def __str__(self):
        return self.client_name
