# File Watcher

A Go-based file system monitoring tool that watches directories for changes and reports file events in real-time.

## Features

- **Real-time Monitoring**: Watches directories for file system events
- **Recursive Watching**: Automatically monitors all subdirectories
- **Multiple Events**: Detects create, write, remove, rename, and chmod operations
- **Event Details**: Provides file path, operation type, size, and timestamp
- **Concurrent Safe**: Thread-safe operation with proper synchronization
- **Multiple Directories**: Can monitor multiple directories simultaneously

## Supported Events

- **CREATE**: File or directory created
- **WRITE**: File content modified
- **REMOVE**: File or directory deleted
- **RENAME**: File or directory renamed
- **CHMOD**: File permissions changed

## Installation

```bash
cd go-projects/file-watcher
go mod download
```

## Usage

### Basic Usage
```bash
go run main.go /path/to/watch
```

### Multiple Directories
```bash
go run main.go /path/to/dir1 /path/to/dir2 /path/to/dir3
```

### Example Output
```
Watching directory: /path/to/watch
Started monitoring 1 directories:
  - /path/to/watch
Press Ctrl+C to stop...

[15:30:45] CREATE /path/to/watch/newfile.txt (0 bytes)
[15:30:46] WRITE /path/to/watch/newfile.txt (1024 bytes)
[15:30:47] REMOVE /path/to/watch/oldfile.txt
```

## API Usage

You can also use the FileWatcher as a library in your Go applications:

```go
package main

import (
    "fmt"
    "log"
)

func main() {
    // Create a new file watcher
    watcher, err := NewFileWatcher([]string{"/path/to/watch"})
    if err != nil {
        log.Fatal(err)
    }

    // Start watching
    if err := watcher.Start(); err != nil {
        log.Fatal(err)
    }
    defer watcher.Stop()

    // Process events
    for event := range watcher.Events() {
        fmt.Printf("Event: %s %s\n", event.Operation, event.Path)
    }
}
```

## Configuration

The file watcher uses the excellent [fsnotify](https://github.com/fsnotify/fsnotify) library for cross-platform file system notifications.

## Event Channel

Events are sent through a buffered channel (capacity: 100 events). If the channel becomes full, new events will be dropped and logged.

## Platform Support

- ✅ Linux (inotify)
- ✅ macOS (FSEvents, kqueue)
- ✅ Windows (ReadDirectoryChangesW)

## Performance Considerations

- Monitoring many files/directories may impact performance
- The watcher uses inotify on Linux which has limits on the number of watches
- Consider using dedicated monitoring solutions for production systems with high file activity

## Error Handling

- Directory not found errors are reported at startup
- File system errors during operation are logged but don't stop the watcher
- Permission errors may prevent watching certain directories

## Building

```bash
go build -o file-watcher main.go
```

## License

This project is for educational purposes as part of the 50 Projects collection.
