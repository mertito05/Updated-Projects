package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"

	"github.com/google/uuid"
	"golang.org/x/crypto/bcrypt"
)

type User struct {
	ID        string    `json:"id"`
	Username  string    `json:"username"`
	Email     string    `json:"email"`
	Password  string    `json:"-"`
	CreatedAt time.Time `json:"created_at"`
}

type Post struct {
	ID        string    `json:"id"`
	Title     string    `json:"title"`
	Content   string    `json:"content"`
	AuthorID  string    `json:"author_id"`
	Author    string    `json:"author"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

type BlogPlatform struct {
	users []User
	posts []Post
	mu    sync.RWMutex
}

func NewBlogPlatform() *BlogPlatform {
	return &BlogPlatform{
		users: make([]User, 0),
		posts: make([]Post, 0),
	}
}

func (bp *BlogPlatform) CreateUser(username, email, password string) (User, error) {
	bp.mu.Lock()
	defer bp.mu.Unlock()

	// Check if username or email already exists
	for _, user := range bp.users {
		if user.Username == username || user.Email == email {
			return User{}, fmt.Errorf("username or email already exists")
		}
	}

	// Hash password
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return User{}, err
	}

	user := User{
		ID:        uuid.New().String(),
		Username:  username,
		Email:     email,
		Password:  string(hashedPassword),
		CreatedAt: time.Now(),
	}

	bp.users = append(bp.users, user)
	return user, nil
}

func (bp *BlogPlatform) AuthenticateUser(username, password string) (User, error) {
	bp.mu.RLock()
	defer bp.mu.RUnlock()

	for _, user := range bp.users {
		if user.Username == username {
			err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(password))
			if err != nil {
				return User{}, fmt.Errorf("invalid password")
			}
			return user, nil
		}
	}
	return User{}, fmt.Errorf("user not found")
}

func (bp *BlogPlatform) CreatePost(title, content, authorID string) (Post, error) {
	bp.mu.Lock()
	defer bp.mu.Unlock()

	// Find author username
	var author string
	for _, user := range bp.users {
		if user.ID == authorID {
			author = user.Username
			break
		}
	}
	if author == "" {
		return Post{}, fmt.Errorf("author not found")
	}

	post := Post{
		ID:        uuid.New().String(),
		Title:     title,
		Content:   content,
		AuthorID:  authorID,
		Author:    author,
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}

	bp.posts = append(bp.posts, post)
	return post, nil
}

func (bp *BlogPlatform) GetPosts() []Post {
	bp.mu.RLock()
	defer bp.mu.RUnlock()

	return bp.posts
}

func (bp *BlogPlatform) GetPostByID(id string) (Post, bool) {
	bp.mu.RLock()
	defer bp.mu.RUnlock()

	for _, post := range bp.posts {
		if post.ID == id {
			return post, true
		}
	}
	return Post{}, false
}

func (bp *BlogPlatform) GetUserPosts(userID string) []Post {
	bp.mu.RLock()
	defer bp.mu.RUnlock()

	var userPosts []Post
	for _, post := range bp.posts {
		if post.AuthorID == userID {
			userPosts = append(userPosts, post)
		}
	}
	return userPosts
}

func main() {
	blog := NewBlogPlatform()

	// Serve static files
	http.Handle("/", http.FileServer(http.Dir(".")))

	// API endpoints
	http.HandleFunc("/api/register", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}

		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		var request struct {
			Username string `json:"username"`
			Email    string `json:"email"`
			Password string `json:"password"`
		}

		if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
			http.Error(w, "Invalid JSON", http.StatusBadRequest)
			return
		}

		user, err := blog.CreateUser(request.Username, request.Email, request.Password)
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		// Don't return password in response
		user.Password = ""
		json.NewEncoder(w).Encode(user)
	})

	http.HandleFunc("/api/login", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}

		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		var request struct {
			Username string `json:"username"`
			Password string `json:"password"`
		}

		if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
			http.Error(w, "Invalid JSON", http.StatusBadRequest)
			return
		}

		user, err := blog.AuthenticateUser(request.Username, request.Password)
		if err != nil {
			http.Error(w, "Invalid credentials", http.StatusUnauthorized)
			return
		}

		// Don't return password in response
		user.Password = ""
		json.NewEncoder(w).Encode(user)
	})

	http.HandleFunc("/api/posts", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}

		switch r.Method {
		case http.MethodGet:
			posts := blog.GetPosts()
			json.NewEncoder(w).Encode(posts)

		case http.MethodPost:
			var request struct {
				Title   string `json:"title"`
				Content string `json:"content"`
				AuthorID string `json:"author_id"`
			}

			if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
				http.Error(w, "Invalid JSON", http.StatusBadRequest)
				return
			}

			if request.Title == "" || request.Content == "" || request.AuthorID == "" {
				http.Error(w, "Title, content, and author_id are required", http.StatusBadRequest)
				return
			}

			post, err := blog.CreatePost(request.Title, request.Content, request.AuthorID)
			if err != nil {
				http.Error(w, err.Error(), http.StatusBadRequest)
				return
			}

			json.NewEncoder(w).Encode(post)

		default:
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	http.HandleFunc("/api/posts/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")

		if r.Method != http.MethodGet {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		id := r.URL.Path[len("/api/posts/"):]
		if id == "" {
			http.Error(w, "Post ID required", http.StatusBadRequest)
			return
		}

		post, exists := blog.GetPostByID(id)
		if !exists {
			http.NotFound(w, r)
			return
		}

		json.NewEncoder(w).Encode(post)
	})

	http.HandleFunc("/api/users/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")

		if r.Method != http.MethodGet {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		path := r.URL.Path[len("/api/users/"):]
		parts := strings.Split(path, "/")
		
		if len(parts) < 2 || parts[1] != "posts" {
			http.NotFound(w, r)
			return
		}

		userID := parts[0]
		posts := blog.GetUserPosts(userID)
		json.NewEncoder(w).Encode(posts)
	})

	fmt.Println("Blog Platform server started on :8080")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Println("Error starting server:", err)
		os.Exit(1)
	}
}
