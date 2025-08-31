package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"sync"
	"time"
)

// User represents a user in the system
type User struct {
	ID        int       `json:"id"`
	Name      string    `json:"name"`
	Email     string    `json:"email"`
	CreatedAt time.Time `json:"created_at"`
}

// Product represents a product in the system
type Product struct {
	ID          int     `json:"id"`
	Name        string  `json:"name"`
	Description string  `json:"description"`
	Price       float64 `json:"price"`
	Stock       int     `json:"stock"`
}

// API Server holds the application state
type APIServer struct {
	users    map[int]*User
	products map[int]*Product
	mu       sync.RWMutex
	nextUserID int
	nextProductID int
}

// NewAPIServer creates a new API server instance
func NewAPIServer() *APIServer {
	return &APIServer{
		users:    make(map[int]*User),
		products: make(map[int]*Product),
		nextUserID: 1,
		nextProductID: 1,
	}
}

// JSONResponse sends a JSON response
func JSONResponse(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(data)
}

// ErrorResponse sends an error response
func ErrorResponse(w http.ResponseWriter, status int, message string) {
	JSONResponse(w, status, map[string]string{"error": message})
}

// HealthCheckHandler handles health check requests
func (s *APIServer) HealthCheckHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		ErrorResponse(w, http.StatusMethodNotAllowed, "Method not allowed")
		return
	}

	response := map[string]interface{}{
		"status":    "healthy",
		"timestamp": time.Now().Format(time.RFC3339),
		"users":     len(s.users),
		"products":  len(s.products),
	}
	JSONResponse(w, http.StatusOK, response)
}

// GetUsersHandler returns all users
func (s *APIServer) GetUsersHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		ErrorResponse(w, http.StatusMethodNotAllowed, "Method not allowed")
		return
	}

	s.mu.RLock()
	defer s.mu.RUnlock()

	users := make([]*User, 0, len(s.users))
	for _, user := range s.users {
		users = append(users, user)
	}

	JSONResponse(w, http.StatusOK, users)
}

// CreateUserHandler creates a new user
func (s *APIServer) CreateUserHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		ErrorResponse(w, http.StatusMethodNotAllowed, "Method not allowed")
		return
	}

	var user User
	if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
		ErrorResponse(w, http.StatusBadRequest, "Invalid JSON")
		return
	}

	if user.Name == "" || user.Email == "" {
		ErrorResponse(w, http.StatusBadRequest, "Name and email are required")
		return
	}

	s.mu.Lock()
	defer s.mu.Unlock()

	user.ID = s.nextUserID
	user.CreatedAt = time.Now()
	s.users[user.ID] = &user
	s.nextUserID++

	JSONResponse(w, http.StatusCreated, user)
}

// GetProductsHandler returns all products
func (s *APIServer) GetProductsHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		ErrorResponse(w, http.StatusMethodNotAllowed, "Method not allowed")
		return
	}

	s.mu.RLock()
	defer s.mu.RUnlock()

	products := make([]*Product, 0, len(s.products))
	for _, product := range s.products {
		products = append(products, product)
	}

	JSONResponse(w, http.StatusOK, products)
}

// CreateProductHandler creates a new product
func (s *APIServer) CreateProductHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		ErrorResponse(w, http.StatusMethodNotAllowed, "Method not allowed")
		return
	}

	var product Product
	if err := json.NewDecoder(r.Body).Decode(&product); err != nil {
		ErrorResponse(w, http.StatusBadRequest, "Invalid JSON")
		return
	}

	if product.Name == "" || product.Price <= 0 {
		ErrorResponse(w, http.StatusBadRequest, "Name and positive price are required")
		return
	}

	s.mu.Lock()
	defer s.mu.Unlock()

	product.ID = s.nextProductID
	s.products[product.ID] = &product
	s.nextProductID++

	JSONResponse(w, http.StatusCreated, product)
}

// GetProductByIDHandler returns a specific product
func (s *APIServer) GetProductByIDHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		ErrorResponse(w, http.StatusMethodNotAllowed, "Method not allowed")
		return
	}

	idStr := r.URL.Path[len("/api/products/"):]
	id, err := strconv.Atoi(idStr)
	if err != nil {
		ErrorResponse(w, http.StatusBadRequest, "Invalid product ID")
		return
	}

	s.mu.RLock()
	defer s.mu.RUnlock()

	product, exists := s.products[id]
	if !exists {
		ErrorResponse(w, http.StatusNotFound, "Product not found")
		return
	}

	JSONResponse(w, http.StatusOK, product)
}

// SetupRoutes configures the HTTP routes
func (s *APIServer) SetupRoutes() {
	http.HandleFunc("/health", s.HealthCheckHandler)
	http.HandleFunc("/api/users", s.GetUsersHandler)
	http.HandleFunc("/api/users/create", s.CreateUserHandler)
	http.HandleFunc("/api/products", s.GetProductsHandler)
	http.HandleFunc("/api/products/create", s.CreateProductHandler)
	http.HandleFunc("/api/products/", s.GetProductByIDHandler)
}

func main() {
	server := NewAPIServer()
	server.SetupRoutes()

	// Add some sample data
	server.mu.Lock()
	server.products[1] = &Product{
		ID:          1,
		Name:        "Laptop",
		Description: "High-performance laptop",
		Price:       999.99,
		Stock:       10,
	}
	server.products[2] = &Product{
		ID:          2,
		Name:        "Smartphone",
		Description: "Latest smartphone model",
		Price:       699.99,
		Stock:       25,
	}
	server.nextProductID = 3
	server.mu.Unlock()

	fmt.Println("REST API Server started on :8080")
	fmt.Println("Endpoints:")
	fmt.Println("  GET  /health              - Health check")
	fmt.Println("  GET  /api/users           - Get all users")
	fmt.Println("  POST /api/users/create    - Create a new user")
	fmt.Println("  GET  /api/products        - Get all products")
	fmt.Println("  POST /api/products/create - Create a new product")
	fmt.Println("  GET  /api/products/{id}   - Get product by ID")

	log.Fatal(http.ListenAndServe(":8080", nil))
}
