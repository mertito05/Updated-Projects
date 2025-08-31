import os
import json
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

class ImageGallery:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Gallery")
        self.root.geometry("800x600")
        
        self.images = []
        self.current_index = 0
        self.gallery_file = "gallery_data.json"
        
        self.load_gallery_data()
        self.create_widgets()
        self.update_display()
    
    def create_widgets(self):
        """Create the GUI widgets"""
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Image display
        self.image_label = tk.Label(main_frame)
        self.image_label.pack(pady=10)
        
        # Navigation frame
        nav_frame = tk.Frame(main_frame)
        nav_frame.pack(pady=5)
        
        self.prev_button = tk.Button(nav_frame, text="← Previous", command=self.prev_image)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        
        self.next_button = tk.Button(nav_frame, text="Next →", command=self.next_image)
        self.next_button.pack(side=tk.LEFT, padx=5)
        
        # Info frame
        info_frame = tk.Frame(main_frame)
        info_frame.pack(pady=5)
        
        self.info_label = tk.Label(info_frame, text="", font=("Arial", 10))
        self.info_label.pack()
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        add_button = tk.Button(button_frame, text="Add Images", command=self.add_images)
        add_button.pack(side=tk.LEFT, padx=5)
        
        remove_button = tk.Button(button_frame, text="Remove Current", command=self.remove_current)
        remove_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = tk.Button(button_frame, text="Clear All", command=self.clear_gallery)
        clear_button.pack(side=tk.LEFT, padx=5)
    
    def load_gallery_data(self):
        """Load gallery data from JSON file"""
        if os.path.exists(self.gallery_file):
            try:
                with open(self.gallery_file, 'r') as f:
                    self.images = json.load(f)
            except:
                self.images = []
        else:
            self.images = []
    
    def save_gallery_data(self):
        """Save gallery data to JSON file"""
        with open(self.gallery_file, 'w') as f:
            json.dump(self.images, f, indent=2)
    
    def add_images(self):
        """Add images to the gallery"""
        file_paths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        
        if file_paths:
            for file_path in file_paths:
                if file_path not in self.images:
                    self.images.append(file_path)
            
            self.save_gallery_data()
            self.update_display()
            messagebox.showinfo("Success", f"Added {len(file_paths)} image(s) to gallery")
    
    def remove_current(self):
        """Remove the current image from the gallery"""
        if not self.images:
            return
        
        self.images.pop(self.current_index)
        self.save_gallery_data()
        
        if self.current_index >= len(self.images):
            self.current_index = max(0, len(self.images) - 1)
        
        self.update_display()
    
    def clear_gallery(self):
        """Clear all images from the gallery"""
        if not self.images:
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all images?"):
            self.images = []
            self.current_index = 0
            self.save_gallery_data()
            self.update_display()
    
    def next_image(self):
        """Show the next image"""
        if not self.images:
            return
        
        self.current_index = (self.current_index + 1) % len(self.images)
        self.update_display()
    
    def prev_image(self):
        """Show the previous image"""
        if not self.images:
            return
        
        self.current_index = (self.current_index - 1) % len(self.images)
        self.update_display()
    
    def update_display(self):
        """Update the image display and info"""
        if not self.images:
            self.image_label.config(image='')
            self.info_label.config(text="No images in gallery")
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
            return
        
        self.prev_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.NORMAL)
        
        try:
            # Load and resize image
            image_path = self.images[self.current_index]
            image = Image.open(image_path)
            
            # Resize to fit in the window
            max_size = (600, 400)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage for Tkinter
            photo = tk.PhotoImage(image=image)
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Keep a reference
            
            # Update info
            file_name = os.path.basename(image_path)
            info_text = f"Image {self.current_index + 1} of {len(self.images)}: {file_name}"
            self.info_label.config(text=info_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {e}")
            self.remove_current()

def main():
    """Main function to run the image gallery"""
    root = tk.Tk()
    app = ImageGallery(root)
    root.mainloop()

if __name__ == "__main__":
    main()
