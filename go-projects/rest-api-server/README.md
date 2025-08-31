# REST API Server

A simple REST API server built with Go that demonstrates CRUD operations for users and products.

## Features

- **User Management**: Create and retrieve users
- **Product Management**: Create and retrieve products
- **Health Check**: Server status endpoint
- **JSON API**: Clean RESTful JSON API design
- **In-Memory Storage**: Simple in-memory data storage
- **Concurrency Safe**: Thread-safe operations with mutex locks

## API Endpoints

### Health Check
- `GET /health` - Check server status

### Users
- `GET /api/users` - Get all users
- `POST /api/users/create` - Create a new user

### Products
- `GET /api/products` - Get all products
- `POST /api/products/create` - Create a new product
- `GET /api/products/{id}` - Get product by ID

## Request/Response Examples

### Create User
```bash
curl -X POST http://localhost:8080/api/users/create \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

Response:
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Get All Products
```bash
curl http://localhost:8080/api/products
```

Response:
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "stock": 10
  },
  {
    "id": 2,
    "name": "Smartphone",
    "description": "Latest smartphone model",
    "price": 699.99,
    "stock": 25
  }
]
```

## Getting Started

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd go-projects/rest-api-server
   ```

2. **Run the server**
   ```bash
   go run main.go
   ```

3. **Test the API**
   ```bash
   curl http://localhost:8080/health
   ```

## Project Structure

```
rest-api-server/
├── main.go          # Main application file
├── go.mod           # Go module definition
└── README.md        # This file
```

## Dependencies

- Go 1.21 or later
- Standard library only (no external dependencies)

## Development

The server uses in-memory storage for simplicity. For production use, you would want to:

1. Add database persistence (PostgreSQL, MySQL, etc.)
2. Add authentication and authorization
3. Add input validation
4. Add logging and monitoring
5. Add proper error handling
6. Add unit tests

## License

This project is for educational purposes as part of the 50 Projects collection.
