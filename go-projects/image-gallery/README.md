# Image Gallery

A web-based image gallery application built with Go that allows users to upload, view, and manage images.

## Features
- Upload images with file validation
- View uploaded images in a gallery
- Delete images
- RESTful API with JSON responses
- File storage with unique filenames
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

### Get All Images
```bash
GET /api/images
```

Response:
```json
[
  {
    "id": "uuid-string",
    "filename": "generated-filename.jpg",
    "original_name": "my-image.jpg",
    "size": 102400,
    "uploaded_at": "2023-12-07T10:30:00Z",
    "content_type": "image/jpeg"
  }
]
```

### Upload Image
```bash
POST /api/images
Content-Type: multipart/form-data

# Include file in form data with field name "image"
```

Response:
```json
{
  "id": "uuid-string",
  "filename": "generated-filename.jpg",
  "original_name": "my-image.jpg",
  "size": 102400,
  "uploaded_at": "2023-12-07T10:30:00Z",
  "content_type": "image/jpeg"
}
```

### Delete Image
```bash
DELETE /api/images/{id}
```

### Access Uploaded Images
```bash
GET /uploads/{filename}
```

## Usage Example

1. Start the server
2. Upload an image:
   ```bash
   curl -X POST http://localhost:8080/api/images \
     -F "image=@/path/to/your/image.jpg"
   ```
3. Get all images:
   ```bash
   curl http://localhost:8080/api/images
   ```
4. View an image:
   ```bash
   curl -o downloaded.jpg http://localhost:8080/uploads/generated-filename.jpg
   ```

## Frontend Integration
The server serves static files from the current directory. You can create an `index.html` file with a frontend interface that uses the API endpoints for uploading and displaying images.

## File Storage
- Images are stored in the `uploads/` directory
- Original filenames are preserved in metadata
- Generated filenames use UUIDs to prevent conflicts
- Maximum file size: 10MB

## Dependencies
- github.com/google/uuid v1.4.0

## Notes
- Images are stored on disk (persistent across restarts)
- Thread-safe implementation for concurrent access
- CORS headers are enabled for cross-origin requests
- File uploads are limited to 10MB maximum size
