from django.db import models

from core.models import ActiveModel, DatedModel
from customers.constants import GenderTypes


# Create your models here.
class Customer(DatedModel, ActiveModel):
    name = models.CharField(max_length=128)
    mobile_number = models.CharField(max_length=32)
    gender = models.CharField(max_length=32, choices=GenderTypes.choices)

    def __str__(self):
        return self.mobile_number

    def is_authenticated_customer(self):
        return True
