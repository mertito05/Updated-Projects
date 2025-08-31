# Blog Platform

A simple blogging platform built with Go that includes user authentication, post creation, and user management features.

## Features
- User registration and authentication
- Create, view blog posts
- User-specific post management
- Password hashing with bcrypt
- RESTful API with JSON responses
- CORS enabled for frontend integration
- Thread-safe implementation

## Requirements
- Go 1.21 or later
- Google UUID library
- Golang crypto library for bcrypt

## Installation
```bash
go mod download
```

## How to Run
```bash
go run main.go
```

The server will start on `localhost:8080`

## API Endpoints

### User Registration
```bash
POST /api/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

Response:
```json
{
  "id": "uuid-string",
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2023-12-07T10:30:00Z"
}
```

### User Login
```bash
POST /api/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepassword123"
}
```

Response:
```json
{
  "id": "uuid-string",
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2023-12-07T10:30:00Z"
}
```

### Create Post
```bash
POST /api/posts
Content-Type: application/json

{
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post...",
  "author_id": "user-uuid-string"
}
```

Response:
```json
{
  "id": "post-uuid-string",
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post...",
  "author_id": "user-uuid-string",
  "author": "john_doe",
  "created_at": "2023-12-07T10:30:00Z",
  "updated_at": "2023-12-07T10:30:00Z"
}
```

### Get All Posts
```bash
GET /api/posts
```

### Get Specific Post
```bash
GET /api/posts/{post_id}
```

### Get User's Posts
```bash
GET /api/users/{user_id}/posts
```

## Usage Example

1. Start the server
2. Register a user:
   ```bash
   curl -X POST http://localhost:8080/api/register \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'
   ```
3. Login:
   ```bash
   curl -X POST http://localhost:8080/api/login \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "password123"}'
   ```
4. Create a post:
   ```bash
   curl -X POST http://localhost:8080/api/posts \
     -H "Content-Type: application/json" \
     -d '{"title": "Test Post", "content": "This is a test post", "author_id": "user-uuid"}'
   ```
5. Get all posts:
   ```bash
   curl http://localhost:8080/api/posts
   ```

## Security Features
- Passwords are hashed using bcrypt
- No plain text password storage
- User authentication required for post creation
- CORS headers for secure cross-origin requests

## Dependencies
- github.com/google/uuid v1.4.0
- golang.org/x/crypto v0.16.0

## Notes
- Users and posts are stored in memory (not persistent across restarts)
- Thread-safe implementation for concurrent access
- No session management (stateless authentication)
- Simple demonstration of authentication principles
- Suitable for learning and small-scale applications
