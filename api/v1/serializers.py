from rest_framework import serializers

from api.v1.exceptions import UnauthorizedUserException
from integrations.google_recaptcha.v2.utils import GoogleReCaptcha


class BaseValidationSerializer(serializers.Serializer):
    def validate_recaptcha_response(self, recaptcha_response):
        if not GoogleReCaptcha().is_valid_token(recaptcha_response):
            raise UnauthorizedUserException()
        return recaptcha_response
