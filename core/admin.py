from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    """
    Base admin to save created_by, modified_by
    """

    readonly_fields = (
        "created_by",
        "modified_by",
        "date_created",
        "date_modified",
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if obj.pk:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class ReadOnlyModelAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class SuperUserPermissionOnlyAdmin(BaseAdmin):
    @staticmethod
    def has_permission(request):
        if request.user.is_superuser:
            return True
        return False

    def has_view_or_change_permission(self, request, obj=None):
        return self.has_permission(request)

    def has_add_permission(self, request):
        return self.has_permission(request)
