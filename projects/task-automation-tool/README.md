# Task Automation Tool

A command-line application designed to automate various tasks such as file management, backups, and command execution. This tool allows users to schedule tasks, manage configurations, and run them efficiently.

## Features
- **Task Scheduling**: Schedule tasks to run at specific intervals (daily, hourly, or minutely)
- **File Cleanup**: Automatically delete old files based on age and size criteria
- **Backup Management**: Create backups of files and directories
- **Command Execution**: Run system commands and scripts
- **File Organization**: Organize files by type or date
- **Logging**: Detailed logging of task execution and errors
- **Configuration Management**: Load and save task configurations in JSON format

## Prerequisites
- Python 3.x
- Required Python libraries: schedule, validators, cryptography

## Installation
```bash
pip install schedule validators cryptography
```

## How to Run
```bash
python main.py
```

## Usage

### Adding Tasks
1. Run the application and choose option 1 to add a task.
2. Select the type of task (file cleanup, backup, command execution, or file organizer).
3. Provide the necessary parameters for the task.
4. Optionally, set a schedule for the task.

### Running Tasks
- Choose option 4 to run a specific task immediately.
- Choose option 6 to start the task scheduler, which will run tasks based on their configured schedules.

### Viewing Tasks
- Choose option 5 to list all configured tasks, their status, and last run times.

### Example Commands
- Add a file cleanup task to delete files older than 30 days.
- Schedule a backup task to run daily at 2 AM.

## Configuration File
The application uses a JSON configuration file (`automation_config.json`) to store task settings. You can manually edit this file to adjust task parameters.

## Logging
All task execution logs are saved in `automation.log`. This file contains information about task runs, errors, and other important events.

## Security Considerations
- Ensure that sensitive commands and file paths are protected.
- Use secure passwords for any tasks that require authentication.
- Validate all user inputs to prevent command injection.

## Customization
You can extend the application by:
- Adding new task types
- Implementing a graphical user interface
- Integrating with cloud storage services
- Adding email notifications for task completions
- Implementing a web-based dashboard for task management

## Troubleshooting
- Ensure all required libraries are installed.
- Check the log file for detailed error messages.
- Verify that the configuration file is correctly formatted.

## Future Enhancements
- User authentication for task management
- Support for more complex scheduling options
- Integration with third-party APIs for enhanced functionality
- Improved error handling and user feedback

## File Structure
```
task-automation-tool/
├── main.py          # Main application
├── automation_config.json # Configuration file (auto-generated)
└── requirements.txt # Python dependencies
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- Inspired by various task automation tools and libraries.
- Uses the `schedule` library for task scheduling.
