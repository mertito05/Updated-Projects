package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/google/uuid"
)

type FileInfo struct {
	ID          string    `json:"id"`
	Filename    string    `json:"filename"`
	OriginalName string   `json:"original_name"`
	Size        int64     `json:"size"`
	UploadedAt  time.Time `json:"uploaded_at"`
	ContentType string    `json:"content_type"`
	DownloadURL string    `json:"download_url"`
}

type FileServer struct {
	files []FileInfo
}

func NewFileServer() *FileServer {
	return &FileServer{
		files: make([]FileInfo, 0),
	}
}

func (fs *FileServer) UploadFile(filename, originalName string, size int64, contentType string) FileInfo {
	fileInfo := FileInfo{
		ID:          uuid.New().String(),
		Filename:    filename,
		OriginalName: originalName,
		Size:        size,
		UploadedAt:  time.Now(),
		ContentType: contentType,
		DownloadURL: fmt.Sprintf("/download/%s", filename),
	}

	fs.files = append(fs.files, fileInfo)
	return fileInfo
}

func (fs *FileServer) GetFiles() []FileInfo {
	return fs.files
}

func (fs *FileServer) GetFileByID(id string) (FileInfo, bool) {
	for _, file := range fs.files {
		if file.ID == id {
			return file, true
		}
	}
	return FileInfo{}, false
}

func (fs *FileServer) DeleteFile(id string) bool {
	for i, file := range fs.files {
		if file.ID == id {
			// Remove the file from disk
			os.Remove(filepath.Join("uploads", file.Filename))
			fs.files = append(fs.files[:i], fs.files[i+1:]...)
			return true
		}
	}
	return false
}

func (fs *FileServer) GetTotalSize() int64 {
	var total int64
	for _, file := range fs.files {
		total += file.Size
	}
	return total
}

func main() {
	// Create uploads directory if it doesn't exist
	if err := os.MkdirAll("uploads", 0755); err != nil {
		fmt.Println("Error creating uploads directory:", err)
		os.Exit(1)
	}

	server := NewFileServer()

	// Serve static files
	http.Handle("/", http.FileServer(http.Dir(".")))

	// API endpoints
	http.HandleFunc("/api/files", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}

		switch r.Method {
		case http.MethodGet:
			files := server.GetFiles()
			
			// Add server statistics
			response := map[string]interface{}{
				"files": files,
				"stats": map[string]interface{}{
					"total_files": len(files),
					"total_size":  server.GetTotalSize(),
					"server_time": time.Now().Format(time.RFC3339),
				},
			}
			
			w.Header().Set("Content-Type", "application/json")
			json.NewEncoder(w).Encode(response)

		case http.MethodPost:
			// Parse multipart form with 100MB max size
			if err := r.ParseMultipartForm(100 << 20); err != nil {
				http.Error(w, "File too large", http.StatusBadRequest)
				return
			}

			file, handler, err := r.FormFile("file")
			if err != nil {
				http.Error(w, "Error retrieving file", http.StatusBadRequest)
				return
			}
			defer file.Close()

			// Generate unique filename
			ext := filepath.Ext(handler.Filename)
			filename := uuid.New().String() + ext
			filepath := filepath.Join("uploads", filename)

			// Create the file
			dst, err := os.Create(filepath)
			if err != nil {
				http.Error(w, "Error creating file", http.StatusInternalServerError)
				return
			}
			defer dst.Close()

			// Copy the uploaded file
			if _, err := io.Copy(dst, file); err != nil {
				http.Error(w, "Error saving file", http.StatusInternalServerError)
				return
			}

			// Add file to server
			fileInfo := server.UploadFile(filename, handler.Filename, handler.Size, handler.Header.Get("Content-Type"))
			json.NewEncoder(w).Encode(fileInfo)

		default:
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	http.HandleFunc("/api/files/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}

		id := r.URL.Path[len("/api/files/"):]
		if id == "" {
			http.Error(w, "File ID required", http.StatusBadRequest)
			return
		}

		if r.Method == http.MethodDelete {
			if server.DeleteFile(id) {
				w.WriteHeader(http.StatusNoContent)
			} else {
				http.NotFound(w, r)
			}
		} else {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	// Download endpoint
	http.HandleFunc("/download/", func(w http.ResponseWriter, r *http.Request) {
		// Prevent directory traversal
		if strings.Contains(r.URL.Path, "..") {
			http.Error(w, "Invalid path", http.StatusBadRequest)
			return
		}

		filename := r.URL.Path[len("/download/"):]
		filepath := filepath.Join("uploads", filename)

		// Check if file exists
		if _, err := os.Stat(filepath); os.IsNotExist(err) {
			http.NotFound(w, r)
			return
		}

		// Set appropriate headers for download
		w.Header().Set("Content-Disposition", fmt.Sprintf("attachment; filename=%s", filename))
		http.ServeFile(w, r, filepath)
	})

	// Health check endpoint
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"status":    "healthy",
			"timestamp": time.Now().Format(time.RFC3339),
			"files":     len(server.GetFiles()),
			"total_size": server.GetTotalSize(),
		})
	})

	fmt.Println("File Server started on :8080")
	fmt.Println("Endpoints:")
	fmt.Println("  GET    /api/files     - List all files with statistics")
	fmt.Println("  POST   /api/files     - Upload a file")
	fmt.Println("  DELETE /api/files/:id - Delete a file")
	fmt.Println("  GET    /download/:file - Download a file")
	fmt.Println("  GET    /health        - Health check")
	
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Println("Error starting server:", err)
		os.Exit(1)
	}
}
