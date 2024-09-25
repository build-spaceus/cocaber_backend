from rest_framework import serializers

from api.v1.exceptions import FieldInvalidException
from api.v1.serializers import BaseValidationSerializer
from core.utils import is_valid_phone_number
from customers.models import Customer


class LoginSendOTPSerializer(BaseValidationSerializer):
    recaptcha_response = serializers.CharField()
    mobile_number = serializers.CharField(max_length=32)

    def validate_mobile_number(self, mobile_number):
        if not is_valid_phone_number(mobile_number):
            raise FieldInvalidException(entity="mobile_number")
        try:
            customer = Customer.objects.get(mobile_number=mobile_number)
        except Customer.DoesNotExist:
            customer = None
        self.context["customer"] = customer
        return mobile_number
