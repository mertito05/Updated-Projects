# CLI Task Manager

A command-line task management application built with Go that helps you organize and track your tasks with a simple interface.

## Features

- **Task Management**: Create, read, update, and delete tasks
- **Priority Levels**: Assign priority levels (1-5) to tasks
- **Due Dates**: Set optional due dates for tasks
- **Completion Tracking**: Mark tasks as completed
- **Persistence**: Save tasks to a JSON file
- **Simple Interface**: Easy-to-use command-line interface
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

```bash
cd go-projects/cli-task-manager
go build -o task-manager main.go
```

## Usage

### Running the Application
```bash
go run main.go
```

Or if built:
```bash
./task-manager
```

### Available Commands

When running the application, you'll see a menu with these options:

1. **List tasks** - View all tasks
2. **Add task** - Create a new task
3. **Complete task** - Mark a task as completed
4. **Delete task** - Remove a task
5. **Update task** - Modify an existing task
6. **Save and exit** - Save changes and quit
7. **Exit without saving** - Quit without saving changes

### Task Structure

Each task contains:
- **ID**: Unique identifier
- **Title**: Task name
- **Description**: Detailed description
- **Completed**: Completion status (✅ or ❌)
- **Priority**: Importance level (1-5)
- **Due Date**: Optional deadline
- **Created At**: Creation timestamp
- **Updated At**: Last modification timestamp

## Examples

### Adding a Task
```
Title: Complete project report
Description: Finish the quarterly project report and submit to manager
Priority (1-5): 2
Due date (YYYY-MM-DD, optional): 2024-01-20
```

### Listing Tasks
```
❌ Task #1: Complete project report
   Description: Finish the quarterly project report and submit to manager
   Priority: 2
   Due: 2024-01-20
   Created: 2024-01-15 14:30
   Updated: 2024-01-15 14:30

✅ Task #2: Buy groceries
   Description: Milk, eggs, bread, and vegetables
   Priority: 3
   Created: 2024-01-14 09:15
   Updated: 2024-01-14 10:30
```

## Data Storage

Tasks are stored in a JSON file (`tasks.json`) in the same directory as the executable. The file format is human-readable:

```json
[
  {
    "id": 1,
    "title": "Complete project report",
    "description": "Finish the quarterly project report and submit to manager",
    "completed": false,
    "priority": 2,
    "due_date": "2024-01-20T00:00:00Z",
    "created_at": "2024-01-15T14:30:00Z",
    "updated_at": "2024-01-15T14:30:00Z"
  }
]
```

## Keyboard Shortcuts

- Use number keys (1-7) to select menu options
- Press Enter to confirm inputs
- Use Ctrl+C to force quit (may lose unsaved changes)

## Error Handling

- Invalid inputs are handled gracefully with helpful error messages
- File I/O errors are displayed but don't crash the application
- Missing files are created automatically when saving

## Building for Distribution

```bash
# Build for current platform
go build -o task-manager main.go

# Build for specific platforms
GOOS=windows GOARCH=amd64 go build -o task-manager.exe main.go
GOOS=linux GOARCH=amd64 go build -o task-manager main.go
GOOS=darwin GOARCH=amd64 go build -o task-manager main.go
```

## Dependencies

- Go 1.21 or later
- Standard library only (no external dependencies)

## Customization

You can customize the application by:

1. Modifying the task structure in `main.go`
2. Changing the storage file path
3. Adding new features like categories or tags
4. Implementing sorting and filtering options
5. Adding color output for better readability

## License

This project is for educational purposes as part of the 50 Projects collection.
