# Contact Management System

A comprehensive command-line contact management application built with Python and SQLite. This system allows you to store, organize, and manage your contacts efficiently with features like tagging, searching, and data import/export.

## Features
- **Contact Management**: Add, update, and delete contacts with detailed information
- **Tagging System**: Organize contacts with custom tags for better categorization
- **Advanced Search**: Search contacts by name, email, company, or tags
- **Data Validation**: Validate email addresses and phone numbers
- **Import/Export**: Export contacts to CSV and import from CSV files
- **SQLite Database**: Lightweight and efficient data storage
- **Contact Details**: Store comprehensive contact information including:
  - Name (first and last)
  - Email address
  - Phone number
  - Physical address
  - Company and job title
  - Notes and additional information
  - Custom tags

## Prerequisites
- Python 3.x
- SQLite3 (included with Python)

## Installation
No additional packages required. The application uses Python's standard library.

## How to Run
```bash
python main.py
```

## Usage

### Adding Contacts
1. Choose option 1 from the main menu
2. Enter contact details (first name and last name are required)
3. Optional fields: email, phone, address, company, title, notes

### Managing Contacts
- **Update**: Modify existing contact information
- **Delete**: Remove contacts from the database
- **Search**: Find contacts by name, email, company, or tags
- **View Details**: Display complete contact information

### Tagging System
- **Add Tags**: Assign custom tags to contacts for organization
- **Remove Tags**: Remove tags from contacts
- **Filter by Tags**: Search and filter contacts by specific tags

### Data Management
- **Export**: Save all contacts to a CSV file
- **Import**: Load contacts from a CSV file (supports tags)

## Database Schema
The application uses three SQLite tables:

### Contacts Table
- `id`: Primary key
- `first_name`, `last_name`: Contact name
- `email`, `phone`: Contact information
- `address`, `company`, `title`: Additional details
- `notes`: Free-form notes
- `created_at`, `updated_at`: Timestamps

### Tags Table
- `id`: Primary key
- `name`: Tag name (unique)

### Contact_Tags Table
- Junction table linking contacts to tags
- `contact_id`: Foreign key to contacts
- `tag_id`: Foreign key to tags

## Data Validation
- **Email Validation**: Uses regex pattern matching for valid email formats
- **Phone Validation**: Basic format validation for phone numbers
- **Required Fields**: First name and last name are mandatory
- **Unique Constraints**: Email addresses must be unique

## CSV Import/Export
### Export Format
CSV files include all contact fields:
- id, first_name, last_name, email, phone, address, company, title, notes, tags

### Import Format
- Supports the same CSV format as export
- Tags should be comma-separated in the tags column
- First name and last name are required for import

## Search Functionality
- **Text Search**: Searches across first name, last name, email, and company fields
- **Tag Filtering**: Filter contacts by specific tags
- **Combined Search**: Combine text search with tag filtering

## Customization
You can extend the application by:
- Adding contact photos or avatars
- Implementing contact groups or categories
- Adding birthday and anniversary tracking
- Creating a web interface
- Adding email integration
- Implementing contact synchronization
- Adding duplicate detection
- Creating a graphical user interface

## Security Considerations
- No authentication system (single-user application)
- Data stored locally in SQLite database
- Input validation prevents malformed data
- No external data sharing

## Performance
- SQLite provides excellent performance for personal use
- Efficient indexing on frequently searched fields
- Optimized database queries
- Suitable for thousands of contacts

## File Structure
```
contact-management-system/
├── main.py          # Main application
├── contacts.db      # SQLite database (created automatically)
└── requirements.txt # Python dependencies (empty - uses standard library)
```

## Troubleshooting
- Ensure write permissions for database file creation
- Check CSV file encoding (UTF-8 recommended)
- Verify email and phone format during input
- Ensure sufficient disk space for database operations

## Backup Recommendations
- Regularly export contacts to CSV for backup
- Copy the SQLite database file for full backup
- Store backups in multiple locations

## Future Enhancements
- Web-based interface
- Mobile app version
- Cloud synchronization
- Contact sharing features
- Advanced search with filters
- Contact merging functionality
- Birthday reminders
- Email integration
- Social media linking
- Contact history tracking

## Legal Compliance
- Ensure compliance with data protection regulations (GDPR, CCPA, etc.)
- Implement proper data encryption if storing sensitive information
- Include data retention policies
- Add user consent mechanisms for data processing

## Support
For issues and feature requests, please check the application documentation or consult the source code comments.
