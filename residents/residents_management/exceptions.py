from rest_framework.exceptions import APIException
from rest_framework import status

class InvalidTypeError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid entity type specified"

class BulkOperationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST