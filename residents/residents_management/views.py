from django.http import JsonResponse
from django.db import transaction
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from requests import request
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle
from rest_framework.versioning import URLPathVersioning
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.conf import settings

from .models import Building, Room, Resident
from .serializers import BuildingSerializer, RoomSerializer, ResidentSerializer
from .swagger_docs import get_swagger
from .api_logging import APILogger, handle_exceptions
from .throttling import BurstRateThrottle, SustainedRateThrottle
from .validators import validate_related_fields, validate_bulk_operation
from .exceptions import InvalidTypeError, BulkOperationError


class CustomPagination(PageNumberPagination):
    page_size = 10  # Keeping original page size
    page_size_query_param = 'page_size'
    max_page_size = 100


class AllDataListCreateView(ListCreateAPIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id']
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]
    versioning_class = URLPathVersioning

    def get_queryset(self):
        entity_type = self.request.query_params.get('type', '').lower()
        if entity_type == 'building':
            return Building.objects.all()
        elif entity_type == 'room':
            return Room.objects.all()
        elif entity_type == 'resident':
            return Resident.objects.all()
        return Building.objects.none()

    def get_serializer_class(self):
        entity_type = self.request.query_params.get('type', '').lower()
        if entity_type == 'building':
            return BuildingSerializer
        elif entity_type == 'room':
            return RoomSerializer
        elif entity_type == 'resident':
            return ResidentSerializer
        return BuildingSerializer

    @method_decorator(cache_page(60 * 15))
    @get_swagger
    @handle_exceptions
    def get(self, request, *args, **kwargs):
        entity_type = request.query_params.get('type')
        user = request.user.username

        if not entity_type:
            cache_key = f'all_data_{request.query_params.urlencode()}'
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)

            with transaction.atomic():
                buildings = Building.objects.all()
                rooms = Room.objects.all()
                residents = Resident.objects.all()

                all_data = list(buildings) + list(rooms) + list(residents)
                page = self.paginate_queryset(all_data)

                if page is not None:
                    serialized_data = []
                    for item in page:
                        if isinstance(item, Building):
                            serialized_data.append(BuildingSerializer(item).data)
                        elif isinstance(item, Room):
                            serialized_data.append(RoomSerializer(item).data)
                        elif isinstance(item, Resident):
                            serialized_data.append(ResidentSerializer(item).data)
                    response = self.get_paginated_response(serialized_data)
                    cache.set(cache_key, response.data, 60 * 15)

                    APILogger.log_operation('GET_ALL', 'multiple', user, {
                        'total_items': len(serialized_data)
                    })
                    return response

                data = {
                    'buildings': BuildingSerializer(buildings, many=True).data,
                    'rooms': RoomSerializer(rooms, many=True).data,
                    'residents': ResidentSerializer(residents, many=True).data,
                }
                cache.set(cache_key, data, 60 * 15)

                APILogger.log_operation('GET_ALL', 'multiple', user, {
                    'counts': {
                        'buildings': len(buildings),
                        'rooms': len(rooms),
                        'residents': len(residents)
                    }
                })
                return Response(data)

        APILogger.log_operation('GET', entity_type, user)
        return super().list(request, *args, **kwargs)

    @handle_exceptions
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        entity_type = request.data.get('type')  # Get the type from the request data
        data = request.data.get('data')  # Get the actual data to be created
        user = request.user.username

        if not entity_type or not data:
            APILogger.log_error('ValidationError', 'Missing type or data', user)
            return Response({
                'error': 'Both type and data are required fields'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # If data is a single object, make it a list for uniform processing
            if isinstance(data, dict):
                data = [data]

            # Handle creation based on the type
            if entity_type.lower() == 'building':
                serializer = BuildingSerializer(data=data, many=True)
            elif entity_type.lower() == 'room':
                serializer = RoomSerializer(data=data, many=True)
            elif entity_type.lower() == 'resident':
                serializer = ResidentSerializer(data=data, many=True)
            else:
                APILogger.log_error('ValidationError', f'Invalid entity type: {entity_type}', user)
                return Response({
                    'error': 'Invalid type specified'
                }, status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                validate_related_fields(serializer.validated_data)
                serializer.save()
                cache.clear()  # Clear the cache to update the records

                APILogger.log_operation('CREATE', entity_type, user, {
                    'count': len(data),
                    'data': data
                })
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            APILogger.log_error('ValidationError', serializer.errors, user)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            APILogger.log_error('UnexpectedError', str(e), user)
            raise


class AllDataRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]
    versioning_class = URLPathVersioning

    def get_queryset(self):
        entity_type = (self.request.query_params.get('type') or 
                       self.request.data.get('type', '')).lower()
        if entity_type == 'building':
            return Building.objects.all()
        elif entity_type == 'room':
            return Room.objects.all()
        elif entity_type == 'resident':
            return Resident.objects.all()
        return Building.objects.none()

    def get_serializer_class(self):
        entity_type = (self.request.query_params.get('type') or 
                       self.request.data.get('type', '')).lower()
        if entity_type == 'building':
            return BuildingSerializer
        elif entity_type == 'room':
            return RoomSerializer
        elif entity_type == 'resident':
            return ResidentSerializer
        return BuildingSerializer

    @method_decorator(cache_page(60 * 15))
    @get_swagger
    @handle_exceptions
    def get(self, request, *args, **kwargs):
        entity_type = request.query_params.get('type')  # Get the entity type from request params
        pk = kwargs.get('pk')  # Get the primary key from URL kwargs

        if entity_type == 'building':
            try:
                building = Building.objects.get(pk=pk)
                serializer = BuildingSerializer(building)
                return Response(serializer.data)
            except Building.DoesNotExist:
                return Response({'error': 'Building not found'}, 
                                status=status.HTTP_404_NOT_FOUND)

        elif entity_type == 'room':
            try:
                room = Room.objects.get(pk=pk)
                serializer = RoomSerializer(room)
                return Response(serializer.data)
            except Room.DoesNotExist:
                return Response({'error': 'Room not found'}, 
                                status=status.HTTP_404_NOT_FOUND)

        elif entity_type == 'resident':
            try:
                resident = Resident.objects.get(pk=pk)
                serializer = ResidentSerializer(resident)
                return Response(serializer.data)
            except Resident.DoesNotExist:
                return Response({'error': 'Resident not found'}, 
                                status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'Invalid type specified'}, 
                        status=status.HTTP_400_BAD_REQUEST)

    @handle_exceptions
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        entity_type = request.data.get('type')  # Get the type from the request data
        data = request.data.get('data')  # Get the actual data to be updated
        pk = kwargs.get('pk')  # Get the primary key from URL kwargs

        if not entity_type or not data:
            return Response({'error': 'Both type and data are required fields'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        if entity_type == 'building':
            # If data is a list, we validate bulk update
            if isinstance(data, list):
                validate_bulk_operation(data, settings.MAX_BULK_SIZE)
                for entry in data:
                    try:
                        building = Building.objects.get(pk=entry['id'])  # Find building by ID
                        serializer = BuildingSerializer(building, data=entry, partial=True)  # Update fields
                        if serializer.is_valid(raise_exception=True):
                            serializer.save()
                    except (Building.DoesNotExist, KeyError):
                        return Response({'error': 'Building not found or invalid data'}, 
                                        status=status.HTTP_404_NOT_FOUND)
                return Response({'status': 'Bulk update successful'}, 
                                status=status.HTTP_200_OK)

            # If data is a single object, we handle it directly
            try:
                building = Building.objects.get(pk=pk)
                serializer = BuildingSerializer(building, data=data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except Building.DoesNotExist:
                return Response({'error': 'Building not found'}, 
                                status=status.HTTP_404_NOT_FOUND)

        elif entity_type == 'room':
            try:
                room = Room.objects.get(pk=pk)
                serializer = RoomSerializer(room, data=data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except Room.DoesNotExist:
                return Response({'error': 'Room not found'}, 
                                status=status.HTTP_404_NOT_FOUND)

        elif entity_type == 'resident':
            try:
                resident = Resident.objects.get(pk=pk)
                serializer = ResidentSerializer(resident, data=data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except Resident.DoesNotExist:
                return Response({'error': 'Resident not found'}, 
                                status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'Invalid type specified'}, 
                        status=status.HTTP_400_BAD_REQUEST)

    @handle_exceptions
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        entity_type = request.query_params.get('type')
        pk = kwargs.get('pk')

        if entity_type == 'building':
            try:
                building = Building.objects.get(pk=pk)
                building.delete()
                cache.clear()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Building.DoesNotExist:
                return Response({'error': 'Building not found'}, 
                                status=status.HTTP_404_NOT_FOUND)

        elif entity_type == 'room':
            try:
                room = Room.objects.get(pk=pk)
                room.delete()
                cache.clear()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Room.DoesNotExist:
                return Response({'error': 'Room not found'}, 
                                status=status.HTTP_404_NOT_FOUND)

        elif entity_type == 'resident':
            try:
                resident = Resident.objects.get(pk=pk)
                resident.delete()
                cache.clear()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Resident.DoesNotExist:
                return Response({'error': 'Resident not found'}, 
                                status=status.HTTP_404_NOT_FOUND)