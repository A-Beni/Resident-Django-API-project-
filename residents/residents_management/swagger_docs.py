from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Shared parameters
type_parameter = openapi.Parameter(
    'type',
    openapi.IN_QUERY,
    description="Type of entity (building, room, resident)",
    type=openapi.TYPE_STRING,
    required=True
)

pk_parameter = openapi.Parameter(
    'pk',
    openapi.IN_PATH,
    description="Primary key of the entity",
    type=openapi.TYPE_INTEGER,
    required=True
)

# GET Method Swagger Documentation
get_swagger = swagger_auto_schema(
    operation_description="""Retrieve all data or filter by type with pagination, filtering, and search capabilities. 
    Results are cached for 15 minutes.

    Usage:
    - To get all buildings: GET /api/data/?type=building
    - To get all rooms: GET /api/data/?type=room
    - To get all residents: GET /api/data/?type=resident
    - To search: add &search=query to the URL
    - To paginate: add &page=1&page_size=10 to the URL
    - To order: add &ordering=field or &ordering=-field for descending order
    """,
    responses={
        200: openapi.Response(
            description="Successful Response",
            examples={
                "application/json": {
                    "count": 100,
                    "next": "http://api.example.org/api/data/?type=building&page=4",
                    "previous": "http://api.example.org/api/data/?type=building&page=2",
                    "results": [
                        {
                            "id": 1,
                            "name": "Oak Tower",
                            "address": "456 Oak Avenue"
                        },
                        {
                            "id": 2,
                            "number": "101",
                            "floor": 1,
                            "building": 1
                        },
                        {
                            "id": 3,
                            "name": "John Doe",
                            "room": 2
                        }
                    ]
                }
            }
        ),
        400: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    "error": "Invalid type specified or type parameter is missing"
                }
            }
        ),
    },
    manual_parameters=[
        type_parameter,
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Search query for name or address",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'page',
            openapi.IN_QUERY,
            description="Page number for pagination",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'page_size',
            openapi.IN_QUERY,
            description="Number of items per page (max 100)",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'ordering',
            openapi.IN_QUERY,
            description="Fields to order by (e.g., 'id' or '-name' for descending)",
            type=openapi.TYPE_STRING
        ),
    ],
    security=[{'Bearer': []}]
)

# POST Method Swagger Documentation
post_swagger = swagger_auto_schema(
    operation_description="""Create new data or bulk data. Requires authentication.

    Usage:
    POST /api/data/
    {
        "type": "building",
        "data": {
            "name": "New Building",
            "address": "123 New St"
        }
    }

    For bulk creation:
    POST /api/data/
    {
        "type": "building",
        "data": [
            {"name": "Building 1", "address": "Address 1"},
            {"name": "Building 2", "address": "Address 2"}
        ]
    }
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'type': openapi.Schema(type=openapi.TYPE_STRING, description="Type of entity (building, room, resident)"),
            'data': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Data for creating entity or array of entities for bulk creation"
            ),
        },
        required=['type', 'data']
    ),
    responses={
        201: openapi.Response(
            description="Created",
            examples={
                "application/json": {
                    "id": 2,
                    "name": "New Tower",
                    "address": "123 Elm Street"
                }
            }
        ),
        400: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    "error": "Invalid data"
                }
            }
        ),
    },
    security=[{'Bearer': []}]
)

# PUT Method Swagger Documentation
put_swagger = swagger_auto_schema(
    operation_description="""Update existing data based on entity type. Supports single or bulk update. Requires authentication.

    Usage for single update:
    PUT /api/data/1/
    {
        "type": "building",
        "data": {
            "name": "Updated Building",
            "address": "456 Update St"
        }
    }

    Usage for bulk update:
    PUT /api/data/
    {
        "type": "building",
        "data": [
            {"id": 1, "name": "Updated Building 1"},
            {"id": 2, "name": "Updated Building 2"}
        ]
    }
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'type': openapi.Schema(type=openapi.TYPE_STRING, description="Type of entity (building, room, resident)"),
            'data': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Data for updating entity or array of entities for bulk update"
            ),
        },
        required=['type', 'data']
    ),
    responses={
        200: openapi.Response(
            description="Successful Update",
            examples={
                "application/json": {
                    "id": 1,
                    "name": "Updated Tower",
                    "address": "456 Oak Avenue"
                }
            }
        ),
        400: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    "error": "Invalid data"
                }
            }
        ),
        404: openapi.Response(
            description="Not Found",
            examples={
                "application/json": {
                    "error": "Entity not found"
                }
            }
        ),
    },
    manual_parameters=[pk_parameter],
    security=[{'Bearer': []}]
)

# DELETE Method Swagger Documentation
delete_swagger = swagger_auto_schema(
    operation_description="""  
    Delete data based on entity type. Supports single or bulk delete. Requires authentication.

    Usage for single delete:
    DELETE /api/data/1/?type=building

    Usage for bulk delete (deletes all entities of the specified type):
    DELETE /api/data/?type=building
    """,
    responses={
        204: openapi.Response(
            description="No Content",
            examples={
                "application/json": {
                    "message": "Entity deleted successfully"
                }
            }
        ),
        404: openapi.Response(
            description="Not Found",
            examples={
                "application/json": {
                    "error": "Entity not found"
                }
            }
        ),
        400: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    "error": "Invalid type specified"
                }
            }
        ),
    },
    manual_parameters=[
        type_parameter,
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description="Primary key of the entity to delete. If not provided, all entities of the specified type will be deleted.",
            type=openapi.TYPE_INTEGER,
            required=True  # Set to True as it's a path parameter
        ),
    ],
    security=[{'Bearer': []}]
)

# Apply these decorators to your view methods
# Example view method
# @swagger_auto_schema(method='get', **get_swagger)
# @swagger_auto_schema(method='post', **post_swagger)
# @swagger_auto_schema(method='put', **put_swagger)
# @swagger_auto_schema(method='delete', **delete_swagger)
# def your_view_method(request, pk=None):
#     ...
