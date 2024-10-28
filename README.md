[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/aO4VHhPy)
## Summative Project: University Residence Management API

### Project Description

This capstone project tasks students with designing and developing a RESTful API for managing a university's residence system. This system will enable students and administrators to interact with various aspects of residence life, such as:

* Room applications and assignments
* Maintenance requests and tracking
* Event announcements and management
* Resident communication and feedback
* Administrative oversight and reporting

The API will be built using Django REST Framework, leveraging advanced Python concepts and techniques.

### [Stage-1: Foundation and Planning ](https://github.com/ALU-BSE/Summative-Project-UniNest-API/blob/stage-1/README.md) 

1. **Project Setup:**
   * Create a new Django project in this repository (no redundant folders ) and install Django REST Framework.
   * Set up a virtual environment to manage project dependencies.
   * Create essential models for entities like `Resident`, `Room`, `Building`, and `MaintenanceRequest`.
   * Implement basic serializers and views for CRUD operations on these models.

2. **API Design and Documentation:**
   * Design a well-structured API, outlining endpoints and their functionalities.
   * Document the API comprehensively using Swagger or Redoc, including clear descriptions, request/response examples, and error handling guidelines.

3. **Asynchronous Programming Exploration:**
   * Research and identify potential API endpoints that could benefit from asynchronous execution (e.g., long-running tasks, background jobs).
   * Provide a written explanation of your findings, justifying your choices for potential asynchronous implementation.

**Submission:**

* A functional Django project with basic models, serializers, and views.
* A well-documented API specification.
* A written report explaining the potential use of asynchronous programming in the project.

### [Stage-2: Enhanced Functionality](https://github.com/ALU-BSE/Summative-Project-UniNest-API/blob/stage-2/README.md) 

1. **Authentication and Authorization:**

*  Implement basic authentication (username/password) using Django's built-in authentication system.
*  Implement session authentication for persistent logins.
*  Design and implement a basic authorization scheme to control access to API endpoints based on user roles (e.g., student, administrator).

2. **Pagination and Filtering:**

*  Implement pagination for endpoints that return large datasets (e.g., list of all residents).
*  Implement filtering capabilities to allow users to refine API requests based on specific criteria.

3. **Caching:**

*  Implement caching for frequently accessed read-only data to improve API performance.
*  Use Django's cache framework or a suitable third-party library.

**Submission:**

*  Updated Django project with implemented authentication, authorization, pagination, and caching features
*  Updated API documentation reflecting the new functionalities.

**Evaluation Criteria:**

*  Correctness and effectiveness of authentication and authorization mechanisms
*  Implementation of pagination and filtering
*  Appropriate use of caching
*  Updated and accurate API documentation

### [Stage-3: Advanced Features and Security](https://github.com/ALU-BSE/Summative-Project-UniNest-API/blob/stage-3/README.md) 

1. **Personal Data Handling:**
   * Review and ensure the API adheres to best practices for handling personal data.
   * Implement appropriate data encryption and anonymization where necessary.
   * Address common security concerns related to personal data.

2. **User Authentication Service:**
   * Improve the authentication system for the API to use JSON Web Tokens.
   * Enhance the authentication system using Django OAuth Toolkit or a similar library.
   * Explore integrating with external authentication providers (e.g., Google, Facebook).

3. **Error Handling and Logging:**
   * Implement comprehensive error handling for all API requests.
   * Provide clear and informative error messages to users.
   * Set up proper logging to capture errors and exceptions for debugging and monitoring.

**Submission:**

* Updated Django project with advanced features and security enhancements.
* Updated API documentation reflecting the new functionalities and security measures.

**Evaluation Criteria:**

* Proper handling of personal data and adherence to security best practices
* Implementation of a robust authentication service
* Effective error handling and logging mechanisms
* Updated and comprehensive API documentation

### [Stage-4: Testing and Refinement](https://github.com/ALU-BSE/Summative-Project-UniNest-API/blob/stage-4/README.md) 

1. **Unit Tests and Integration Tests:**
   * Write unit tests to verify the functionality of individual components (models, views, serializers).
   * Write integration tests to ensure seamless interaction between different parts of the API.
   * Use Python's `unittest` module or a similar testing framework.

2. **Deployment (Optional):**
   * If time and resources permit, deploy the API to a production-like environment.
   * Consider using a cloud platform (e.g., Heroku, AWS) or a local server setup.

3. **Documentation and Presentation:**
   * Finalize API documentation (Swagger) and ensure it's comprehensive and up-to-date
   * Prepare a presentation or demonstration to showcase the project, highlighting the challenges faced and the solutions implemented

**Submission:**

* Updated Django project with implemented tests
* Finalized and comprehensive API documentation
* Presentation or demonstration materials

**Evaluation Criteria:**

* Thoroughness and effectiveness of unit and integration tests
* Quality and completeness of final API documentation
* Clarity and effectiveness of project presentation or demonstration

