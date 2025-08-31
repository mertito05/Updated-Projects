# Go Projects Summary

This directory contains 5 complete Go projects covering various domains and use cases.

## Projects Created

### 1. Chat Application (`chat-app/`)
A real-time chat application using WebSocket connections for instant messaging.

**Features:**
- Real-time messaging with WebSockets
- Multiple client support
- Simple command-line interface
- Connection management

**Tech Stack:**
- Gorilla WebSocket library
- Concurrent connection handling

### 2. URL Shortener (`url-shortener/`)
A URL shortening service with RESTful API endpoints.

**Features:**
- Create short URLs from long URLs
- Redirect functionality
- Access statistics tracking
- Thread-safe implementation

**Tech Stack:**
- HTTP server with JSON API
- UUID generation for short URLs

### 3. Expense Tracker (`expense-tracker/`)
A web-based expense tracking application with REST API.

**Features:**
- Add, view, delete expenses
- Category-based expense tracking
- Total and category-wise calculations
- CORS-enabled for frontend integration

**Tech Stack:**
- RESTful API design
- JSON data handling
- Concurrent access safety

### 4. Image Gallery (`image-gallery/`)
A web application for uploading and managing images.

**Features:**
- File upload with validation
- Image metadata storage
- File serving capabilities
- 10MB file size limit

**Tech Stack:**
- Multipart form handling
- File system operations
- UUID-based filename generation

### 5. Blog Platform (`blog-platform/`)
A blogging platform with user authentication.

**Features:**
- User registration and login
- Post creation and management
- Password hashing with bcrypt
- User-specific content

**Tech Stack:**
- Bcrypt password hashing
- User authentication
- REST API endpoints

### 6. Task Scheduler (`task-scheduler/`)
A command-line task management application.

**Features:**
- Task creation with priorities and due dates
- Task completion tracking
- Overdue task identification
- Persistent JSON storage
- Interactive CLI interface

**Tech Stack:**
- JSON file persistence
- Command-line interface
- Date/time handling

## Common Dependencies
- `github.com/google/uuid v1.4.0` - For UUID generation
- `golang.org/x/crypto v0.16.0` - For bcrypt hashing (blog platform)

## Running the Projects

Each project can be run independently:

```bash
cd go-projects/project-name
go mod download
go run main.go
```

## Project Structure
Each project includes:
- `main.go` - Main application code
- `go.mod` - Go module definition
- `README.md` - Project documentation
- Additional files as needed (HTML templates, static files, etc.)

## Key Features Across Projects
- **Concurrency Safety**: All projects use proper synchronization
- **Error Handling**: Comprehensive error handling throughout
- **API Design**: RESTful principles where applicable
- **Documentation**: Complete README files with usage examples
- **Persistence**: File-based or in-memory data storage

## Next Steps
1. Install Go dependencies for each project
2. Run individual projects to test functionality
3. Create frontend interfaces for web applications
4. Extend features as needed for specific use cases
