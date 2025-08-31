import pygame
import os
import time
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import List, Optional

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.playlist: List[str] = []
        self.current_track_index: int = 0
        self.paused: bool = False
        self.volume: float = 0.5
        self.current_position: float = 0
        
        # Set initial volume
        pygame.mixer.music.set_volume(self.volume)
    
    def load_playlist(self, directory: str) -> bool:
        """Load all audio files from a directory"""
        if not os.path.exists(directory):
            return False
        
        audio_extensions = {'.mp3', '.wav', '.ogg', '.flac', '.m4a'}
        self.playlist = []
        
        for file_path in Path(directory).rglob('*'):
            if file_path.suffix.lower() in audio_extensions and file_path.is_file():
                self.playlist.append(str(file_path))
        
        return len(self.playlist) > 0
    
    def play(self, track_index: Optional[int] = None) -> bool:
        """Play a track from the playlist"""
        if not self.playlist:
            return False
        
        if track_index is not None:
            if 0 <= track_index < len(self.playlist):
                self.current_track_index = track_index
            else:
                return False
        
        try:
            pygame.mixer.music.load(self.playlist[self.current_track_index])
            pygame.mixer.music.play()
            self.paused = False
            return True
        except pygame.error:
            return False
    
    def pause(self) -> bool:
        """Pause the current track"""
        if pygame.mixer.music.get_busy() and not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
            return True
        return False
    
    def unpause(self) -> bool:
        """Unpause the current track"""
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            return True
        return False
    
    def stop(self) -> bool:
        """Stop the current track"""
        if pygame.mixer.music.get_busy() or self.paused:
            pygame.mixer.music.stop()
            self.paused = False
            return True
        return False
    
    def next_track(self) -> bool:
        """Play the next track in the playlist"""
        if not self.playlist:
            return False
        
        self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
        return self.play()
    
    def previous_track(self) -> bool:
        """Play the previous track in the playlist"""
        if not self.playlist:
            return False
        
        self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
        return self.play()
    
    def set_volume(self, volume: float) -> bool:
        """Set the volume (0.0 to 1.0)"""
        if 0.0 <= volume <= 1.0:
            self.volume = volume
            pygame.mixer.music.set_volume(volume)
            return True
        return False
    
    def get_current_track_info(self) -> Optional[dict]:
        """Get information about the current track"""
        if not self.playlist or self.current_track_index >= len(self.playlist):
            return None
        
        track_path = self.playlist[self.current_track_index]
        file_name = os.path.basename(track_path)
        file_size = os.path.getsize(track_path)
        
        return {
            'path': track_path,
            'name': file_name,
            'size': file_size,
            'index': self.current_track_index,
            'total': len(self.playlist),
            'position': self.get_position(),
            'length': self.get_length(),
            'volume': self.volume,
            'paused': self.paused,
            'playing': pygame.mixer.music.get_busy() and not self.paused
        }
    
    def get_position(self) -> float:
        """Get current playback position in seconds"""
        if pygame.mixer.music.get_busy() and not self.paused:
            # pygame doesn't have a direct way to get position, so we estimate
            # This is a simple implementation - for accurate position, consider using other libraries
            return pygame.mixer.music.get_pos() / 1000.0  # Convert milliseconds to seconds
        return 0.0
    
    def get_length(self) -> float:
        """Get total length of current track in seconds"""
        # pygame doesn't have a direct way to get track length
        # This would require additional libraries like mutagen
        # For now, return 0 and implement properly if needed
        return 0.0
    
    def seek(self, position: float) -> bool:
        """Seek to a specific position in the track"""
        # pygame doesn't support seeking directly
        # This would require stopping and restarting playback
        # For now, this is a placeholder
        return False
    
    def get_playlist(self) -> List[str]:
        """Get the current playlist"""
        return self.playlist.copy()

