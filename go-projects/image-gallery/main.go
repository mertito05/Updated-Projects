package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"

	"github.com/google/uuid"
)

type Image struct {
	ID          string    `json:"id"`
	Filename    string    `json:"filename"`
	OriginalName string   `json:"original_name"`
	Size        int64     `json:"size"`
	UploadedAt  time.Time `json:"uploaded_at"`
	ContentType string    `json:"content_type"`
}

type ImageGallery struct {
	images []Image
	mu     sync.RWMutex
}

func NewImageGallery() *ImageGallery {
	return &ImageGallery{
		images: make([]Image, 0),
	}
}

func (ig *ImageGallery) AddImage(filename, originalName string, size int64, contentType string) Image {
	ig.mu.Lock()
	defer ig.mu.Unlock()

	image := Image{
		ID:          uuid.New().String(),
		Filename:    filename,
		OriginalName: originalName,
		Size:        size,
		UploadedAt:  time.Now(),
		ContentType: contentType,
	}

	ig.images = append(ig.images, image)
	return image
}

func (ig *ImageGallery) GetImages() []Image {
	ig.mu.RLock()
	defer ig.mu.RUnlock()

	return ig.images
}

func (ig *ImageGallery) GetImageByID(id string) (Image, bool) {
	ig.mu.RLock()
	defer ig.mu.RUnlock()

	for _, image := range ig.images {
		if image.ID == id {
			return image, true
		}
	}
	return Image{}, false
}

func (ig *ImageGallery) DeleteImage(id string) bool {
	ig.mu.Lock()
	defer ig.mu.Unlock()

	for i, image := range ig.images {
		if image.ID == id {
			// Remove the image file
			os.Remove(filepath.Join("uploads", image.Filename))
			ig.images = append(ig.images[:i], ig.images[i+1:]...)
			return true
		}
	}
	return false
}

func main() {
	// Create uploads directory if it doesn't exist
	if err := os.MkdirAll("uploads", 0755); err != nil {
		fmt.Println("Error creating uploads directory:", err)
		os.Exit(1)
	}

	gallery := NewImageGallery()

	// Serve static files
	http.Handle("/", http.FileServer(http.Dir(".")))

	// API endpoints
	http.HandleFunc("/api/images", func(w http.ResponseWriter, r *http.Request) {
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
			images := gallery.GetImages()
			json.NewEncoder(w).Encode(images)

		case http.MethodPost:
			// Parse multipart form
			if err := r.ParseMultipartForm(10 << 20); err != nil { // 10 MB max
				http.Error(w, "File too large", http.StatusBadRequest)
				return
			}

			file, handler, err := r.FormFile("image")
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

			// Copy the uploaded file to the destination file
			if _, err := io.Copy(dst, file); err != nil {
				http.Error(w, "Error saving file", http.StatusInternalServerError)
				return
			}

			// Add image to gallery
			image := gallery.AddImage(filename, handler.Filename, handler.Size, handler.Header.Get("Content-Type"))
			json.NewEncoder(w).Encode(image)

		default:
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	http.HandleFunc("/api/images/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}

		id := r.URL.Path[len("/api/images/"):]
		if id == "" {
			http.Error(w, "Image ID required", http.StatusBadRequest)
			return
		}

		if r.Method == http.MethodDelete {
			if gallery.DeleteImage(id) {
				w.WriteHeader(http.StatusNoContent)
			} else {
				http.NotFound(w, r)
			}
		} else {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	// Serve uploaded images
	http.HandleFunc("/uploads/", func(w http.ResponseWriter, r *http.Request) {
		// Prevent directory traversal
		if strings.Contains(r.URL.Path, "..") {
			http.Error(w, "Invalid path", http.StatusBadRequest)
			return
		}

		http.ServeFile(w, r, r.URL.Path[1:])
	})

	fmt.Println("Image Gallery server started on :8080")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Println("Error starting server:", err)
		os.Exit(1)
	}
}
