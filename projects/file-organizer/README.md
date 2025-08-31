# File Organizer

A comprehensive command-line file organization tool that helps you automatically sort, categorize, and manage your files. This tool provides multiple organization methods and advanced features like duplicate detection and directory analysis.

## Features
- **Multiple Organization Methods**: Organize files by extension, date, size, or MIME type
- **Flexible Operations**: Copy or move files during organization
- **Duplicate Detection**: Find and remove duplicate files by content hash
- **Directory Statistics**: Get detailed analytics about file types and sizes
- **History Tracking**: Keep track of all organization operations
- **Export Capabilities**: Export organization history and statistics
- **Safe Operations**: Dry run mode for testing before making changes
- **Recursive Processing**: Handle nested directory structures

## Prerequisites
- Python 3.x
- No additional packages required (uses standard library)

## Installation
No additional installation required. The tool uses Python's standard library.

## How to Run
```bash
python main.py
```

## Usage

### Organization Methods

#### 1. By Extension
Organizes files into folders based on their file extensions (e.g., `.txt`, `.jpg`, `.pdf`).

#### 2. By Date
Organizes files into date-based folders using:
- **Modified date**: When the file was last changed
- **Created date**: When the file was created
- **Accessed date**: When the file was last accessed

#### 3. By Size
Categorizes files into size-based folders:
- **Tiny**: 0 - 1KB
- **Small**: 1KB - 10KB
- **Medium**: 10KB - 1MB
- **Large**: 1MB - 10MB
- **Huge**: 10MB+

#### 4. By Type
Organizes files by MIME type categories (e.g., `image`, `text`, `video`).

### Advanced Features

#### Duplicate Detection
- Finds files with identical content using MD5 hashing
- Shows duplicate groups with file paths
- Safe removal with dry-run mode

#### Directory Statistics
- Total file count and size
- Breakdown by file extensions
- Size category distribution
- Export to CSV format

#### Operation History
- Tracks all organization operations
- Records source, destination, and file counts
- Export to JSON format

## Command Line Options

The application provides an interactive menu with these options:

1. **Organize by Extension**: Sort files by their extensions
2. **Organize by Date**: Sort files by creation/modification/access dates
3. **Organize by Size**: Sort files into size categories
4. **Organize by Type**: Sort files by MIME type categories
5. **Find Duplicates**: Detect duplicate files by content
6. **Remove Duplicates**: Delete duplicate files (with dry-run option)
7. **Get Directory Statistics**: Analyze file distribution and sizes
8. **Export History**: Save organization history to JSON
9. **Export Statistics**: Save directory stats to CSV
10. **Exit**: Quit the application

## File Operations

### Copy vs Move
- **Copy**: Creates duplicates in organized folders, preserves originals
- **Move**: Transfers files to organized folders, removes from source

### Destination Directory
- Can specify different destination directory
- If not specified, uses source directory for organization

## Safety Features

### Dry Run Mode
- Preview what would be removed before deleting duplicates
- No actual file operations performed in dry run

### Error Handling
- Graceful handling of permission errors
- Skip files that can't be processed
- Detailed error messages

### Backup Recommendation
- Always backup important files before bulk operations
- Use copy mode first to verify organization results

## Performance Considerations

### Large Directories
- Efficient file processing with chunked reading
- Memory-friendly duplicate detection
- Progress feedback during operations

### Network Drives
- Works with local and network file systems
- Consider performance impact on network operations

## Customization

You can extend the tool by:

### Adding New Organization Methods
- Implement custom categorization logic
- Add new file attribute-based organization

### Modifying Size Categories
- Adjust size thresholds in the code
- Add custom size ranges

### Enhanced Statistics
- Add more detailed analytics
- Implement visual reporting
- Add file type-specific statistics

### Integration
- Add command-line arguments
- Create scheduled tasks
- Integrate with file watchers

## File Structure
```
file-organizer/
├── main.py          # Main application
├── organize_history.json # Operation history (auto-generated)
└── directory_stats.csv   # Statistics export (auto-generated)
```

## Troubleshooting

### Common Issues
- **Permission Errors**: Ensure write access to directories
- **Large Files**: Be patient with very large files during hashing
- **Network Issues**: Check connectivity for network drives
- **Unsupported Files**: Some special files may not be processed

### Error Messages
- Clear error messages with file paths
- Skip problematic files and continue
- Logging of all operations

## Best Practices

### Before Organization
1. Backup important files
2. Test with copy mode first
3. Review duplicate detection results
4. Check available disk space

### During Organization
1. Monitor progress for large operations
2. Verify results in destination folders
3. Keep organization history for reference

### After Organization
1. Verify file integrity
2. Clean up source directory if needed
3. Export statistics for record keeping

## Future Enhancements
- Graphical user interface
- Real-time directory monitoring
- Cloud storage integration
- Advanced duplicate matching (similar content)
- File content analysis
- Automated organization rules
- Email notifications
- Mobile app version
- Web interface
- API for integration
- Plugin system
- Machine learning categorization
- Image recognition
- Document content analysis

## Legal and Security
- No data leaves your local machine
- All processing happens locally
- No internet connection required
- Open source and transparent

## Support
For issues and feature requests, please check the source code comments or documentation. The tool is designed to be modular and extensible for custom requirements.
