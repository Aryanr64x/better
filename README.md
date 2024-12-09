# Library Management System API

## Overview
This project is a Flask-based API for a Library Management System that supports:
- CRUD operations for books and members.
- Search functionality for books by title or author.
- Pagination for book results.
- Token-based authentication for secure operations.

---

## Features
1. **Authentication:** Generate tokens for secure operations.
2. **Books API:**
   - Add, update, delete, and fetch books.
   - Search by title or author.
   - Pagination support.
3. **Members API:** Add and fetch library members.

---

## Installation
1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>


## API Endpoints

### Books Endpoints

#### 1. List All Books
- **Method**: `GET /books`
- **Query Parameters**:
  - `search`: Search for books by title or author (e.g., `?search=Around`).
  - `page`: Specify the page number for paginated results (default: `1`).
- **Response**:
  ```json
  [
    {
      "id": 1,
      "title": "Around the World in Eighty Days",
      "author": "Jules Verne",
      "available": 1
    }
  ]



#### 2. Add a New Book
- **Method**: `POST /books`
- **Description**: Adds a new book to the library.
- **Request Body**:
  ```json
  {
    "title": "Book Title",
    "author": "Author Name",
    "available": 1
  }

#### 3. Get Details of a Single Book
- **Method**: `GET /books/<id>`
- **Description**: Retrieves details of a specific book by its ID.
- **URL Parameters**:
  - `id`: The ID of the book to fetch (e.g., `/books/1`).
- **Response**:
  ```json
  {
    "id": 1,
    "title": "Around the World in Eighty Days",
    "author": "Jules Verne",
    "available": 1
  }


#### 4. Update a Book
- **Method**: `PUT /books/<id>`
- **Description**: Updates the details of an existing book by its ID.
- **URL Parameters**:
  - `id`: The ID of the book to update (e.g., `/books/1`).
- **Request Body**:
  - The request body should contain the updated details of the book:
  ```json
  {
    "title": "Updated Title",
    "author": "Updated Author",
    "available": 0
  }

#### 5. Delete a Book
- **Method**: `DELETE /books/<id>`
- **Description**: Deletes a book from the library by its ID.
- **URL Parameters**:
  - `id`: The ID of the book to delete (e.g., `/books/1`).
- **Response**:
  ```json
  {
    "message": "Book deleted successfully"
  }


### Members Endpoints

#### 1. List All Members
- **Method**: `GET /members`
- **Description**: Retrieves a list of all members in the library.
- **Query Parameters**:
  - `page`: Specify the page number for paginated results (default: `1`).
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "John Doe"
    },
    {
      "id": 2,
      "name": "Jane Smith"
    }
  ]


#### 2. Add a New Member
- **Method**: `POST /members`
- **Description**: Adds a new member to the library system.
- **Request Body**:
  - The request body should contain the details of the member to be added:
  ```json
  {
    "name": "John Doe"
  }


  ### Authentication Endpoint

#### 1. Authenticate (Login)
- **Method**: `POST /auth/login`
- **Description**: Authenticates a user and provides a token for subsequent requests.
- **Request Body**:
  ```json
  {
    "username": "user_name",
    "password": "password"
  }


### Authorization Requirements

- **Authorization Required**: All routes except for the following require a valid JWT token in the `Authorization` header (as a Bearer token):
  - `POST /auth/login` (Authentication endpoint)
  - `GET /books?search=<search_term>` (Search for books)
  
- **For protected routes** (adding, updating, or deleting books, managing members, etc.), include a valid JWT token in the `Authorization` header:




## Design Choices

### 1. Flask Framework
- **Why Flask?**: Flask was chosen because it is a lightweight and flexible web framework that is simple to use for building RESTful APIs. It provides all the necessary tools to build and manage routes, handle HTTP methods, and manage middleware for authentication.
- **Simplicity**: Flask allows for quick development and testing with minimal boilerplate code, making it ideal for building a library management system that can be easily extended and maintained.

### 2. RESTful API Design
- **Why REST?**: The system is built following RESTful principles, as it is a well-known architectural style for designing networked applications. This allows clients to interact with the server through a set of simple HTTP methods (GET, POST, PUT, DELETE).
- **Resources**: In this case, resources like "books" and "members" are represented as entities, and CRUD operations (Create, Read, Update, Delete) are exposed as HTTP endpoints.

### 3. Token-Based Authentication (JWT)
- **Why JWT?**: JWT (JSON Web Token) was chosen for handling authentication because it is stateless and allows secure transmission of information between client and server. It is well-suited for modern web applications, where the server does not store session information but relies on tokens for user verification.
- **Authorization**: A middleware function checks for the presence of a valid JWT token in the request header for routes that require authentication. This ensures that only authorized users can access specific resources.

### 4. Pagination
- **Why Pagination?**: Pagination is implemented to improve the performance of the API when returning large datasets. Instead of loading all records in a single response, we limit the number of records returned per request and allow the client to navigate through multiple pages of results.
- **Page Numbering**: Clients can specify the page number and the number of results per page. The server returns only the relevant subset of data based on the requested page.

### 5. SQL Database (SQLite)
- **Why SQLite?**: SQLite was chosen as the database for this project because it is lightweight, serverless, and easy to set up. It is a good fit for small to medium-scale applications like this library management system.
- **Tables and Relationships**: 
  - **Books** table contains details about each book.
  - **Members** table stores user information. 
  - The system can be extended to include additional relationships, such as a many-to-many relationship between books and members (borrowed books).

### 6. Search Functionality
- **Why Search?**: Search functionality allows users to find books quickly by title or author. It improves the usability of the system, especially as the number of books grows.
- **Implementation**: The search feature looks for partial matches in both the `title` and `author` fields. This allows users to query books even if they don't know the full title or author name.

### 7. Error Handling
- **Why Error Handling?**: Proper error handling ensures that users receive meaningful feedback when something goes wrong (e.g., invalid input or missing data). It helps with debugging and provides a better user experience.
- **Implementation**: The API returns standard HTTP status codes along with error messages for different error scenarios like `400 Bad Request`, `404 Not Found`, and `401 Unauthorized`.

### 8. Data Validation
- **Why Data Validation?**: To ensure the integrity of the data, data validation is performed when adding or updating records. This prevents invalid data from being saved to the database, maintaining the system's reliability.
- **Implementation**: Simple validation checks are applied to ensure that required fields are present and correctly formatted (e.g., non-empty strings for book titles and member names).

### 9. Extensibility
- **Future Enhancements**: The design is modular, allowing easy integration of future features such as book reservations, due dates, overdue tracking, and advanced search filters.
