package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

// Task represents a single task
type Task struct {
	ID          int       `json:"id"`
	Title       string    `json:"title"`
	Description string    `json:"description"`
	Completed   bool      `json:"completed"`
	Priority    int       `json:"priority"`
	DueDate     time.Time `json:"due_date"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}

// TaskManager manages tasks
type TaskManager struct {
	tasks     []Task
	nextID    int
	filePath  string
}

// NewTaskManager creates a new task manager
func NewTaskManager(filePath string) *TaskManager {
	return &TaskManager{
		tasks:    make([]Task, 0),
		nextID:   1,
		filePath: filePath,
	}
}

// AddTask adds a new task
func (tm *TaskManager) AddTask(title, description string, priority int, dueDate time.Time) Task {
	task := Task{
		ID:          tm.nextID,
		Title:       title,
		Description: description,
		Completed:   false,
		Priority:    priority,
		DueDate:     dueDate,
		CreatedAt:   time.Now(),
		UpdatedAt:   time.Now(),
	}
	tm.tasks = append(tm.tasks, task)
	tm.nextID++
	return task
}

// ListTasks returns all tasks
func (tm *TaskManager) ListTasks() []Task {
	return tm.tasks
}

// GetTaskByID returns a task by ID
func (tm *TaskManager) GetTaskByID(id int) (*Task, error) {
	for i, task := range tm.tasks {
		if task.ID == id {
			return &tm.tasks[i], nil
		}
	}
	return nil, fmt.Errorf("task not found with ID %d", id)
}

// CompleteTask marks a task as completed
func (tm *TaskManager) CompleteTask(id int) error {
	task, err := tm.GetTaskByID(id)
	if err != nil {
		return err
	}
	task.Completed = true
	task.UpdatedAt = time.Now()
	return nil
}

// DeleteTask removes a task
func (tm *TaskManager) DeleteTask(id int) error {
	for i, task := range tm.tasks {
		if task.ID == id {
			tm.tasks = append(tm.tasks[:i], tm.tasks[i+1:]...)
			return nil
		}
	}
	return fmt.Errorf("task not found with ID %d", id)
}

// UpdateTask updates a task
func (tm *TaskManager) UpdateTask(id int, title, description string, priority int, dueDate time.Time) error {
	task, err := tm.GetTaskByID(id)
	if err != nil {
		return err
	}
	task.Title = title
	task.Description = description
	task.Priority = priority
	task.DueDate = dueDate
	task.UpdatedAt = time.Now()
	return nil
}

// SaveToFile saves tasks to a file
func (tm *TaskManager) SaveToFile() error {
	file, err := os.Create(tm.filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "  ")
	return encoder.Encode(tm.tasks)
}

// LoadFromFile loads tasks from a file
func (tm *TaskManager) LoadFromFile() error {
	file, err := os.Open(tm.filePath)
	if err != nil {
		if os.IsNotExist(err) {
			return nil // File doesn't exist yet, that's okay
		}
		return err
	}
	defer file.Close()

	var tasks []Task
	if err := json.NewDecoder(file).Decode(&tasks); err != nil {
		return err
	}

	tm.tasks = tasks
	// Find the maximum ID to set nextID
	maxID := 0
	for _, task := range tasks {
		if task.ID > maxID {
			maxID = task.ID
		}
	}
	tm.nextID = maxID + 1
	return nil
}

// PrintTask prints a single task
func PrintTask(task Task) {
	status := "❌"
	if task.Completed {
		status = "✅"
	}

	fmt.Printf("\n%s Task #%d: %s\n", status, task.ID, task.Title)
	fmt.Printf("   Description: %s\n", task.Description)
	fmt.Printf("   Priority: %d\n", task.Priority)
	if !task.DueDate.IsZero() {
		fmt.Printf("   Due: %s\n", task.DueDate.Format("2006-01-02"))
	}
	fmt.Printf("   Created: %s\n", task.CreatedAt.Format("2006-01-02 15:04"))
	fmt.Printf("   Updated: %s\n", task.UpdatedAt.Format("2006-01-02 15:04"))
}

// PrintTasks prints all tasks
func PrintTasks(tasks []Task) {
	if len(tasks) == 0 {
		fmt.Println("No tasks found.")
		return
	}

	for _, task := range tasks {
		PrintTask(task)
	}
}

// GetUserInput gets input from the user
func GetUserInput(prompt string) string {
	fmt.Print(prompt)
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan()
	return strings.TrimSpace(scanner.Text())
}

// ParseDate parses a date string
func ParseDate(dateStr string) (time.Time, error) {
	if dateStr == "" {
		return time.Time{}, nil
	}
	return time.Parse("2006-01-02", dateStr)
}

func main() {
	tm := NewTaskManager("tasks.json")

	// Load existing tasks
	if err := tm.LoadFromFile(); err != nil {
		fmt.Printf("Error loading tasks: %v\n", err)
	}

	fmt.Println("📝 CLI Task Manager")
	fmt.Println("===================")

	for {
		fmt.Println("\nOptions:")
		fmt.Println("1. List tasks")
		fmt.Println("2. Add task")
		fmt.Println("3. Complete task")
		fmt.Println("4. Delete task")
		fmt.Println("5. Update task")
		fmt.Println("6. Save and exit")
		fmt.Println("7. Exit without saving")

		choice := GetUserInput("Choose an option (1-7): ")

		switch choice {
		case "1":
			tasks := tm.ListTasks()
			PrintTasks(tasks)

		case "2":
			title := GetUserInput("Title: ")
			description := GetUserInput("Description: ")
			priorityStr := GetUserInput("Priority (1-5): ")
			dueDateStr := GetUserInput("Due date (YYYY-MM-DD, optional): ")

			priority, err := strconv.Atoi(priorityStr)
			if err != nil {
				priority = 3
			}

			dueDate, err := ParseDate(dueDateStr)
			if err != nil {
				fmt.Println("Invalid date format, using no due date")
				dueDate = time.Time{}
			}

			task := tm.AddTask(title, description, priority, dueDate)
			fmt.Printf("Added task #%d\n", task.ID)

		case "3":
			idStr := GetUserInput("Task ID to complete: ")
			id, err := strconv.Atoi(idStr)
			if err != nil {
				fmt.Println("Invalid ID")
				continue
			}

			if err := tm.CompleteTask(id); err != nil {
				fmt.Printf("Error: %v\n", err)
			} else {
				fmt.Println("Task completed!")
			}

		case "4":
			idStr := GetUserInput("Task ID to delete: ")
			id, err := strconv.Atoi(idStr)
			if err != nil {
				fmt.Println("Invalid ID")
				continue
			}

			if err := tm.DeleteTask(id); err != nil {
				fmt.Printf("Error: %v\n", err)
			} else {
				fmt.Println("Task deleted!")
			}

		case "5":
			idStr := GetUserInput("Task ID to update: ")
			id, err := strconv.Atoi(idStr)
			if err != nil {
				fmt.Println("Invalid ID")
				continue
			}

			title := GetUserInput("New title: ")
			description := GetUserInput("New description: ")
			priorityStr := GetUserInput("New priority (1-5): ")
			dueDateStr := GetUserInput("New due date (YYYY-MM-DD, optional): ")

			priority, err := strconv.Atoi(priorityStr)
			if err != nil {
				priority = 3
			}

			dueDate, err := ParseDate(dueDateStr)
			if err != nil {
				fmt.Println("Invalid date format, using no due date")
				dueDate = time.Time{}
			}

			if err := tm.UpdateTask(id, title, description, priority, dueDate); err != nil {
				fmt.Printf("Error: %v\n", err)
			} else {
				fmt.Println("Task updated!")
			}

		case "6":
			if err := tm.SaveToFile(); err != nil {
				fmt.Printf("Error saving tasks: %v\n", err)
			} else {
				fmt.Println("Tasks saved to tasks.json")
			}
			fmt.Println("Goodbye!")
			return

		case "7":
			fmt.Println("Goodbye!")
			return

		default:
			fmt.Println("Invalid option. Please choose 1-7.")
		}
	}
}
