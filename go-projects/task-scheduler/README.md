# Task Scheduler

A command-line task management application built with Go that allows you to schedule, track, and manage tasks with priorities and due dates.

## Features
- Add tasks with titles, descriptions, due dates, and priorities
- Mark tasks as complete
- Delete tasks
- View all tasks or filter by priority
- Identify overdue tasks
- Persistent storage using JSON files
- Interactive command-line interface

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

## Usage

### Main Menu Options:
1. **Add task** - Create a new task with details
2. **List all tasks** - View all tasks with complete information
3. **Mark task as complete** - Update task status
4. **Delete task** - Remove a task permanently
5. **Show overdue tasks** - View tasks that are past their due date
6. **Show tasks by priority** - Filter tasks by priority level
7. **Save tasks** - Manually save tasks to file
8. **Exit** - Exit the application (auto-saves)

### Task Properties:
- **ID**: Unique identifier (UUID)
- **Title**: Short description of the task
- **Description**: Detailed explanation
- **Due Date**: When the task should be completed (YYYY-MM-DD format)
- **Priority**: "low", "medium", or "high"
- **Status**: "Pending" or "Completed"
- **Created At**: When the task was created

### Data Persistence:
Tasks are automatically saved to `tasks.json` when you exit the application. You can also manually save at any time using option 7.

## Example Usage

1. Start the application:
   ```bash
   go run main.go
   ```

2. Add a task:
   ```
   Enter task title: Complete project report
   Enter task description: Write the final report for the Q4 project
   Enter due date (YYYY-MM-DD): 2023-12-15
   Enter priority (low/medium/high): high
   ```

3. View all tasks:
   ```
   ID: 123e4567-e89b-12d3-a456-426614174000
   Title: Complete project report
   Description: Write the final report for the Q4 project
   Due: 2023-12-15
   Priority: high
   Status: Pending
   Created: 2023-12-07 14:30
   ```

4. Mark task as complete:
   ```
   Enter task ID to mark as complete: 123e4567-e89b-12d3-a456-426614174000
   ```

## File Format

Tasks are stored in `tasks.json` with the following format:
```json
[
  {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Task description",
    "due_date": "2023-12-15T00:00:00Z",
    "priority": "high",
    "completed": false,
    "created_at": "2023-12-07T14:30:00Z"
  }
]
```

## Dependencies
- github.com/google/uuid v1.4.0

## Notes
- Tasks are stored locally in JSON format
- Date format: YYYY-MM-DD
- Priorities: "low", "medium", "high"
- Overdue tasks are calculated based on current system time
- Simple and intuitive command-line interface
- Suitable for personal task management
