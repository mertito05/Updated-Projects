package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"sync"
	"time"

	"github.com/fsnotify/fsnotify"
)

// FileEvent represents a file system event
type FileEvent struct {
	Path      string    `json:"path"`
	Operation string    `json:"operation"`
	Size      int64     `json:"size"`
	Timestamp time.Time `json:"timestamp"`
}

// FileWatcher monitors directories for changes
type FileWatcher struct {
	watcher   *fsnotify.Watcher
	events    chan FileEvent
	stop      chan bool
	wg        sync.WaitGroup
	watchDirs []string
}

// NewFileWatcher creates a new file watcher instance
func NewFileWatcher(dirs []string) (*FileWatcher, error) {
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		return nil, err
	}

	return &FileWatcher{
		watcher:   watcher,
		events:    make(chan FileEvent, 100),
		stop:      make(chan bool),
		watchDirs: dirs,
	}, nil
}

// Start begins watching the specified directories
func (fw *FileWatcher) Start() error {
	// Add directories to watch
	for _, dir := range fw.watchDirs {
		if err := fw.watcher.Add(dir); err != nil {
			return fmt.Errorf("failed to watch directory %s: %v", dir, err)
		}
		fmt.Printf("Watching directory: %s\n", dir)
	}

	fw.wg.Add(1)
	go fw.watchLoop()

	return nil
}

// Stop stops the file watcher
func (fw *FileWatcher) Stop() {
	close(fw.stop)
	fw.wg.Wait()
	fw.watcher.Close()
}

// watchLoop handles file system events
func (fw *FileWatcher) watchLoop() {
	defer fw.wg.Done()

	for {
		select {
		case event, ok := <-fw.watcher.Events:
			if !ok {
				return
			}
			fw.handleEvent(event)

		case err, ok := <-fw.watcher.Errors:
			if !ok {
				return
			}
			log.Printf("File watcher error: %v", err)

		case <-fw.stop:
			return
		}
	}
}

// handleEvent processes a file system event
func (fw *FileWatcher) handleEvent(event fsnotify.Event) {
	var operation string
	switch {
	case event.Op&fsnotify.Create == fsnotify.Create:
		operation = "CREATE"
	case event.Op&fsnotify.Write == fsnotify.Write:
		operation = "WRITE"
	case event.Op&fsnotify.Remove == fsnotify.Remove:
		operation = "REMOVE"
	case event.Op&fsnotify.Rename == fsnotify.Rename:
		operation = "RENAME"
	case event.Op&fsnotify.Chmod == fsnotify.Chmod:
		operation = "CHMOD"
	default:
		return
	}

	// Get file info if it exists
	var size int64
	if operation != "REMOVE" {
		if info, err := os.Stat(event.Name); err == nil {
			size = info.Size()
		}
	}

	fileEvent := FileEvent{
		Path:      event.Name,
		Operation: operation,
		Size:      size,
		Timestamp: time.Now(),
	}

	// Send event to channel
	select {
	case fw.events <- fileEvent:
	default:
		log.Printf("Event channel full, dropping event: %v", fileEvent)
	}
}

// Events returns the channel for receiving file events
func (fw *FileWatcher) Events() <-chan FileEvent {
	return fw.events
}

// printEvents prints file events to console
func (fw *FileWatcher) printEvents() {
	for event := range fw.events {
		fmt.Printf("[%s] %s %s", event.Timestamp.Format("15:04:05"), event.Operation, event.Path)
		if event.Size > 0 {
			fmt.Printf(" (%d bytes)", event.Size)
		}
		fmt.Println()
	}
}

// monitorDirectory monitors a single directory recursively
func monitorDirectory(path string) error {
	absPath, err := filepath.Abs(path)
	if err != nil {
		return err
	}

	// Check if directory exists
	if _, err := os.Stat(absPath); os.IsNotExist(err) {
		return fmt.Errorf("directory does not exist: %s", absPath)
	}

	// Get all subdirectories
	var dirs []string
	err = filepath.Walk(absPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() {
			dirs = append(dirs, path)
		}
		return nil
	})

	if err != nil {
		return err
	}

	watcher, err := NewFileWatcher(dirs)
	if err != nil {
		return err
	}

	if err := watcher.Start(); err != nil {
		return err
	}
	defer watcher.Stop()

	fmt.Printf("Started monitoring %s and %d subdirectories\n", absPath, len(dirs)-1)
	fmt.Println("Press Ctrl+C to stop...")
	fmt.Println()

	// Start printing events
	go watcher.printEvents()

	// Wait for interrupt
	<-make(chan struct{})

	return nil
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: file-watcher <directory> [directory2 ...]")
		fmt.Println("Example: file-watcher ./my-folder /tmp/logs")
		os.Exit(1)
	}

	dirs := os.Args[1:]

	// Create a watcher for the specified directories
	watcher, err := NewFileWatcher(dirs)
	if err != nil {
		log.Fatal(err)
	}

	if err := watcher.Start(); err != nil {
		log.Fatal(err)
	}
	defer watcher.Stop()

	fmt.Printf("Started monitoring %d directories:\n", len(dirs))
	for _, dir := range dirs {
		fmt.Printf("  - %s\n", dir)
	}
	fmt.Println("Press Ctrl+C to stop...")
	fmt.Println()

	// Start printing events
	go watcher.printEvents()

	// Wait for interrupt
	<-make(chan struct{})
}
