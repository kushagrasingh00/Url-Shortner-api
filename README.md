# URL Shortener API

A RESTful URL shortener API built with **FastAPI** and **PostgreSQL**.
## Live API
https://url-shortner-api-k077.onrender.com

## API Documentation
Interactive Swagger UI:

https://url-shortner-api-k077.onrender.com/docs

## Features

* User registration and login
* JWT-based authentication
* Protected routes
* Create shortened URLs
* Automatic unique short-code generation
* Redirect shortened URLs to their original URLs
* View links belonging to the authenticated user
* Track link clicks
* Delete shortened links
* PostgreSQL database
* SQLAlchemy ORM
* Alembic database migrations
* API testing with Pytest

## Tech Stack

* **Python**
* **FastAPI**
* **PostgreSQL**
* **SQLAlchemy**
* **Pydantic**
* **JWT**
* **Alembic**
* **Pytest**

## API Documentation

FastAPI provides interactive API documentation through Swagger UI:

```text
/docs
```

When running locally:

```text
http://localhost:8000/docs
```

## Project Structure

```text
url-shortner-api/
│
├── app/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── links.py
│   │   └── users.py
│   │
│   ├── database.py
│   ├── database_models.py
│   ├── models.py
│   ├── Oauth2.py
│   ├── utils.py
│   └── main.py
│
├── alembic/
│   └── versions/
│
├── test/
│   ├── conftest.py
│   ├── test_link.py
│   └── test_user.py
│
├── alembic.ini
├── requirements.txt
└── .gitignore
```

## Running Locally

Clone the repository:

```bash
git clone https://github.com/kushagrasingh00/Url-Shortner-api.git
cd Url-Shortner-api
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add the required database and authentication configuration.

Run the API:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

## Database Migrations

This project uses Alembic for database migrations.

Create a migration:

```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:

```bash
alembic upgrade head
```

## Testing

Run the test suite with:

```bash
pytest
```

For verbose output:

```bash
pytest -v
```

## Authentication

Protected endpoints require a JWT access token.

The token is sent through the `Authorization` header:

```text
Authorization: Bearer <access_token>
```

## Example

A user submits an original URL:

```json
{
    "original_url": "https://google.com/"
}
```

The API generates a unique short code and returns a shortened URL.

The shortened URL can then be used to redirect the user to the original URL.

## Author

Kushagra Singh
