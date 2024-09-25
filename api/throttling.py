import datetime
import json

from django.core.cache import cache
from rest_framework.throttling import BaseThrottle


class CacheKeyThrottling(BaseThrottle):
    """
    A custom throttle class to throttle unique values from request body.
    This class implements rate limiting by storing the number of requests
    made within a specific time period in cache and checking it before
    allowing a new request.

    The rate limit applies to one of two unique values in the
    request body:- email address, mobile number

    The cache key used to store the number of requests is generated based on
    the type of unique value present in the request body.
    """

    cache_key = None
    wait_remaining = None
    scope = None
    cache_time = 24 * 60 * 60  # 24 hours
    max_attempts = 5
    duration = 1 * 60 * 60  # 1 hour
    request_data = None

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

    def add_initial_cache_time(self):
        cache.set(
            f"initial_{self.cache_key}_time",
            datetime.datetime.now().timestamp(),
            self.cache_time,
        )

    def get_initial_time(self):
        # retrieve initial requested time from cache
        initial_request = cache.get(f"initial_{self.cache_key}_time")
        if initial_request is None:
            # set current datetime as initial requested time,
            self.add_initial_cache_time()
            # drop existing request count from cache
            cache.delete(self.cache_key)
            initial_request = cache.get(f"initial_{self.cache_key}_time")
        return initial_request

    def add_cache_time(self):
        cache.set(
            f"{self.cache_key}_time",
            datetime.datetime.now().timestamp(),
            self.cache_time,
        )

    def get_wait_remaining(self):
        initial_request = cache.get(f"initial_{self.cache_key}_time")
        if initial_request:
            return round(
                (datetime.datetime.now().timestamp() - initial_request)
            )

    def get_request_data(self, request):
        data = request.data
        if not data:
            try:
                data = json.loads(request.body)
            except Exception:
                data = dict()
        return data

    def allow_request(self, request, view):
        """
        Check if a request should be allowed based on rate limiting rules.
        The method checks the number of requests made by a client in a given
        time window. If the number of requests exceeds the allowed limit
        within the time window, the method returns False. and block the
        request from the client to the next wait time eg:- block the user for
        the next 1hr. Otherwise, it updates the number of requests made by
        the client and returns True.

        - param request: The incoming request to be checked.
        - param view: The view being executed.

        - return: Boolean indicating whether the request should be allowed
         (True) or not (False).
        """
        self.request_data = self.get_request_data(request)
        self.cache_key = self.get_cache_key(request, view)
        if self.cache_key:
            # retrieve initial requested datetime value if exist
            initial_request = self.get_initial_time()
            # current datetime as recent time
            recent_request = datetime.datetime.now().timestamp()
            # get current number of requests
            num_requests = cache.get(self.cache_key, 0)
            # get abs difference of init an recent request time
            request_gap = abs(float(initial_request) - float(recent_request))
            if (
                request_gap >= self.duration
                or num_requests >= self.max_attempts
            ):
                """
                If the requested time gap exceeds the allowed rate duration,
                the cache is cleared and the user is allowed to make their
                next request. Otherwise, it returns False and throttle the
                request with configured wait period.
                """
                if round(request_gap) >= self.duration:
                    # reset current sessions initial datetime
                    self.add_initial_cache_time()
                    cache.set(self.cache_key, 1, self.cache_time)
                else:
                    self.wait_remaining = self.get_wait_remaining()
                    return False
            else:
                cache.set(self.cache_key, num_requests + 1, self.cache_time)
                if num_requests + 1 >= self.max_attempts:
                    # add last request time for showing wait_remaining time
                    # only need to show last throttled cache time
                    self.add_cache_time()
        return True

    def wait(self):
        """
        Returns the recommended next request time in seconds.
        """
        available_in = self.cache_time - self.wait_remaining
        return available_in
