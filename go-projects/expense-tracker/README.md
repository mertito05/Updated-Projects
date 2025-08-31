# Expense Tracker

A web-based expense tracking application built with Go that provides a RESTful API for managing personal expenses.

## Features
- Add, view, and delete expenses
- Track expenses by category
- Calculate total expenses and category-wise totals
- RESTful API with JSON responses
- CORS enabled for frontend integration
- Thread-safe implementation

## Requirements
- Go 1.21 or later
- Google UUID library

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

### Get All Expenses
```bash
GET /api/expenses
```

Response:
```json
[
  {
    "id": "uuid-string",
    "amount": 25.99,
    "category": "Food",
    "description": "Lunch",
    "date": "2023-12-07T10:30:00Z"
  }
]
```

### Add New Expense
```bash
POST /api/expenses
Content-Type: application/json

{
  "amount": 25.99,
  "category": "Food",
  "description": "Lunch"
}
```

Response:
```json
{
  "id": "uuid-string",
  "amount": 25.99,
  "category": "Food",
  "description": "Lunch",
  "date": "2023-12-07T10:30:00Z"
}
```

### Delete Expense
```bash
DELETE /api/expenses/{id}
```

### Get Statistics
```bash
GET /api/stats
```

Response:
```json
{
  "total": 125.99,
  "byCategory": {
    "Food": 75.99,
    "Transport": 50.00
  },
  "count": 3
}
```

## Usage Example

1. Start the server
2. Add an expense:
   ```bash
   curl -X POST http://localhost:8080/api/expenses \
     -H "Content-Type: application/json" \
     -d '{"amount": 25.99, "category": "Food", "description": "Lunch"}'
   ```
3. Get all expenses:
   ```bash
   curl http://localhost:8080/api/expenses
   ```
4. Get statistics:
   ```bash
   curl http://localhost:8080/api/stats
   ```

## Frontend Integration
The server serves static files from the current directory. You can create an `index.html` file with a frontend interface that uses the API endpoints.

## Dependencies
- github.com/google/uuid v1.4.0

## Notes
- Expenses are stored in memory (not persistent across restarts)
- Thread-safe implementation for concurrent access
- CORS headers are enabled for cross-origin requests
