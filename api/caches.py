from core.cache.utils import Cache


class LoginRequest(Cache):
    fields = {
        "mobile_number": (str, ""),
        "request_id": (str, ""),
        "has_request": (bool, False),
    }
