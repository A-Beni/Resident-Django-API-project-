 Report:                          Potential Use of Asynchronous Programming in the Residence Management Project

Overview
Asynchronous programming enables a system to manage several tasks at once, without having to wait for one to finish before beginning another. Asynchronous programming can improve responsiveness and performance in the context of the Residence Management Project, particularly when handling numerous network calls, database transactions, or other time-consuming operations. This research investigates how asynchronous programming might be used to different project components.


Asynchronous Programming's Advantages for the Project

1. Increased responsiveness and scalability
   Multiple users may be simultaneously providing or requesting data in a web application such as residence management. Asynchronous programming enables the server to handle several requests at once without causing the application as a whole to stall. For instance, asynchronous handling makes that the system can handle other requests while the data is being collected from the database for inhabitants, rooms, or buildings.


2. Effective Engagements with Databases
   Asynchronous calls help ensure that database searches don't impede other activities when interacting with a database. Asynchronous database queries, for example, can free up resources to handle more requests when the system is looking for available rooms or getting resident details. When the database grows larger and more queries need to be processed simultaneously, this becomes essential.


3. Non-blocking Input/Output Operations
   When an application needs to handle I/O-bound operations or communicate with external services, asynchronous programming is especially useful. Integrations with third-party systems (such rent payment gateways) may exist in the field of residence management. In order to allow the server to manage additional user operations while it waits for a response from the external service, asynchronous queries to these services are made.


4. Instantaneous Updates and Alerts
   Real-time functionality, such as informing residents about room availability, maintenance schedules, or rent dues, is another crucial use case for asynchronous programming. Sending emails or pushing messages in the background can be accomplished with asynchronous tasks, which guarantee that the user is not kept waiting.


5. Enhanced User Experience
   Any management system must provide a faster and more seamless user experience. For some front-end tasks, such as filling out forms or loading resident data, asynchronous queries are used to minimize needless delays for users. Additionally, without the interface stopping, this enables loading spinners or other visual cues to let users know that their request is being handled.



 Implementation Possibilities

1. Views and APIs that are asynchronous
   Asynchronous views can be developed in the Django REST Framework, which is used in the project, to manage requests. It is possible to configure asynchronous API endpoints to manage laborious operations like database queries or external API requests without causing the application to crash.

2. Multitasking Asynchronously
   Django can be used with a task queue system such as Celery for background work. Long-term tasks like sending notifications, creating reports, or processing payments benefit greatly from this. Celery frees up the primary application thread by enabling asynchronous task execution in the background.


3. Asynchronous ORM-Based Database Searches
   Database queries can now be executed with Django's support for asynchronous ORM queries, which doesn't impede the main thread. Performance can be increased when retrieving huge datasets, such as lists of rooms, buildings, and occupants, by using async database queries.

Obstacles and Things to Think About

1. The codebase's complexity
   Although asynchronous programming has several advantages, the codebase may get more complex as a result of it. Careful planning is necessary to ensure that code is managed appropriately and to comprehend how to efficiently handle asynchronous operations. Additionally, debugging asynchronous code can be more difficult.

2. Compatibility with Databases
   Not every database has equal support for asynchronous operations. Django's asynchronous ORM, for instance, is still in its infancy and might not be perfectly optimized for every database backend. It's critical to confirm that the database system for the project can efficiently handle asynchronous queries.

3. Managing Race and Concurrency Situations
   In asynchronous programming, concurrency must be handled carefully. When numerous asynchronous operations attempt to access shared resources, like updating room availability or processing payments, race situations may arise. Data inconsistencies must be prevented by putting in place appropriate synchronization methods.


In summary

The Residence Management Project's scalability, productivity, and user interface can all be significantly enhanced via asynchronous programming. Task queues, non-blocking I/O, and asynchronous views will all help the system effectively manage many concurrent requests. Even though implementing asynchronous programming presents certain difficulties in terms of complexity and making sure concurrency is handled correctly, the advantages far exceed these worries, especially for real-time jobs and external service interaction.




API Documentation for AllDataView


