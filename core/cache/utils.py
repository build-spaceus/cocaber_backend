from django.core.cache import cache

from core.cache.exceptions import (
    CacheKeyDoesNotExist,
    InvalidDatatypeError,
    InvalidFieldError,
)


class Cache(object):
    fields = {
        "mobile_number": (str, ""),
        "retries": (int, 1),
    }
    expiry = 30 * 60  # 30 minutes

    def __init__(self, reference_id):
        self.reference_id = reference_id

    def is_valid(self, request_cache_type):
        try:
            self.decompose()
            cache_type = getattr(self, "cache_type")
            return cache_type == request_cache_type
        except (CacheKeyDoesNotExist, AttributeError):
            return False

    def has_cache_key(self):
        return cache.get(self.reference_id) is not None

    def get_default_value(self, attr):
        return self.fields[attr][1]

    def get_datatype(self, attr):
        return self.fields[attr][0]

    @staticmethod
    def bool_to_string(value):
        return "1" if value else "0"

    @staticmethod
    def string_to_bool(value):
        return True if int(value) else False

    def compose(self):
        attrs = list(self.fields.keys())
        data = []
        for attr in attrs:
            try:
                value = getattr(self, attr)
            except AttributeError:
                value = self.get_default_value(attr)
            if isinstance(value, bool):
                value = self.bool_to_string(value)
            else:
                value = str(value)
            data.append(value)
        cache_value = ":".join(data)
        cache.set(self.reference_id, cache_value, self.expiry)

    def decompose(self):
        try:
            cache_value = cache.get(self.reference_id)
            assert cache_value is not None
            data = cache_value.split(":")
            attrs = list(self.fields.keys())
            for i in range(len(attrs)):
                datatype = self.get_datatype(attrs[i])
                try:
                    if datatype == bool:
                        value = self.string_to_bool(data[i])
                    else:
                        value = datatype(data[i])
                    setattr(self, attrs[i], value)
                except (ValueError, IndexError):
                    default = self.get_default_value(attrs[i])
                    setattr(self, attrs[i], default)
        except AssertionError:
            raise CacheKeyDoesNotExist()

    def create_or_update(self, **kwargs):
        for kwarg in kwargs:
            datatype = self.get_datatype(kwarg)
            if kwarg not in self.fields:
                raise InvalidFieldError(kwarg)
            try:
                assert isinstance(kwargs[kwarg], datatype)
                setattr(self, kwarg, kwargs[kwarg])
            except AssertionError:
                raise InvalidDatatypeError(kwarg)

    def change_key(self, key):
        cache.delete(self.reference_id)
        self.reference_id = key
        self.compose()

    def delete_key(self):
        cache.delete(self.reference_id)