class MusicPlayerGUI:
    def __init__(self):
        self.player = MusicPlayer()
        self.root = tk.Tk()
        self.root.title("Python Music Player")
        self.root.geometry("600x400")
        
        self.setup_ui()
        self.update_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Playlist frame
        playlist_frame = tk.Frame(main_frame)
        playlist_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        tk.Label(playlist_frame, text="Playlist", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        self.playlist_listbox = tk.Listbox(playlist_frame, height=10)
        self.playlist_listbox.pack(fill=tk.BOTH, expand=True)
        self.playlist_listbox.bind('<<ListboxSelect>>', self.on_track_select)
        
        # Control frame
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        # Load button
        load_btn = tk.Button(control_frame, text="Load Folder", command=self.load_folder)
        load_btn.pack(side=tk.LEFT, padx=5)
        
        # Play/Pause button
        self.play_pause_btn = tk.Button(control_frame, text="Play", command=self.toggle_play_pause)
        self.play_pause_btn.pack(side=tk.LEFT, padx=5)
        
        # Stop button
        stop_btn = tk.Button(control_frame, text="Stop", command=self.stop)
        stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Previous button
        prev_btn = tk.Button(control_frame, text="Previous", command=self.previous)
        prev_btn.pack(side=tk.LEFT, padx=5)
        
        # Next button
        next_btn = tk.Button(control_frame, text="Next", command=self.next)
        next_btn.pack(side=tk.LEFT, padx=5)
        
        # Volume control
        volume_frame = tk.Frame(control_frame)
        volume_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(volume_frame, text="Volume:").pack(side=tk.LEFT)
        self.volume_scale = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                   command=self.on_volume_change, length=100)
        self.volume_scale.set(50)
        self.volume_scale.pack(side=tk.LEFT)
        
        # Status frame
        status_frame = tk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = tk.Label(status_frame, text="Ready to play music", 
                                   font=("Arial", 10), anchor=tk.W)
        self.status_label.pack(fill=tk.X)
        
        # Current track info
        self.track_label = tk.Label(status_frame, text="No track selected", 
                                  font=("Arial", 9), anchor=tk.W, fg="gray")
        self.track_label.pack(fill=tk.X)
    
    def load_folder(self):
        """Load music files from a folder"""
        folder_path = filedialog.askdirectory(title="Select Music Folder")
        if folder_path:
            if self.player.load_playlist(folder_path):
                self.update_playlist()
                self.status_label.config(text=f"Loaded {len(self.player.playlist)} tracks")
            else:
                messagebox.showerror("Error", "No music files found in the selected folder")
    
    def update_playlist(self):
        """Update the playlist display"""
        self.playlist_listbox.delete(0, tk.END)
        for track_path in self.player.playlist:
            track_name = os.path.basename(track_path)
            self.playlist_listbox.insert(tk.END, track_name)
    
    def on_track_select(self, event):
        """Handle track selection from playlist"""
        selection = self.playlist_listbox.curselection()
        if selection:
            track_index = selection[0]
            self.player.play(track_index)
            self.update_ui()
    
    def toggle_play_pause(self):
        """Toggle between play and pause"""
        if self.player.paused:
            self.player.unpause()
        else:
            if not pygame.mixer.music.get_busy():
                # If nothing is playing, start from current track
                self.player.play()
            else:
                self.player.pause()
        self.update_ui()
    
    def stop(self):
        """Stop playback"""
        self.player.stop()
        self.update_ui()
    
    def previous(self):
        """Play previous track"""
        self.player.previous_track()
        self.update_ui()
    
    def next(self):
        """Play next track"""
        self.player.next_track()
        self.update_ui()
    
    def on_volume_change(self, value):
        """Handle volume change"""
        volume = int(value) / 100.0
        self.player.set_volume(volume)
    
    def update_ui(self):
        """Update the UI based on current player state"""
        track_info = self.player.get_current_track_info()
        
        if track_info:
            # Update track info
            track_text = f"Now playing: {track_info['name']} "
            track_text += f"({track_info['index'] + 1}/{track_info['total']})"
            self.track_label.config(text=track_text)
            
            # Update play/pause button
            if track_info['playing']:
                self.play_pause_btn.config(text="Pause")
                self.status_label.config(text="Playing")
            elif track_info['paused']:
                self.play_pause_btn.config(text="Play")
                self.status_label.config(text="Paused")
            else:
                self.play_pause_btn.config(text="Play")
                self.status_label.config(text="Stopped")
            
            # Select current track in playlist
            self.playlist_listbox.selection_clear(0, tk.END)
            self.playlist_listbox.selection_set(track_info['index'])
            self.playlist_listbox.activate(track_info['index'])
        else:
            self.track_label.config(text="No track selected")
            self.play_pause_btn.config(text="Play")
            self.status_label.config(text="Ready to play music")
        
        # Schedule next update
        self.root.after(1000, self.update_ui)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main function"""
    app = MusicPlayerGUI()
    app.run()

if __name__ == "__main__":
    main()
