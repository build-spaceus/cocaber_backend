from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    """Custom API exception handler."""

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        # Using the description's of the HTTPStatus class as error message.
        message = "API error occurred."
        try:
            message = response.data.get("errors").get("message", message)
        except AttributeError:
            message = response.data.get("detail", message)
        try:
            error_code = response.data.get("errors", None).get(
                "error_code", 0000
            )
        except AttributeError:
            error_code = 0000

        response.data = {
            "status": response.data.get("status", "failure"),
            "errors": {"message": message, "error_code": error_code},
        }
    return response
