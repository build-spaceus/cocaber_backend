"""
Declare all client related common exceptions here
"""


class ApiIntegrationDoesNotExist(Exception):
    def __init__(self, message="API integration object does not exist."):
        self.message = message
        super().__init__(self.message)


class ApiIntegrationFailedException(Exception):
    def __init__(self, message="API integration failed."):
        self.message = message
        super().__init__(self.message)
