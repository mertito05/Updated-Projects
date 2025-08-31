package main

import (
	"encoding/json"
	"fmt"
	"os"
	"time"

	"github.com/google/uuid"
)

type Task struct {
	ID          string    `json:"id"`
	Title       string    `json:"title"`
	Description string    `json:"description"`
	DueDate     time.Time `json:"due_date"`
	Priority    string    `json:"priority"` // "low", "medium", "high"
	Completed   bool      `json:"completed"`
	CreatedAt   time.Time `json:"created_at"`
}

type TaskScheduler struct {
	tasks []Task
}

func NewTaskScheduler() *TaskScheduler {
	return &TaskScheduler{
		tasks: make([]Task, 0),
	}
}

func (ts *TaskScheduler) AddTask(title, description string, dueDate time.Time, priority string) Task {
	task := Task{
		ID:          uuid.New().String(),
		Title:       title,
		Description: description,
		DueDate:     dueDate,
		Priority:    priority,
		Completed:   false,
		CreatedAt:   time.Now(),
	}

	ts.tasks = append(ts.tasks, task)
	return task
}

func (ts *TaskScheduler) ListTasks() []Task {
	return ts.tasks
}

func (ts *TaskScheduler) GetTaskByID(id string) (Task, bool) {
	for _, task := range ts.tasks {
		if task.ID == id {
			return task, true
		}
	}
	return Task{}, false
}

func (ts *TaskScheduler) CompleteTask(id string) bool {
	for i, task := range ts.tasks {
		if task.ID == id {
			ts.tasks[i].Completed = true
			return true
		}
	}
	return false
}

func (ts *TaskScheduler) DeleteTask(id string) bool {
	for i, task := range ts.tasks {
		if task.ID == id {
			ts.tasks = append(ts.tasks[:i], ts.tasks[i+1:]...)
			return true
		}
	}
	return false
}

func (ts *TaskScheduler) GetOverdueTasks() []Task {
	var overdue []Task
	now := time.Now()

	for _, task := range ts.tasks {
		if !task.Completed && task.DueDate.Before(now) {
			overdue = append(overdue, task)
		}
	}
	return overdue
}

func (ts *TaskScheduler) GetTasksByPriority(priority string) []Task {
	var filtered []Task
	for _, task := range ts.tasks {
		if task.Priority == priority {
			filtered = append(filtered, task)
		}
	}
	return filtered
}

func (ts *TaskScheduler) SaveToFile(filename string) error {
	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "  ")
	return encoder.Encode(ts.tasks)
}

func (ts *TaskScheduler) LoadFromFile(filename string) error {
	file, err := os.Open(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	return json.NewDecoder(file).Decode(&ts.tasks)
}

func main() {
	scheduler := NewTaskScheduler()
	
	// Load tasks from file if it exists
	if err := scheduler.LoadFromFile("tasks.json"); err != nil {
		fmt.Println("No existing tasks file found, starting fresh")
	}

	for {
		fmt.Println("\nTask Scheduler")
		fmt.Println("==============")
		fmt.Println("1. Add task")
		fmt.Println("2. List all tasks")
		fmt.Println("3. Mark task as complete")
		fmt.Println("4. Delete task")
		fmt.Println("5. Show overdue tasks")
		fmt.Println("6. Show tasks by priority")
		fmt.Println("7. Save tasks")
		fmt.Println("8. Exit")

		var choice int
		fmt.Print("\nEnter your choice (1-8): ")
		fmt.Scanln(&choice)

		switch choice {
		case 1:
			var title, description, priority string
			var dueDateStr string

			fmt.Print("Enter task title: ")
			fmt.Scanln(&title)
			fmt.Print("Enter task description: ")
			fmt.Scanln(&description)
			fmt.Print("Enter due date (YYYY-MM-DD): ")
			fmt.Scanln(&dueDateStr)
			fmt.Print("Enter priority (low/medium/high): ")
			fmt.Scanln(&priority)

			dueDate, err := time.Parse("2006-01-02", dueDateStr)
			if err != nil {
				fmt.Println("Invalid date format. Use YYYY-MM-DD")
				continue
			}

			task := scheduler.AddTask(title, description, dueDate, priority)
			fmt.Printf("Task added: %s (ID: %s)\n", task.Title, task.ID)

		case 2:
			tasks := scheduler.ListTasks()
			if len(tasks) == 0 {
				fmt.Println("No tasks found.")
				continue
			}

			fmt.Println("\nAll Tasks:")
			fmt.Println("==========")
			for _, task := range tasks {
				status := "Pending"
				if task.Completed {
					status = "Completed"
				}
				fmt.Printf("ID: %s\n", task.ID)
				fmt.Printf("Title: %s\n", task.Title)
				fmt.Printf("Description: %s\n", task.Description)
				fmt.Printf("Due: %s\n", task.DueDate.Format("2006-01-02"))
				fmt.Printf("Priority: %s\n", task.Priority)
				fmt.Printf("Status: %s\n", status)
				fmt.Printf("Created: %s\n", task.CreatedAt.Format("2006-01-02 15:04"))
				fmt.Println("---")
			}

		case 3:
			var id string
			fmt.Print("Enter task ID to mark as complete: ")
			fmt.Scanln(&id)

			if scheduler.CompleteTask(id) {
				fmt.Println("Task marked as complete.")
			} else {
				fmt.Println("Task not found.")
			}

		case 4:
			var id string
			fmt.Print("Enter task ID to delete: ")
			fmt.Scanln(&id)

			if scheduler.DeleteTask(id) {
				fmt.Println("Task deleted.")
			} else {
				fmt.Println("Task not found.")
			}

		case 5:
			overdue := scheduler.GetOverdueTasks()
			if len(overdue) == 0 {
				fmt.Println("No overdue tasks.")
				continue
			}

			fmt.Println("\nOverdue Tasks:")
			fmt.Println("==============")
			for _, task := range overdue {
				fmt.Printf("ID: %s\n", task.ID)
				fmt.Printf("Title: %s\n", task.Title)
				fmt.Printf("Due: %s (Overdue by %v days)\n", 
					task.DueDate.Format("2006-01-02"),
					time.Since(task.DueDate).Hours()/24)
				fmt.Println("---")
			}

		case 6:
			var priority string
			fmt.Print("Enter priority to filter (low/medium/high): ")
			fmt.Scanln(&priority)

			tasks := scheduler.GetTasksByPriority(priority)
			if len(tasks) == 0 {
				fmt.Printf("No tasks with priority '%s'.\n", priority)
				continue
			}

			fmt.Printf("\nTasks with priority '%s':\n", priority)
			fmt.Println("========================")
			for _, task := range tasks {
				status := "Pending"
				if task.Completed {
					status = "Completed"
				}
				fmt.Printf("ID: %s\n", task.ID)
				fmt.Printf("Title: %s\n", task.Title)
				fmt.Printf("Due: %s\n", task.DueDate.Format("2006-01-02"))
				fmt.Printf("Status: %s\n", status)
				fmt.Println("---")
			}

		case 7:
			if err := scheduler.SaveToFile("tasks.json"); err != nil {
				fmt.Println("Error saving tasks:", err)
			} else {
				fmt.Println("Tasks saved to tasks.json")
			}

		case 8:
			// Save before exiting
			if err := scheduler.SaveToFile("tasks.json"); err != nil {
				fmt.Println("Error saving tasks:", err)
			}
			fmt.Println("Goodbye!")
			return

		default:
			fmt.Println("Invalid choice. Please try again.")
		}
	}
}
