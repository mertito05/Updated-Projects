# File Server

A robust file server application built with Go that provides RESTful API endpoints for file upload, download, and management with advanced features.

## Features
- File upload with 100MB size limit
- File download with proper content disposition
- RESTful API for file management
- File metadata storage and retrieval
- Server statistics and health monitoring
- CORS enabled for frontend integration
- Secure file handling with UUID-based filenames

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

### Get All Files with Statistics
```bash
GET /api/files
```

Response:
```json
{
  "files": [
    {
      "id": "uuid-string",
      "filename": "generated-filename.txt",
      "original_name": "my-file.txt",
      "size": 1024,
      "uploaded_at": "2023-12-07T10:30:00Z",
      "content_type": "text/plain",
      "download_url": "/download/generated-filename.txt"
    }
  ],
  "stats": {
    "total_files": 1,
    "total_size": 1024,
    "server_time": "2023-12-07T10:30:00Z"
  }
}
```

### Upload File
```bash
POST /api/files
Content-Type: multipart/form-data

# Include file in form data with field name "file"
```

Response:
```json
{
  "id": "uuid-string",
  "filename": "generated-filename.txt",
  "original_name": "my-file.txt",
  "size": 1024,
  "uploaded_at": "2023-12-07T10:30:00Z",
  "content_type": "text/plain",
  "download_url": "/download/generated-filename.txt"
}
```

### Delete File
```bash
DELETE /api/files/{id}
```

### Download File
```bash
GET /download/{filename}
```
Downloads the file with proper content disposition headers.

### Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2023-12-07T10:30:00Z",
  "files": 1,
  "total_size": 1024
}
```

## Usage Example

1. Start the server
2. Upload a file:
   ```bash
   curl -X POST http://localhost:8080/api/files \
     -F "file=@/path/to/your/file.txt"
   ```
3. List all files:
   ```bash
   curl http://localhost:8080/api/files
   ```
4. Download a file:
   ```bash
   curl -o downloaded.txt http://localhost:8080/download/generated-filename.txt
   ```
5. Check server health:
   ```bash
   curl http://localhost:8080/health
   ```

## File Storage
- Files are stored in the `uploads/` directory
- Original filenames are preserved in metadata
- Generated filenames use UUIDs to prevent conflicts
- Maximum file size: 100MB

## Security Features
- UUID-based filenames prevent directory traversal
- Content disposition headers for secure downloads
- CORS headers for cross-origin requests
- File size validation

## Dependencies
- github.com/google/uuid v1.4.0

## Notes
- Files are stored on disk (persistent across restarts)
- Server maintains file metadata in memory
- Suitable for file sharing and management applications
- Includes comprehensive error handling
