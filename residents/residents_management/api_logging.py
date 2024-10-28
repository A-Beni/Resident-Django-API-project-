import logging
from functools import wraps
from typing import Any, Dict, Optional
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import (
    APIException,
    NotFound,
    ValidationError,
    PermissionDenied
)
from django.conf import settings


# Configure logger
logger = logging.getLogger(__name__)


class APILogger:
    """Centralized logging functionality for API operations"""
   
    @staticmethod
    def setup_logging():
        """Configure logging settings"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler('api.log'),
                logging.StreamHandler()
            ]
        )


    @staticmethod
    def log_operation(operation: str, entity_type: str, user: str, data: Any = None):
        """Log API operations with user context"""
        log_data = {
            'operation': operation,
            'entity_type': entity_type,
            'user': user,
            'data': data
        }
        logger.info(f"API Operation: {log_data}")


    @staticmethod
    def log_error(error_type: str, details: str, user: str = None):
        """Log error events"""
        log_data = {
            'error_type': error_type,
            'details': details,
            'user': user
        }
        logger.error(f"API Error: {log_data}")


    @staticmethod
    def log_security(event_type: str, user: str, details: str):
        """Log security-related events"""
        log_data = {
            'event_type': event_type,
            'user': user,
            'details': details
        }
        logger.warning(f"Security Event: {log_data}")


    @staticmethod
    def log_performance(operation: str, duration: float):
        """Log performance metrics"""
        logger.info(f"Performance: {operation} took {duration:.2f} seconds")


class RateLimitExceeded(APIException):
    status_code = 429
    default_detail = 'Rate limit exceeded. Please try again later.'
    default_code = 'rate_limit_exceeded'


def handle_exceptions(func):
    """Decorator for handling API exceptions"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            APILogger.log_error('Validation', str(e))
            return Response({
                'error': 'Validation error',
                'details': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            APILogger.log_error('NotFound', str(e))
            return Response({
                'error': 'Resource not found',
                'details': str(e)
            }, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            APILogger.log_error('PermissionDenied', str(e))
            return Response({
                'error': 'Permission denied',
                'details': str(e)
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            APILogger.log_error('Unexpected', str(e))
            return Response({
                'error': 'Internal server error',
                'details': str(e) if settings.DEBUG else 'An unexpected error occurred'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper