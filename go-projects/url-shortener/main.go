package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"sync"
	"time"

	"github.com/google/uuid"
)

type URLMapping struct {
	OriginalURL string    `json:"original_url"`
	ShortURL    string    `json:"short_url"`
	CreatedAt   time.Time `json:"created_at"`
	AccessCount int       `json:"access_count"`
}

type URLShortener struct {
	mappings map[string]URLMapping
	mu       sync.RWMutex
}

func NewURLShortener() *URLShortener {
	return &URLShortener{
		mappings: make(map[string]URLMapping),
	}
}

func (us *URLShortener) CreateShortURL(originalURL string) string {
	us.mu.Lock()
	defer us.mu.Unlock()

	// Generate a unique short ID
	shortID := uuid.New().String()[:8]

	mapping := URLMapping{
		OriginalURL: originalURL,
		ShortURL:    shortID,
		CreatedAt:   time.Now(),
		AccessCount: 0,
	}

	us.mappings[shortID] = mapping
	return shortID
}

func (us *URLShortener) GetOriginalURL(shortURL string) (string, bool) {
	us.mu.RLock()
	defer us.mu.RUnlock()

	mapping, exists := us.mappings[shortURL]
	if !exists {
		return "", false
	}

	// Update access count (this requires a write lock, so we'll do it separately)
	go us.incrementAccessCount(shortURL)

	return mapping.OriginalURL, true
}

func (us *URLShortener) incrementAccessCount(shortURL string) {
	us.mu.Lock()
	defer us.mu.Unlock()

	if mapping, exists := us.mappings[shortURL]; exists {
		mapping.AccessCount++
		us.mappings[shortURL] = mapping
	}
}

func (us *URLShortener) GetStats(shortURL string) (URLMapping, bool) {
	us.mu.RLock()
	defer us.mu.RUnlock()

	mapping, exists := us.mappings[shortURL]
	return mapping, exists
}

func main() {
	shortener := NewURLShortener()

	http.HandleFunc("/shorten", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		var request struct {
			URL string `json:"url"`
		}

		if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
			http.Error(w, "Invalid JSON", http.StatusBadRequest)
			return
		}

		if request.URL == "" {
			http.Error(w, "URL is required", http.StatusBadRequest)
			return
		}

		shortID := shortener.CreateShortURL(request.URL)

		response := map[string]string{
			"short_url":    shortID,
			"original_url": request.URL,
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)
	})

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		shortURL := r.URL.Path[1:] // Remove leading slash
		if shortURL == "" {
			http.ServeFile(w, r, "index.html")
			return
		}

		originalURL, exists := shortener.GetOriginalURL(shortURL)
		if !exists {
			http.NotFound(w, r)
			return
		}

		http.Redirect(w, r, originalURL, http.StatusFound)
	})

	http.HandleFunc("/stats/", func(w http.ResponseWriter, r *http.Request) {
		shortURL := r.URL.Path[len("/stats/"):]
		stats, exists := shortener.GetStats(shortURL)
		if !exists {
			http.NotFound(w, r)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(stats)
	})

	fmt.Println("URL Shortener server started on :8080")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Println("Error starting server:", err)
		os.Exit(1)
	}
}
