# URL Shortener

The system allows users to create short links, manage them from a dashboard, and redirect users through short URLs while tracking usage.

The project emphasizes backend architecture, authentication, containerization, and reverse-proxy routing.

---

## Architecture

Frontend- Built with React and served through Nginx.

Backend- Implemented with FastAPI providing authentication, URL management, and redirection.

Database- PostgreSQL stores users, shortened URLs, and metadata.
Redis is used for token blacklisting and caching.

Infrastructure- Docker Compose orchestrates the services and networking.
RabbitMQ as messaging queue, to send and receive data with analytics service.

---

## Features

Authentication

- User registration
- Login with JWT authentication
- Protected endpoints
- Current user session endpoint

URL Management

- Create shortened URLs
- List user URLs
- Store original URL and short code
- Optional metadata storage

Redirection

- `/r/{short_code}` endpoint
- HTTP redirect to the original URL
- Designed to work through Nginx reverse proxy

Dashboard

- View all created links
- Copy shortened URLs
- Manage personal URLs

Containerized Deployment

- Backend container (FastAPI + Uvicorn)
- Frontend container (Nginx + React)
- PostgreSQL container
- Docker networking between services

---

## Tech Stack

Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Uvicorn
- Pytest for testing

Frontend

- React
- Vite

Infrastructure

- Docker
- Docker Compose
- Nginx

---

## How URL Redirection Works

1. User creates a shortened URL.

Example

```
https://domain/r/bigG
```

2. Request flow

```
Browser
   ↓
NGINX
   ↓
proxy /r/ → backend:8000
   ↓
FastAPI redirect endpoint
   ↓
HTTP 307 redirect
   ↓
Target URL
```

3. Backend response

```
HTTP/1.1 307 Temporary Redirect
Location: https://google.com
```

---

## Running the Project

Requirements

- Docker
- Docker Compose

Clone repository

```
git clone <repo-url>
cd url-shortener
```

Make .env in the project root and fill it as shown in .env.example

Build and start containers

```
docker compose up --build
```

Services

Frontend

```
http://localhost
```

Backend API

```
http://localhost:8000
```

Short URL example

```
http://localhost/r/abc123
```

API Docs

```
http://localhost:8000/docs
```

---

## API Overview

Access full API docs at `http://localhost:8000/docs`

Authentication

Register

```
POST /auth/register
```

Login

```
POST /auth/login
```

Get current user

```
GET /auth/me
```

URLs

Create URL

```
POST /urls/
```

List URLs

```
GET /urls/
```

Redirect

```
GET /r/{short_code}
```

---

## Example Request

Create short URL

```
POST /urls/

{
  "original_url": "https://google.com"
}
```

Response

```
{
  "short_code": "bigG",
  "short_url": "http://localhost/r/bigG"
}
```

---

## Testing

Run backend tests

```
pytest -v
```

Test coverage includes

- authentication
- url creation
- redirect logic
- analytics endpoints

---

## Future Improvements

Analytics

Security

- OAuth login
- abuse detection

Features

- expiration time
- QR code generation

---

## Purpose of the Project

The project focuses on demonstrating:

- backend API design
- authentication workflows
- database operations
- reverse proxy routing
- containerized deployment
- production-like architecture for a simple service

It serves as a practical backend system design exercise and portfolio project.
