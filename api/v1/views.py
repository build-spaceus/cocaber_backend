from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from api.handlers import api_exception_handler
from api.renderers import APIRenderer
from api.v1.authentication import CustomerAuthentication
from api.v1.exceptions import (
    FieldBlankException,
    FieldInvalidException,
    FieldNullException,
    FieldRequiredException,
)
from api.v1.permissions import IsCustomerAuthenticated


class APIBaseView(APIView):
    permission_classes = [IsCustomerAuthenticated]
    authentication_classes = [CustomerAuthentication]
    renderer_classes = [APIRenderer]
    parser_classes = [JSONParser]

    def get_exception_handler(self):
        return api_exception_handler

    @staticmethod
    def handle_serializer_errors(errors):
        for key, value in errors.items():
            error = value[0]
            if error.code == "required":
                raise FieldRequiredException(entity=key)
            elif error.code == "blank":
                raise FieldBlankException(entity=key)
            elif error.code == "null":
                raise FieldNullException(entity=key)
            else:
                raise FieldInvalidException(entity=key)
