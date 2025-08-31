# URL Shortener

A URL shortening service built with Go that provides RESTful API endpoints for creating short URLs and redirecting to original URLs.

## Features
- Create short URLs from long URLs
- Redirect short URLs to original destinations
- Track access statistics (visit counts)
- Thread-safe implementation with mutex locks
- RESTful API design
- JSON responses

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

### Create Short URL
```bash
POST /shorten
Content-Type: application/json

{
  "url": "https://example.com/very/long/url/path"
}
```

Response:
```json
{
  "short_url": "abc123def",
  "original_url": "https://example.com/very/long/url/path"
}
```

### Redirect to Original URL
```bash
GET /{short_url}
```
Redirects to the original URL (HTTP 302)

### Get Statistics
```bash
GET /stats/{short_url}
```

Response:
```json
{
  "original_url": "https://example.com/very/long/url/path",
  "short_url": "abc123def",
  "created_at": "2023-12-07T10:30:00Z",
  "access_count": 42
}
```

## Usage Example

1. Start the server
2. Create a short URL:
   ```bash
   curl -X POST http://localhost:8080/shorten \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com"}'
   ```
3. Use the short URL:
   ```bash
   curl -L http://localhost:8080/abc123def
   ```
4. Check statistics:
   ```bash
   curl http://localhost:8080/stats/abc123def
   ```

## Dependencies
- github.com/google/uuid v1.4.0

## Notes
- URLs are stored in memory (not persistent across restarts)
- Short URLs are 8-character UUID prefixes
- Thread-safe implementation for concurrent access
