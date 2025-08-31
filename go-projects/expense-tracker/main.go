package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strconv"
	"sync"
	"time"

	"github.com/google/uuid"
)

type Expense struct {
	ID          string    `json:"id"`
	Amount      float64   `json:"amount"`
	Category    string    `json:"category"`
	Description string    `json:"description"`
	Date        time.Time `json:"date"`
}

type ExpenseTracker struct {
	expenses []Expense
	mu       sync.RWMutex
}

func NewExpenseTracker() *ExpenseTracker {
	return &ExpenseTracker{
		expenses: make([]Expense, 0),
	}
}

func (et *ExpenseTracker) AddExpense(amount float64, category, description string) Expense {
	et.mu.Lock()
	defer et.mu.Unlock()

	expense := Expense{
		ID:          uuid.New().String(),
		Amount:      amount,
		Category:    category,
		Description: description,
		Date:        time.Now(),
	}

	et.expenses = append(et.expenses, expense)
	return expense
}

func (et *ExpenseTracker) GetExpenses() []Expense {
	et.mu.RLock()
	defer et.mu.RUnlock()

	return et.expenses
}

func (et *ExpenseTracker) GetExpenseByID(id string) (Expense, bool) {
	et.mu.RLock()
	defer et.mu.RUnlock()

	for _, expense := range et.expenses {
		if expense.ID == id {
			return expense, true
		}
	}
	return Expense{}, false
}

func (et *ExpenseTracker) DeleteExpense(id string) bool {
	et.mu.Lock()
	defer et.mu.Unlock()

	for i, expense := range et.expenses {
		if expense.ID == id {
			et.expenses = append(et.expenses[:i], et.expenses[i+1:]...)
			return true
		}
	}
	return false
}

func (et *ExpenseTracker) GetTotalExpenses() float64 {
	et.mu.RLock()
	defer et.mu.RUnlock()

	var total float64
	for _, expense := range et.expenses {
		total += expense.Amount
	}
	return total
}

func (et *ExpenseTracker) GetExpensesByCategory() map[string]float64 {
	et.mu.RLock()
	defer et.mu.RUnlock()

	categoryTotals := make(map[string]float64)
	for _, expense := range et.expenses {
		categoryTotals[expense.Category] += expense.Amount
	}
	return categoryTotals
}

func main() {
	tracker := NewExpenseTracker()

	// Serve static files
	http.Handle("/", http.FileServer(http.Dir(".")))

	// API endpoints
	http.HandleFunc("/api/expenses", func(w http.ResponseWriter, r *http.Request) {
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
			expenses := tracker.GetExpenses()
			json.NewEncoder(w).Encode(expenses)

		case http.MethodPost:
			var request struct {
				Amount      float64 `json:"amount"`
				Category    string  `json:"category"`
				Description string  `json:"description"`
			}

			if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
				http.Error(w, "Invalid JSON", http.StatusBadRequest)
				return
			}

			if request.Amount <= 0 || request.Category == "" {
				http.Error(w, "Amount and category are required", http.StatusBadRequest)
				return
			}

			expense := tracker.AddExpense(request.Amount, request.Category, request.Description)
			json.NewEncoder(w).Encode(expense)

		default:
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	http.HandleFunc("/api/expenses/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}

		id := r.URL.Path[len("/api/expenses/"):]
		if id == "" {
			http.Error(w, "Expense ID required", http.StatusBadRequest)
			return
		}

		if r.Method == http.MethodDelete {
			if tracker.DeleteExpense(id) {
				w.WriteHeader(http.StatusNoContent)
			} else {
				http.NotFound(w, r)
			}
		} else {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	http.HandleFunc("/api/stats", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")

		if r.Method != http.MethodGet {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		stats := map[string]interface{}{
			"total":      tracker.GetTotalExpenses(),
			"byCategory": tracker.GetExpensesByCategory(),
			"count":      len(tracker.GetExpenses()),
		}

		json.NewEncoder(w).Encode(stats)
	})

	fmt.Println("Expense Tracker server started on :8080")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Println("Error starting server:", err)
		os.Exit(1)
	}
}
