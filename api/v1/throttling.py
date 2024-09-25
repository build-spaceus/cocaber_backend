from django.core.cache import cache

from api.throttling import CacheKeyThrottling


class MobileNumberThrottle(CacheKeyThrottling):
    """
    Throttling class for mobile number throttle flow.
    only throttle uses with mobile number input in request
    """

    scope = "mobile"
    cache_time = 6 * 60 * 60  # 24 hours
    max_attempts = 5
    duration = 1 * 60 * 60  # 1 hour

    def get_cache_key(self, request, view):
        """
        Generates the cache key for the current request.
        """
        if "mobile_number" in self.request_data:
            mobile_number = self.request_data["mobile_number"]
            cache_key = f"throttle_{self.scope}_{mobile_number}"
        else:
            cache_key = None
        return cache_key

    def reset_throttle(self, mobile_number):
        cache_key = f"throttle_{self.scope}_{mobile_number}"
        cache.delete(cache_key)
