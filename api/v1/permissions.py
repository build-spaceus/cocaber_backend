from rest_framework.permissions import BasePermission

from api.v1.exceptions import ForbiddenActionException


class IsCustomerAuthenticated(BasePermission):
    """
    Allows the request if the customer is authenticated.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated_customer:
            return True
        raise ForbiddenActionException()
