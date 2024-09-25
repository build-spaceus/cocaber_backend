import logging

import requests
from decouple import config
from django.views.decorators.debug import sensitive_variables

from integrations.google_recaptcha.v2.constants import (
    GOOGLE_RECAPTCHA_VERIFY_ENDPOINT,
)

logger = logging.getLogger("integrations")


class GoogleReCaptcha(object):
    def __init__(self):
        self.secret = config("GOOGLE_RECAPTCHA_V2_SECRET", None)

    @sensitive_variables("secret")
    def is_valid_token(self, recaptcha_token):
        payload = {"secret": self.secret, "response": recaptcha_token}
        try:
            response = requests.post(
                GOOGLE_RECAPTCHA_VERIFY_ENDPOINT, data=payload
            )
            response.raise_for_status()
            return response.json().get("success", False)
        except Exception as e:
            logger.error(
                f"Error occurred during invoking google recaptcha "
                f"verify api, {e}"
            )
            return False
