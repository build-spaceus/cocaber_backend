"""
Declare all cache related common exceptions here
"""


class CacheKeyDoesNotExist(Exception):
    def __init__(self, message="Cache key does not exist."):
        self.message = message
        super().__init__(self.message)


class InvalidFieldError(Exception):
    def __init__(self, field_name=""):
        if field_name:
            self.message = f"{field_name} is not a valid option."
        else:
            self.message = "Invalid field."
        super().__init__(self.message)


class InvalidDatatypeError(Exception):
    def __init__(self, field_name=""):
        if field_name:
            self.message = f"{field_name} value is invalid."
        else:
            self.message = "Invalid value."
        super().__init__(self.message)
