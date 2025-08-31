import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
import json
import csv
from typing import List, Dict, Set
import mimetypes

class FileOrganizer:
    def __init__(self):
        self.organize_history = []
        self.duplicate_files = {}
    
    def organize_by_extension(self, source_dir: str, dest_dir: str = None, 
                            move_files: bool = False) -> Dict[str, int]:
        """Organize files by their extensions"""
        if dest_dir is None:
            dest_dir = source_dir
        
        source_path = Path(source_dir)
        dest_path = Path(dest_dir)
        
        if not source_path.exists():
            print(f"Source directory does not exist: {source_dir}")
            return {}
        
        dest_path.mkdir(exist_ok=True)
        
        organized_files = {}
        operation = "Moved" if move_files else "Copied"
        
        for file_path in source_path.iterdir():
            if file_path.is_file():
                try:
                    # Get file extension (without dot) or use 'no_extension'
                    ext = file_path.suffix.lower()[1:] if file_path.suffix else 'no_extension'
                    
                    # Create category directory
                    category_dir = dest_path / ext
                    category_dir.mkdir(exist_ok=True)
                    
                    # Copy or move the file
                    dest_file = category_dir / file_path.name
                    
                    if move_files:
                        shutil.move(str(file_path), str(dest_file))
                    else:
                        shutil.copy2(str(file_path), str(dest_file))
                    
                    # Update statistics
                    organized_files[ext] = organized_files.get(ext, 0) + 1
                    
                    print(f"{operation} {file_path.name} to {ext}/")
                    
                except Exception as e:
                    print(f"Error processing {file_path.name}: {e}")
        
        # Record organization
        self.organize_history.append({
            'type': 'extension',
            'source': source_dir,
            'destination': dest_dir,
            'move_files': move_files,
            'files_organized': sum(organized_files.values()),
            'timestamp': datetime.now().isoformat()
        })
        
        return organized_files
    
    def organize_by_date(self, source_dir: str, dest_dir: str = None,
                       move_files: bool = False, date_type: str = 'modified') -> Dict[str, int]:
        """Organize files by date (created, modified, or accessed)"""
        if dest_dir is None:
            dest_dir = source_dir
        
        source_path = Path(source_dir)
        dest_path = Path(dest_dir)
        
        if not source_path.exists():
            print(f"Source directory does not exist: {source_dir}")
            return {}
        
        dest_path.mkdir(exist_ok=True)
        
        organized_files = {}
        operation = "Moved" if move_files else "Copied"
        date_type = date_type.lower()
        
        valid_date_types = ['modified', 'created', 'accessed']
        if date_type not in valid_date_types:
            print(f"Invalid date type. Use one of: {valid_date_types}")
            return {}
        
        for file_path in source_path.iterdir():
            if file_path.is_file():
                try:
                    # Get file date based on specified type
                    if date_type == 'modified':
                        file_date = datetime.fromtimestamp(file_path.stat().st_mtime)
                    elif date_type == 'created':
                        file_date = datetime.fromtimestamp(file_path.stat().st_ctime)
                    else:  # accessed
                        file_date = datetime.fromtimestamp(file_path.stat().st_atime)
                    
                    # Create date directory (YYYY-MM-DD format)
                    date_str = file_date.strftime('%Y-%m-%d')
                    date_dir = dest_path / date_str
                    date_dir.mkdir(exist_ok=True)
                    
                    # Copy or move the file
                    dest_file = date_dir / file_path.name
                    
                    if move_files:
                        shutil.move(str(file_path), str(dest_file))
                    else:
                        shutil.copy2(str(file_path), str(dest_file))
                    
                    # Update statistics
                    organized_files[date_str] = organized_files.get(date_str, 0) + 1
                    
                    print(f"{operation} {file_path.name} to {date_str}/")
                    
                except Exception as e:
                    print(f"Error processing {file_path.name}: {e}")
        
        # Record organization
        self.organize_history.append({
            'type': f'date_{date_type}',
            'source': source_dir,
            'destination': dest_dir,
            'move_files': move_files,
            'files_organized': sum(organized_files.values()),
            'timestamp': datetime.now().isoformat()
        })
        
        return organized_files
    
    def organize_by_size(self, source_dir: str, dest_dir: str = None,
                       move_files: bool = False) -> Dict[str, int]:
        """Organize files by size categories"""
        if dest_dir is None:
            dest_dir = source_dir
        
        source_path = Path(source_dir)
        dest_path = Path(dest_dir)
        
        if not source_path.exists():
            print(f"Source directory does not exist: {source_dir}")
            return {}
        
        dest_path.mkdir(exist_ok=True)
        
        size_categories = {
            'tiny': (0, 1024),           # 0 - 1KB
            'small': (1024, 10240),      # 1KB - 10KB
            'medium': (10240, 1048576),  # 10KB - 1MB
            'large': (1048576, 10485760), # 1MB - 10MB
            'huge': (10485760, float('inf')) # 10MB+
        }
        
        organized_files = {}
        operation = "Moved" if move_files else "Copied"
        
        for file_path in source_path.iterdir():
            if file_path.is_file():
                try:
                    file_size = file_path.stat().st_size
                    
                    # Determine size category
                    category = None
                    for cat_name, (min_size, max_size) in size_categories.items():
                        if min_size <= file_size < max_size:
                            category = cat_name
                            break
                    
                    if category is None:
                        category = 'unknown'
                    
                    # Create category directory
                    category_dir = dest_path / category
                    category_dir.mkdir(exist_ok=True)
                    
                    # Copy or move the file
                    dest_file = category_dir / file_path.name
                    
                    if move_files:
                        shutil.move(str(file_path), str(dest_file))
                    else:
                        shutil.copy2(str(file_path), str(dest_file))
                    
                    # Update statistics
                    organized_files[category] = organized_files.get(category, 0) + 1
                    
                    print(f"{operation} {file_path.name} to {category}/ ({file_size} bytes)")
                    
                except Exception as e:
                    print(f"Error processing {file_path.name}: {e}")
        
        # Record organization
        self.organize_history.append({
            'type': 'size',
            'source': source_dir,
            'destination': dest_dir,
            'move_files': move_files,
            'files_organized': sum(organized_files.values()),
            'timestamp': datetime.now().isoformat()
        })
        
        return organized_files
    
    def organize_by_type(self, source_dir: str, dest_dir: str = None,
                       move_files: bool = False) -> Dict[str, int]:
        """Organize files by MIME type"""
        if dest_dir is None:
            dest_dir = source_dir
        
        source_path = Path(source_dir)
        dest_path = Path(dest_dir)
        
        if not source_path.exists():
            print(f"Source directory does not exist: {source_dir}")
            return {}
        
        dest_path.mkdir(exist_ok=True)
        
        organized_files = {}
        operation = "Moved" if move_files else "Copied"
        
        for file_path in source_path.iterdir():
            if file_path.is_file():
                try:
                    # Get MIME type
                    mime_type, _ = mimetypes.guess_type(str(file_path))
                    
                    if mime_type:
                        # Extract main type (e.g., 'image' from 'image/jpeg')
                        main_type = mime_type.split('/')[0]
                    else:
                        main_type = 'unknown'
                    
                    # Create type directory
                    type_dir = dest_path / main_type
                    type_dir.mkdir(exist_ok=True)
                    
                    # Copy or move the file
                    dest_file = type_dir / file_path.name
                    
                    if move_files:
                        shutil.move(str(file_path), str(dest_file))
                    else:
                        shutil.copy2(str(file_path), str(dest_file))
                    
                    # Update statistics
                    organized_files[main_type] = organized_files.get(main_type, 0) + 1
                    
                    print(f"{operation} {file_path.name} to {main_type}/ ({mime_type or 'unknown'})")
                    
                except Exception as e:
                    print(f"Error processing {file_path.name}: {e}")
        
        # Record organization
        self.organize_history.append({
            'type': 'mime_type',
            'source': source_dir,
            'destination': dest_dir,
            'move_files': move_files,
            'files_organized': sum(organized_files.values()),
            'timestamp': datetime.now().isoformat()
        })
        
        return organized_files
    
    def find_duplicates(self, directory: str) -> Dict[str, List[str]]:
        """Find duplicate files by content hash"""
        directory_path = Path(directory)
        
        if not directory_path.exists():
            print(f"Directory does not exist: {directory}")
            return {}
        
        file_hashes = {}
        duplicates = {}
        
        for file_path in directory_path.rglob('*'):
            if file_path.is_file():
                try:
                    # Calculate file hash
                    file_hash = self.calculate_file_hash(file_path)
                    
                    if file_hash in file_hashes:
                        if file_hash not in duplicates:
                            duplicates[file_hash] = [file_hashes[file_hash]]
                        duplicates[file_hash].append(str(file_path))
                    else:
                        file_hashes[file_hash] = str(file_path)
                        
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        
        self.duplicate_files = duplicates
        return duplicates
    
    def calculate_file_hash(self, file_path: Path, chunk_size: int = 8192) -> str:
        """Calculate MD5 hash of a file"""
        hash_md5 = hashlib.md5()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                hash_md5.update(chunk)
        
        return hash_md5.hexdigest()
    
    def remove_duplicates(self, directory: str, dry_run: bool = True) -> int:
        """Remove duplicate files (keep one copy of each)"""
        duplicates = self.find_duplicates(directory)
        removed_count = 0
        
        for file_hash, file_paths in duplicates.items():
            if len(file_paths) > 1:
                # Keep the first file, remove others
                keep_file = file_paths[0]
                
                for file_path in file_paths[1:]:
                    if dry_run:
                        print(f"Would remove duplicate: {file_path} (same as {keep_file})")
                    else:
                        try:
                            os.remove(file_path)
                            print(f"Removed duplicate: {file_path}")
                            removed_count += 1
                        except Exception as e:
                            print(f"Error removing {file_path}: {e}")
        
        return removed_count
    
    def get_directory_stats(self, directory: str) -> Dict:
        """Get statistics about files in a directory"""
        directory_path = Path(directory)
        
        if not directory_path.exists():
            print(f"Directory does not exist: {directory}")
            return {}
        
        stats = {
            'total_files': 0,
            'total_size': 0,
            'file_types': {},
            'size_categories': {
                'tiny': 0, 'small': 0, 'medium': 0, 'large': 0, 'huge': 0
            }
        }
        
        for file_path in directory_path.rglob('*'):
            if file_path.is_file():
                try:
                    file_size = file_path.stat().st_size
                    stats['total_files'] += 1
                    stats['total_size'] += file_size
                    
                    # Count by extension
                    ext = file_path.suffix.lower()
                    stats['file_types'][ext] = stats['file_types'].get(ext, 0) + 1
                    
                    # Count by size category
                    if file_size < 1024:
                        stats['size_categories']['tiny'] += 1
                    elif file_size < 10240:
                        stats['size_categories']['small'] += 1
                    elif file_size < 1048576:
                        stats['size_categories']['medium'] += 1
                    elif file_size < 10485760:
                        stats['size_categories']['large'] += 1
                    else:
                        stats['size_categories']['huge'] += 1
                        
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        
        return stats
    
    def export_history(self, filename: str = 'organize_history.json'):
        """Export organization history to JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.organize_history, f, indent=2, default=str)
            
            print(f"History exported to {filename}")
            return True
            
        except Exception as e:
            print(f"Error exporting history: {e}")
            return False
    
    def export_stats(self, directory: str, filename: str = 'directory_stats.csv'):
        """Export directory statistics to CSV"""
        stats = self.get_directory_stats(directory)
        
        if not stats:
            return False
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['Statistic', 'Value'])
                
                # Write basic stats
                writer.writerow(['Total Files', stats['total_files']])
                writer.writerow(['Total Size', stats['total_size']])
                writer.writerow(['Total Size (MB)', stats['total_size'] / (1024*1024)])
                
                # Write size categories
                writer.writerow([])
                writer.writerow(['Size Category', 'Count'])
                for category, count in stats['size_categories'].items():
                    writer.writerow([category, count])
                
                # Write file types
                writer.writerow([])
                writer.writerow(['File Type', 'Count'])
                for file_type, count in stats['file_types'].items():
                    writer.writerow([file_type, count])
            
            print(f"Statistics exported to {filename}")
            return True
            
        except Exception as e:
            print(f"Error exporting statistics: {e}")
            return False

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"

def main():
    """Main function"""
    organizer = FileOrganizer()
    
    while True:
        print("\n=== File Organizer ===")
        print("1. Organize by Extension")
        print("2. Organize by Date")
        print("3. Organize by Size")
        print("4. Organize by Type")
        print("5. Find Duplicates")
        print("6. Remove Duplicates")
        print("7. Get Directory Statistics")
        print("8. Export History")
        print("9. Export Statistics")
        print("10. Exit")
        
        choice = input("\nEnter your choice (1-10): ").strip()
        
        if choice == "1":
            source_dir = input("Source directory: ").strip()
            dest_dir = input("Destination directory (optional): ").strip() or None
            move = input("Move files instead of copy? (y/n): ").strip().lower() == 'y'
            
            stats = organizer.organize_by_extension(source_dir, dest_dir, move)
            print(f"\nOrganization complete:")
            for ext, count in stats.items():
                print(f"{ext}: {count} files")
        
        elif choice == "2":
            source_dir = input("Source directory: ").strip()
            dest_dir = input("Destination directory (optional): ").strip() or None
            move = input("Move files instead of copy? (y/n): ").strip().lower() == 'y'
            date_type = input("Date type (modified/created/accessed): ").strip() or 'modified'
            
            stats = organizer.organize_by_date(source_dir, dest_dir, move, date_type)
            print(f"\nOrganization complete:")
            for date, count in stats.items():
                print(f"{date}: {count} files")
        
        elif choice == "3":
            source_dir = input("Source directory: ").strip()
            dest_dir = input("Destination directory (optional): ").strip() or None
            move = input("Move files instead of copy? (y/n): ").strip().lower() == 'y'
            
            stats = organizer.organize_by_size(source_dir, dest_dir, move)
            print(f"\nOrganization complete:")
            for size_cat, count in stats.items():
                print(f"{size_cat}: {count} files")
        
        elif choice == "4":
            source_dir = input("Source directory: ").strip()
            dest_dir = input("Destination directory (optional): ").strip() or None
            move = input("Move files instead of copy? (y/n): ").strip().lower() == 'y'
            
            stats = organizer.organize_by_type(source_dir, dest_dir, move)
            print(f"\nOrganization complete:")
            for mime_type, count in stats.items():
                print(f"{mime_type}: {count} files")
        
        elif choice == "5":
            directory = input("Directory to scan for duplicates: ").strip()
            duplicates = organizer.find_duplicates(directory)
            
            if not duplicates:
                print("No duplicates found")
            else:
                print(f"\nFound {len(duplicates)} groups of duplicates:")
                for i, (file_hash, file_paths) in enumerate(duplicates.items(), 1):
                    print(f"\nGroup {i} ({len(file_paths)} files):")
                    for file_path in file_paths:
                        print(f"  {file_path}")
        
        elif choice == "6":
            directory = input("Directory to remove duplicates from: ").strip()
            dry_run = input("Dry run (show what would be removed)? (y/n): ").strip().lower() == 'y'
            
            removed = organizer.remove_duplicates(directory, dry_run)
            if dry_run:
                print(f"Would remove {removed} duplicate files")
            else:
                print(f"Removed {removed} duplicate files")
        
        elif choice == "7":
            directory = input("Directory to analyze: ").strip()
            stats = organizer.get_directory_stats(directory)
            
            if stats:
                print(f"\nDirectory Statistics for {directory}:")
                print(f"Total Files: {stats['total_files']}")
                print(f"Total Size: {format_file_size(stats['total_size'])}")
                
                print("\nSize Categories:")
                for category, count in stats['size_categories'].items():
                    print(f"  {category}: {count} files")
                
                print("\nFile Types (top 10):")
                sorted_types = sorted(stats['file_types'].items(), key=lambda x: x[1], reverse=True)[:10]
                for file_type, count in sorted_types:
                    print(f"  {file_type or 'no_extension'}: {count} files")
        
        elif choice == "8":
            filename = input("Export filename (default: organize_history.json): ").strip()
            filename = filename or 'organize_history.json'
            organizer.export_history(filename)
        
        elif choice == "9":
            directory = input("Directory to export stats from: ").strip()
            filename = input("Export filename (default: directory_stats.csv): ").strip()
            filename = filename or 'directory_stats.csv'
            organizer.export_stats(directory, filename)
        
        elif choice == "10":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
