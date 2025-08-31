import os
import shutil
import time
import schedule
import json
from datetime import datetime, timedelta
import subprocess
import logging
from pathlib import Path
import zipfile
import hashlib

class TaskAutomationTool:
    def __init__(self, config_file='automation_config.json'):
        self.config_file = config_file
        self.tasks = self.load_config()
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('automation.log'),
                logging.StreamHandler()
            ]
        )
    
    def load_config(self):
        """Load automation configuration"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            return {}
    
    def save_config(self):
        """Save automation configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
            logging.info("Configuration saved")
        except Exception as e:
            logging.error(f"Error saving config: {e}")
    
    def add_task(self, task_name, task_type, **kwargs):
        """Add a new automation task"""
        if task_name in self.tasks:
            logging.warning(f"Task '{task_name}' already exists")
            return False
        
        task_config = {
            'type': task_type,
            'enabled': True,
            'created_at': datetime.now().isoformat(),
            'last_run': None,
            'next_run': None
        }
        task_config.update(kwargs)
        
        self.tasks[task_name] = task_config
        self.save_config()
        logging.info(f"Task '{task_name}' added successfully")
        return True
    
    def remove_task(self, task_name):
        """Remove an automation task"""
        if task_name in self.tasks:
            del self.tasks[task_name]
            self.save_config()
            logging.info(f"Task '{task_name}' removed")
            return True
        logging.warning(f"Task '{task_name}' not found")
        return False
    
    def enable_task(self, task_name, enabled=True):
        """Enable or disable a task"""
        if task_name in self.tasks:
            self.tasks[task_name]['enabled'] = enabled
            self.save_config()
            status = "enabled" if enabled else "disabled"
            logging.info(f"Task '{task_name}' {status}")
            return True
        logging.warning(f"Task '{task_name}' not found")
        return False
    
    def run_task(self, task_name):
        """Run a specific task"""
        if task_name not in self.tasks or not self.tasks[task_name]['enabled']:
            logging.warning(f"Task '{task_name}' not found or disabled")
            return False
        
        task = self.tasks[task_name]
        task_type = task['type']
        
        logging.info(f"Running task: {task_name}")
        
        try:
            if task_type == 'file_cleanup':
                self.run_file_cleanup(task)
            elif task_type == 'backup':
                self.run_backup(task)
            elif task_type == 'command':
                self.run_command(task)
            elif task_type == 'file_organizer':
                self.run_file_organizer(task)
            else:
                logging.error(f"Unknown task type: {task_type}")
                return False
            
            # Update last run time
            self.tasks[task_name]['last_run'] = datetime.now().isoformat()
            self.save_config()
            logging.info(f"Task '{task_name}' completed successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error running task '{task_name}': {e}")
            return False
    
    def run_file_cleanup(self, task):
        """Clean up files based on criteria"""
        directory = task.get('directory', '.')
        pattern = task.get('pattern', '*')
        max_age_days = task.get('max_age_days', 30)
        min_size_mb = task.get('min_size_mb', 0)
        
        cutoff_time = datetime.now() - timedelta(days=max_age_days)
        min_size_bytes = min_size_mb * 1024 * 1024
        
        deleted_count = 0
        freed_space = 0
        
        for file_path in Path(directory).rglob(pattern):
            if file_path.is_file():
                file_stat = file_path.stat()
                file_age = datetime.fromtimestamp(file_stat.st_mtime)
                file_size = file_stat.st_size
                
                if (file_age < cutoff_time and 
                    file_size >= min_size_bytes and
                    self.is_safe_to_delete(file_path)):
                    
                    try:
                        freed_space += file_size
                        file_path.unlink()
                        deleted_count += 1
                        logging.info(f"Deleted: {file_path}")
                    except Exception as e:
                        logging.error(f"Error deleting {file_path}: {e}")
        
        logging.info(f"Cleanup completed: {deleted_count} files deleted, "
                    f"{freed_space / (1024*1024):.2f} MB freed")
    
    def run_backup(self, task):
        """Create backup of files"""
        source = task['source']
        destination = task['destination']
        backup_type = task.get('type', 'copy')
        compress = task.get('compress', False)
        
        if not os.path.exists(source):
            logging.error(f"Source path does not exist: {source}")
            return
        
        # Create destination directory if it doesn't exist
        os.makedirs(destination, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{timestamp}"
        
        if backup_type == 'copy':
            if os.path.isfile(source):
                # Backup single file
                dest_file = os.path.join(destination, f"{backup_name}_{os.path.basename(source)}")
                if compress:
                    dest_file += '.zip'
                    with zipfile.ZipFile(dest_file, 'w') as zipf:
                        zipf.write(source, os.path.basename(source))
                else:
                    shutil.copy2(source, dest_file)
            else:
                # Backup directory
                dest_dir = os.path.join(destination, backup_name)
                if compress:
                    dest_dir += '.zip'
                    shutil.make_archive(dest_dir[:-4], 'zip', source)
                else:
                    shutil.copytree(source, dest_dir)
        
        logging.info(f"Backup created: {backup_name}")
    
    def run_command(self, task):
        """Execute a system command"""
        command = task['command']
        working_dir = task.get('working_dir', '.')
        timeout = task.get('timeout', 300)
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=working_dir,
                timeout=timeout,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logging.info(f"Command executed successfully: {command}")
                if result.stdout:
                    logging.info(f"Output: {result.stdout[:500]}...")  # Limit output length
            else:
                logging.error(f"Command failed: {command}")
                logging.error(f"Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            logging.error(f"Command timed out: {command}")
        except Exception as e:
            logging.error(f"Error executing command: {e}")
    
    def run_file_organizer(self, task):
        """Organize files by type"""
        source_dir = task['source_dir']
        organize_by = task.get('organize_by', 'extension')
        
        if not os.path.exists(source_dir):
            logging.error(f"Source directory does not exist: {source_dir}")
            return
        
        organized_count = 0
        
        for file_path in Path(source_dir).iterdir():
            if file_path.is_file():
                try:
                    if organize_by == 'extension':
                        ext = file_path.suffix.lower()[1:] or 'no_extension'
                        target_dir = Path(source_dir) / ext
                    elif organize_by == 'date':
                        file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                        target_dir = Path(source_dir) / file_time.strftime('%Y-%m-%d')
                    else:
                        logging.error(f"Unknown organize_by method: {organize_by}")
                        return
                    
                    target_dir.mkdir(exist_ok=True)
                    shutil.move(str(file_path), str(target_dir / file_path.name))
                    organized_count += 1
                    
                except Exception as e:
                    logging.error(f"Error organizing {file_path}: {e}")
        
        logging.info(f"Organized {organized_count} files")
    
    def is_safe_to_delete(self, file_path):
        """Check if it's safe to delete a file"""
        # Add safety checks here
        # For example, don't delete system files, important documents, etc.
        dangerous_extensions = {'.exe', '.dll', '.sys', '.ini', '.cfg'}
        if file_path.suffix.lower() in dangerous_extensions:
            return False
        return True
    
    def schedule_tasks(self):
        """Schedule all enabled tasks"""
        for task_name, task_config in self.tasks.items():
            if task_config['enabled'] and 'schedule' in task_config:
                schedule_config = task_config['schedule']
                
                if schedule_config.get('daily'):
                    time_str = schedule_config['daily']
                    schedule.every().day.at(time_str).do(self.run_task, task_name)
                    logging.info(f"Scheduled '{task_name}' daily at {time_str}")
                
                elif schedule_config.get('hourly'):
                    schedule.every().hour.do(self.run_task, task_name)
                    logging.info(f"Scheduled '{task_name}' hourly")
                
                elif schedule_config.get('minutely'):
                    minutes = schedule_config['minutely']
                    schedule.every(minutes).minutes.do(self.run_task, task_name)
                    logging.info(f"Scheduled '{task_name}' every {minutes} minutes")
    
    def run_scheduler(self):
        """Run the task scheduler"""
        self.schedule_tasks()
        logging.info("Task scheduler started. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Scheduler stopped")

def main():
    """Main function"""
    tool = TaskAutomationTool()
    
    while True:
        print("\n=== Task Automation Tool ===")
        print("1. Add task")
        print("2. Remove task")
        print("3. Enable/disable task")
        print("4. Run task")
        print("5. List tasks")
        print("6. Start scheduler")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            print("\nTask Types:")
            print("1. File Cleanup")
            print("2. Backup")
            print("3. Command Execution")
            print("4. File Organizer")
            
            task_type_choice = input("Select task type (1-4): ").strip()
            task_types = ['file_cleanup', 'backup', 'command', 'file_organizer']
            
            if task_type_choice in ['1', '2', '3', '4']:
                task_name = input("Enter task name: ").strip()
                task_type = task_types[int(task_type_choice) - 1]
                
                # Get task-specific parameters
                params = {}
                if task_type == 'file_cleanup':
                    params['directory'] = input("Directory to clean: ").strip() or '.'
                    params['pattern'] = input("File pattern (e.g., *.log): ").strip() or '*'
                    params['max_age_days'] = int(input("Max age in days (30): ") or "30")
                    params['min_size_mb'] = int(input("Min size in MB (0): ") or "0")
                
                elif task_type == 'backup':
                    params['source'] = input("Source path: ").strip()
                    params['destination'] = input("Backup destination: ").strip()
                    params['compress'] = input("Compress? (y/n): ").strip().lower() == 'y'
                
                elif task_type == 'command':
                    params['command'] = input("Command to execute: ").strip()
                    params['working_dir'] = input("Working directory (optional): ").strip() or '.'
                    params['timeout'] = int(input("Timeout in seconds (300): ") or "300")
                
                elif task_type == 'file_organizer':
                    params['source_dir'] = input("Source directory: ").strip()
                    print("Organize by: 1. Extension, 2. Date")
                    org_choice = input("Choice (1-2): ").strip()
                    params['organize_by'] = 'extension' if org_choice == '1' else 'date'
                
                # Schedule configuration
                print("\nSchedule options:")
                print("1. Run manually only")
                print("2. Daily")
                print("3. Hourly")
                print("4. Every X minutes")
                
                sched_choice = input("Schedule choice (1-4): ").strip()
                if sched_choice != '1':
                    schedule_config = {}
                    if sched_choice == '2':
                        time_str = input("Time (HH:MM): ").strip()
                        schedule_config['daily'] = time_str
                    elif sched_choice == '3':
                        schedule_config['hourly'] = True
                    elif sched_choice == '4':
                        minutes = input("Minutes: ").strip()
                        schedule_config['minutely'] = int(minutes)
                    params['schedule'] = schedule_config
                
                tool.add_task(task_name, task_type, **params)
            else:
                print("Invalid task type")
        
        elif choice == "2":
            task_name = input("Enter task name to remove: ").strip()
            tool.remove_task(task_name)
        
        elif choice == "3":
            task_name = input("Enter task name: ").strip()
            enable = input("Enable? (y/n): ").strip().lower() == 'y'
            tool.enable_task(task_name, enable)
        
        elif choice == "4":
            task_name = input("Enter task name to run: ").strip()
            tool.run_task(task_name)
        
        elif choice == "5":
            print("\n=== Tasks ===")
            for task_name, config in tool.tasks.items():
                status = "✓" if config['enabled'] else "✗"
                last_run = config.get('last_run', 'Never')
                print(f"{status} {task_name} ({config['type']}) - Last run: {last_run}")
        
        elif choice == "6":
            tool.run_scheduler()
        
        elif choice == "7":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
