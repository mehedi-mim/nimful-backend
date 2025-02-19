# Nimful Backend

Nimful is a web application that provides a platform for users to interact with various features.
The application is built using FastAPI as the web framework and SQLAlchemy as the ORM library.
The project structure is organized into the following directories:

- `alembic`: Contains Alembic migration scripts for managing database schema changes.
- `backend`: Contains the backend codebase including routers, services, and configurations.
- `db`: Contains database related modules and configurations.
- `models`: Contains SQLAlchemy models for database tables.
- `routers`: Contains API routers for handling different endpoints.
- `services`: Contains service modules for business logic implementation.
- `utils`: Contains utility modules for helper functions.
- `requirements.txt`: Lists all project dependencies.
- `docker-compose.yml`: Defines the Docker Compose configuration for setting up the project environment.

## Project Overview

The Nimful backend is designed to provide a RESTful API for the frontend to interact with.
The API endpoints are defined using FastAPI and are organized into different routers.
Each router is responsible for handling a specific set of endpoints.
The service modules are responsible for implementing the business logic for each endpoint.
The models are used to define the database schema and are used by the services to interact with the database.

## Setup Instructions

To set up the project, follow these steps:

1. Clone the repository.
2. Install project dependencies by running `pip install -r requirements.txt`.
3. Set up the database by running Alembic migrations: `alembic upgrade head`.
4. Start the backend server using `uvicorn backend.main:app --reload`.

## Environment Variables

Make sure to set the following environment variables:

- `DATABASE_URL`: URL for the database connection.
- `SECRET_KEY`: Secret key used for JWT token generation.
- `PASETO_LOCAL_KEY`: Secret key used for PASETO token generation.
- `EMAIL_USER`: Email address used for sending emails.
- `EMAIL_PASSWORD`: Password for the email address.
- `CONTACT_ME_EMAIL`: Email address used for contact form submissions.

## API Endpoints

The API endpoints are defined in the `routers` directory.
Each endpoint is documented using FastAPI's built-in documentation features.

Some examples of endpoints include:

- `/create-domain-visit`: POST endpoint to create a domain visit.
- `/generate-new-seed`: POST endpoint to generate a new seed.
- `/login`: POST endpoint to log in a user.
- `/logout`: POST endpoint to log out a user.
- `/signup`: POST endpoint to sign up a new user.
- `/verify`: POST endpoint to verify a user's email address.

## Technology Stack

The project uses the following technologies:

- FastAPI: Web framework for building the API.
- SQLAlchemy: ORM library for interacting with the database.
- Alembic: Migration library for managing database schema changes.
- Pydantic: Library for defining data models and validating data.
- PASETO: Library for generating and verifying tokens.
- Uvicorn: ASGI server for running the FastAPI application.
- Nginx: Reverse proxy server for handling incoming requests.
## Development

To start the development server, run `python main.py`.
This will start the server in debug mode and reload the application whenever changes are made to the code.

## Deployment

To deploy the application, run `docker-compose up -d`.
This will start the application in detached mode and create Docker containers for the application and Nginx.

To stop the application, run `docker-compose down`.
This will stop the application and remove the Docker containers.

To update the application, run `docker-compose pull` and then `docker-compose up -d`.
This will pull the latest version of the application and start it in detached mode.

## Nginx Configuration

The application uses Nginx as a reverse proxy. 
Ensure that the `nginx.conf` file is correctly configured for your environment. 
Here is a basic example of what the `nginx.conf` might contain:

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://backend:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Make sure to replace `example.com` with your domain name and adjust any other configurations as necessary.