
import requests
from decouple import config

from integrations.exceptions import ApiIntegrationFailedException
from integrations.sinch.v1.constants import SEND_OTP_URL


class Sinch(object):
    def __init__(self):
        self.application_key = config("SINCH_APP_KEY", None)
        self.application_secret = config("SINCH_APP_SECRET", None)

    def send_otp(self, to_number):
        try:
            payload = {
                "identity": {"type": "number", "endpoint": to_number},
                "method": "sms",
            }

            # Production code

            # base64_string = self.application_secret
            # base64_string = base64_string.strip()
            # padding_needed = 4 - (len(base64_string) % 4)
            # if padding_needed and padding_needed != 4:
            #     base64_string += "=" * padding_needed
            # b64_encoded_application_secret = base64.b64decode(base64_string)
            # encoded_verification_request = json.dumps(payload).encode()
            # md5_verification_request = hashlib.md5(encoded_verification_request)
            # encoded_md5_to_base64_verification_request = base64.b64encode(md5_verification_request.digest())
            #
            # http_verb = "POST"
            # request_content_type = "application/json; charset=UTF-8"
            # time_now = datetime.now(timezone.utc).isoformat()
            # request_timestamp = "x-timestamp:" + time_now
            # request_uri_path = "/verification/v1/verifications"
            #
            # string_to_sign = (
            #         http_verb + "\n"
            #         + encoded_md5_to_base64_verification_request.decode() + "\n"
            #         + request_content_type + "\n"
            #         + request_timestamp + "\n"
            #         + request_uri_path
            # )
            #
            # authorization_signature = base64.b64encode(
            #     hmac.new(b64_encoded_application_secret, string_to_sign.encode(), hashlib.sha256).digest()
            # ).decode()
            #
            # headers = {
            #     "Content-Type": request_content_type,
            #     "Authorization": f"Application {self.application_key}:{authorization_signature}",
            #     "x-timestamp": time_now
            # }
            #
            # response = requests.post(
            #     SEND_OTP_URL,
            #     json=payload,
            #     headers=headers,
            # )

            # sandbox code

            headers = {"Content-Type": "application/json"}

            print(f"url: {SEND_OTP_URL}")
            print(f"payload: {payload}")
            print(f"headers: {headers}")
            print(f"auth: {self.application_key}, {self.application_secret}")

            response = requests.post(
                SEND_OTP_URL,
                json=payload,
                headers=headers,
                auth=(self.application_key, self.application_secret),
            )

            response_dict = response.json()
            print(response_dict)
            return response_dict
        except Exception as e:
            raise ApiIntegrationFailedException(e)
