import jwt
from django.conf import settings
from rest_framework import authentication

from api.v1.exceptions import UnauthorizedUserException
from customers.models import Customer


class CustomerAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != b"jwt":
            raise UnauthorizedUserException()

        if len(auth_header) != 2:
            raise UnauthorizedUserException("Invalid token header.")
        token = auth_header[1]
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise UnauthorizedUserException("Token expired.")
        except jwt.DecodeError:
            raise UnauthorizedUserException()

        user_id = payload.get("user_id", None)
        if not user_id:
            raise UnauthorizedUserException()
        try:
            customer = Customer.objects.get(pk=user_id)
        except Customer.DoesNotExist:
            raise UnauthorizedUserException()
        return customer, None
