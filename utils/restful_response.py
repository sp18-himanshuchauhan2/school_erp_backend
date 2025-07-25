from dataclasses import dataclass
from rest_framework import status
from rest_framework.response import Response
from .data_constants import ResponseMessages
from .db_choices import ErrorMessageInfoLevels

@dataclass
class DisplayMessage:
    show_to_user: bool
    level: str
    message: str


def send_response(
        data: dict = {},
        show_to_user: bool = False,
        level: str = ErrorMessageInfoLevels.info.value,
        message: str = ResponseMessages.DATA_FETCH_SUCCESS,
        status_code: int = status.HTTP_200_OK,
        error_code: int = None
) -> Response:
    """
    This function creates a standard response structure for APIs that can be returned to the client.
    Arguments:
    data: A dictionary containing the data that needs to be returned in the response.
    show_to_user: A boolean value that specifies whether the message should be shown
        to the user or not. By default, it is set to False.
    level: The level of the message. It can take one of the following values from the
        ErrorMessageInfoLevels class: info, error, warn, or na. By default, it is set to
        ErrorMessageInfoLevels.info.
    message: A string that represents the message that needs to be returned in the response.
        By default, it is set to DATA_FETCH_SUCCESS.
    status_code: An HTTP status code that needs to be returned in the response.
        By default, it is set to status.HTTP_200_OK (Successful request).
    Returns:
    A response object that can be returned to the client.
    """
    display_message = DisplayMessage(
        show_to_user=show_to_user,
        level=level,
        message=message or ResponseMessages.DATA_FETCH_SUCCESS,
    )
    if level == ErrorMessageInfoLevels.error.value:
        error_data = data
        response = {
            "error": error_data,
            "data": None,
            "display_message": display_message.__dict__,
            "error_code": error_code,
        }
    else:
        response = {
            "error": None,
            "data": data,
            "display_message": display_message.__dict__,
            "error_code": error_code,
        }
    return Response(response, status=status_code)
