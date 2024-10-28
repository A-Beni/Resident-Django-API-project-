from rest_framework.exceptions import ValidationError
from .exceptions import BulkOperationError

def validate_related_fields(data):
    if isinstance(data, list):
        for item in data:
            _validate_single_item(item)
    else:
        _validate_single_item(data)

def _validate_single_item(data):
    if 'room' in data and 'building' in data:
        if data['room'].building != data['building']:
            raise ValidationError("Room must belong to the specified building")
    
    if 'resident' in data and 'room' in data:
        if data['resident'].room != data['room']:
            raise ValidationError("Resident must belong to the specified room")

def validate_bulk_operation(data, max_size):
    if len(data) > max_size:
        raise BulkOperationError(f"Bulk operation exceeds maximum size of {max_size}")
    