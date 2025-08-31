import time
import tkinter as tk
from tkinter import messagebox
import winsound  # For Windows sound alerts

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Timer settings (in seconds)
        self.work_time = 25 * 60  # 25 minutes
        self.break_time = 5 * 60   # 5 minutes
        self.long_break_time = 15 * 60  # 15 minutes
        
        self.current_time = self.work_time
        self.is_running = False
        self.is_break = False
        self.pomodoro_count = 0
        
        self.create_widgets()
        self.update_display()
    
    def create_widgets(self):
        """Create the GUI widgets"""
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Timer display
        self.time_label = tk.Label(main_frame, font=("Arial", 48, "bold"))
        self.time_label.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(main_frame, font=("Arial", 14))
        self.status_label.pack(pady=10)
        
        # Pomodoro count
        self.count_label = tk.Label(main_frame, font=("Arial", 12))
        self.count_label.pack(pady=5)
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(button_frame, text="Start", command=self.start_timer, width=10)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = tk.Button(button_frame, text="Pause", command=self.pause_timer, width=10, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_timer, width=10)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Settings frame
        settings_frame = tk.Frame(main_frame)
        settings_frame.pack(pady=10)
        
        tk.Label(settings_frame, text="Work:").grid(row=0, column=0, padx=5)
        self.work_var = tk.StringVar(value="25")
        work_spin = tk.Spinbox(settings_frame, from_=1, to=60, width=5, textvariable=self.work_var)
        work_spin.grid(row=0, column=1, padx=5)
        
        tk.Label(settings_frame, text="Break:").grid(row=0, column=2, padx=5)
        self.break_var = tk.StringVar(value="5")
        break_spin = tk.Spinbox(settings_frame, from_=1, to=30, width=5, textvariable=self.break_var)
        break_spin.grid(row=0, column=3, padx=5)
        
        tk.Label(settings_frame, text="Long Break:").grid(row=0, column=4, padx=5)
        self.long_break_var = tk.StringVar(value="15")
        long_break_spin = tk.Spinbox(settings_frame, from_=1, to=30, width=5, textvariable=self.long_break_var)
        long_break_spin.grid(row=0, column=5, padx=5)
        
        apply_button = tk.Button(settings_frame, text="Apply", command=self.apply_settings)
        apply_button.grid(row=0, column=6, padx=5)
    
    def apply_settings(self):
        """Apply new timer settings"""
        try:
            self.work_time = int(self.work_var.get()) * 60
            self.break_time = int(self.break_var.get()) * 60
            self.long_break_time = int(self.long_break_var.get()) * 60
            self.reset_timer()
            messagebox.showinfo("Settings", "Timer settings updated!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
    
    def format_time(self, seconds):
        """Format seconds into MM:SS format"""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def update_display(self):
        """Update the timer display"""
        self.time_label.config(text=self.format_time(self.current_time))
        
        if self.is_break:
            if self.pomodoro_count % 4 == 0:
                self.status_label.config(text="Long Break Time! 🎉")
            else:
                self.status_label.config(text="Break Time! ☕")
        else:
            self.status_label.config(text="Work Time! 💪")
        
        self.count_label.config(text=f"Pomodoros: {self.pomodoro_count}")
    
    def start_timer(self):
        """Start the timer"""
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.run_timer()
    
    def pause_timer(self):
        """Pause the timer"""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
    
    def reset_timer(self):
        """Reset the timer"""
        self.is_running = False
        self.is_break = False
        self.current_time = self.work_time
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.update_display()
    
    def run_timer(self):
        """Run the timer countdown"""
        if self.is_running:
            if self.current_time > 0:
                self.current_time -= 1
                self.update_display()
                self.root.after(1000, self.run_timer)
            else:
                self.timer_complete()
    
    def timer_complete(self):
        """Handle timer completion"""
        self.is_running = False
        self.play_sound()
        
        if self.is_break:
            # Break completed, start work time
            self.is_break = False
            self.current_time = self.work_time
            messagebox.showinfo("Break Over", "Time to get back to work! 💪")
        else:
            # Work completed, start break time
            self.is_break = True
            self.pomodoro_count += 1
            
            if self.pomodoro_count % 4 == 0:
                self.current_time = self.long_break_time
                messagebox.showinfo("Work Complete", "Great job! Time for a long break! 🎉")
            else:
                self.current_time = self.break_time
                messagebox.showinfo("Work Complete", "Good work! Time for a short break! ☕")
        
        self.update_display()
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
    
    def play_sound(self):
        """Play a sound alert"""
        try:
            winsound.Beep(1000, 1000)  # Frequency 1000Hz, duration 1000ms
        except:
            pass  # Sound might not work on all systems

def main():
    """Main function to run the Pomodoro timer"""
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
