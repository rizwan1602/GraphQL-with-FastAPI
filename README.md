## GraphQL with FastAPI.

This project demonstrates how to build a GraphQL API using FastAPI and SQLAlchemy.

## Getting Started

### Prerequisites

- Python 3.x installed on your machine

### Installation

1. Clone the repository:

    ```
    git clone https://github.com/rizwan1602/GraphQL-with-FastAPI.git
    ```

2. Navigate to the project directory:

    ```
    cd GraphQL-with-FastAPI
    ```

3. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

### Running the Application

To run the application, execute the following command:
uvicorn main --reload

The GraphQL API will be available at `http://localhost:8000/graphql`.

## GraphQL Schema

### UserType

Represents a user with `id`, `name`, and `age` fields.

### Query

Contains a resolver to retrieve a user by `name` and/or `age`.

### Mutation

Contains a resolver to add a new user with a `name` and `age`.

## Usage

### Retrieving Users

You can retrieve users by providing optional parameters `name` and `age` to the `user` query:

```graphql
query {
  user(name: "John", age: 30) {
    id
    name
    age
  }
}