Overview
This API provides CRUD functionality for managing Buildings, Rooms, and Residents. It allows retrieving all data or filtering by entity type (building, room, resident), and supports the creation, updating, and deletion of these entities. The API is built using the Django Rest Framework (DRF) and is documented using drf_yasg to enable Swagger-based API documentation.

Available Endpoints:
1. GET /all-data/: Retrieve Data
This endpoint allows retrieving all data from the database or filtering data by entity type (building, room, resident) and an optional primary key (pk).

Query Parameters:
type: Type of entity to filter by (building, room, resident).
pk: (Optional) Primary key to retrieve a specific entity.
Example URLs:
Retrieve all entities:
sql
Copy code
GET http://127.0.0.1:8000/all-data/
Retrieve all buildings:
bash
Copy code
GET http://127.0.0.1:8000/all-data/?type=building
Retrieve a specific room by pk:
bash
Copy code
GET http://127.0.0.1:8000/all-data/?type=room&pk=1
Response Codes:
200 OK: Successful data retrieval.
400 Bad Request: Invalid type specified.
404 Not Found: The entity with the specified pk is not found.
2. POST /all-data/: Create a New Entity
This endpoint allows for the creation of a new Building, Room, or Resident.

Request Body:
type: The type of entity to create (building, room, resident).
Additional entity-specific fields such as:
Building: name, address.
Room: building, number.
Resident: room, name.
Example URL:
arduino
Copy code
POST http://127.0.0.1:8000/all-data/
Response Codes:
201 Created: The entity has been successfully created.
400 Bad Request: Invalid data provided.
3. PUT /all-data/{pk}/: Update an Existing Entity
This endpoint allows updating an existing Building, Room, or Resident.

Path Parameter:
pk: Primary key of the entity to be updated.
Request Body:
type: The type of entity (building, room, resident).
Fields to be updated such as:
Building: name, address.
Room: building, number.
Resident: room, name.
Example URL:
arduino
Copy code
PUT http://127.0.0.1:8000/all-data/1/
Response Codes:
200 OK: Successful update.
400 Bad Request: Invalid data provided.
404 Not Found: Entity with the specified pk not found.
4. DELETE /all-data/{pk}/: Delete an Entity
This endpoint allows deleting an existing Building, Room, or Resident by its primary key (pk).

Path Parameter:
pk: Primary key of the entity to be deleted.
Query Parameter:
type: The type of entity to delete (building, room, resident).
Example URLs:
Delete a specific building:
bash
Copy code
DELETE http://127.0.0.1:8000/all-data/1/?type=building
Delete a specific room:
bash
Copy code
DELETE http://127.0.0.1:8000/all-data/2/?type=room
Response Codes:
204 No Content: Entity deleted successfully.
404 Not Found: Entity with the specified pk not found.
400 Bad Request: Invalid type specified.
How to Use This API with Postman
1. Setting Up Postman:
Open Postman and create a new request.
For each operation (GET, POST, PUT, DELETE), select the appropriate HTTP method from the dropdown.
2. GET Request in Postman:
URL: http://127.0.0.1:8000/all-data/
Add optional query parameters (type, pk) by clicking on "Params" and entering the key-value pairs.
Click Send to execute the request.
3. POST Request in Postman:
URL: http://127.0.0.1:8000/all-data/
Select Body, then choose raw and set the format to JSON.
In the body, specify the type and the entity fields.
Click Send to execute the request.
4. PUT Request in Postman:
URL: http://127.0.0.1:8000/all-data/{pk}/
Select Body, then choose raw and set the format to JSON.
Specify the type and the fields to update in the body.
Click Send to execute the request.
5. DELETE Request in Postman:
URL: http://127.0.0.1:8000/all-data/{pk}/
Add the type parameter in the Params section.
Click Send to execute the request.
6. Swagger UI:
For easier interaction, Swagger UI can be accessed (if enabled) at http://127.0.0.1:8000/swagger/, where you can view and test all API endpoints.
Error Responses:
Common error responses for the API are:

400 Bad Request: Invalid request data.
404 Not Found: Entity not found.
204 No Content: Successful deletion, no response body.



