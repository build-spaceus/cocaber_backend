import logging

from rest_framework.response import Response

from api.caches import LoginRequest
from api.v1.auth.serializers import LoginSendOTPSerializer
from api.v1.exceptions import InternalException
from api.v1.throttling import MobileNumberThrottle
from api.v1.views import APIBaseView
from core.utils import generate_random_string_with_regex

logger = logging.getLogger("api")


class LoginSendOTPView(APIBaseView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = [MobileNumberThrottle]

    @staticmethod
    def get_request_token():
        request_token = generate_random_string_with_regex()
        while LoginRequest(request_token).has_cache_key():
            request_token = generate_random_string_with_regex()
        return request_token

    def send_otp(self, login_request):
        return "abc"

    def post(self, request, code):
        serializer = LoginSendOTPSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.context.get("customer", None)
            has_customer = customer is not None
            try:
                mobile_number = serializer.validated_data.get(
                    "mobile_number", None
                )
                request_token = self.get_request_token()
                login_request = LoginRequest(request_token)
                login_request.create_or_update(
                    mobile_number=mobile_number,
                    has_customer=has_customer,
                )
                request_id = self.send_otp(login_request, request_token)
                login_request.create_or_update(request_id=request_id)
                login_request.compose()
                response_data = {
                    "request_token": request_token,
                }
                return Response(response_data)
            except Exception as e:
                logger.error(f"Login send OTP failed with error: {e}")
                raise InternalException()
        else:
            self.handle_serializer_errors(serializer.errors)


class LoginVerifyOTPView(APIBaseView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = [SignUpRequestTokenThrottle]

    @staticmethod
    def get_tokens_for_customer(customer):
        refresh = RefreshToken.for_user(customer)
        return str(refresh.access_token), str(refresh)

    def post(self, request, code):
        serializer = LoginVerifyOTPSerializer(data=request.data)
        serializer.context["code"] = code
        request_token = serializer.initial_data.get("request_token", None)
        request_token_lock_name = REQUEST_TOKEN_LOCK.format(request_token)
        with wait_redis_lock(request_token_lock_name):
            if serializer.is_valid():
                try:
                    request_token = serializer.validated_data.get(
                        "request_token", None
                    )
                    login_request = LoginRequest(request_token)
                    login_request.decompose()
                    customer = Customer.objects.get(
                        region__code__iexact=code,
                        mobile_number=login_request.mobile_number,
                    )
                    MobileNumberThrottle().reset_throttle(
                        mobile_number=login_request.mobile_number
                    )
                    login_request.delete_key()
                    access, refresh = self.get_tokens_for_customer(customer)
                    response_data = {"access": access}
                    response = Response(response_data)
                    response.set_cookie(
                        key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
                        value=refresh,
                        httponly=True,
                        expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                        secure=settings.SIMPLE_JWT["REFRESH_COOKIE_SECURE"],
                        domain=settings.SIMPLE_JWT["COOKIE_DOMAIN"],
                    )
                    response.set_cookie(
                        key="access_token_expiry",
                        value="access_token_expiry",
                        expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                        secure=settings.SIMPLE_JWT["REFRESH_COOKIE_SECURE"],
                        httponly=False,
                        domain=settings.SIMPLE_JWT["COOKIE_DOMAIN"],
                    )
                    return response
                except Exception as e:
                    logger.error(
                        f"Error occurred while verifying login otp: {e}"
                    )
                    raise InternalException()
            else:
                self.handle_serializer_errors(serializer.errors)


class LoginTokenRefreshView(APIBaseView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def post(self, request, code):
        try:
            refresh_token_value = request.COOKIES.get("refresh_token")
            refresh_token = RefreshToken(refresh_token_value)
            refresh_token.verify()
            access_token = refresh_token.access_token
            customer_id = access_token.payload["user_id"]
            Customer.objects.get(id=customer_id, region__code__iexact=code)
            response_data = {"access": str(access_token)}
            response = Response(response_data)
            response.set_cookie(
                key="access_token_expiry",
                value="access_token_expiry",
                expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT["REFRESH_COOKIE_SECURE"],
                httponly=False,
                domain=settings.SIMPLE_JWT["COOKIE_DOMAIN"],
            )
            return response
        except Exception:
            raise UnauthorizedUserException()


class LogoutView(APIBaseView):
    def post(self, request, code):
        response_data = {"success_message": "User logged out successfully"}
        response = Response(response_data)
        response.delete_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
            domain=settings.SIMPLE_JWT["COOKIE_DOMAIN"],
        )
        response.delete_cookie(
            key="access_token_expiry",
            domain=settings.SIMPLE_JWT["COOKIE_DOMAIN"],
        )
        return response


class ProfileView(APIBaseView):
    def get(self, request, code):
        customer = request.user
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
