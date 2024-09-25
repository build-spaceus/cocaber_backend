from django.contrib import admin

from core.admin import SuperUserPermissionOnlyAdmin
from integrations.models import ApiIntegration


class ApiIntegrationAdmin(SuperUserPermissionOnlyAdmin):
    model = ApiIntegration
    list_display = (
        "client_name",
        "code",
        "created_by",
        "date_created",
    )


admin.site.register(ApiIntegration, ApiIntegrationAdmin)
