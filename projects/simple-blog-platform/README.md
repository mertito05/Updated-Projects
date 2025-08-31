# Simple Blog Platform

A command-line blog management system built with Python and SQLite. This platform allows you to create, manage, and publish blog posts with features like categories, comments, and content management.

## Features
- **Post Management**: Create, update, and delete blog posts
- **Category System**: Organize posts with custom categories
- **Comment System**: Allow readers to comment on posts with moderation
- **Slug Generation**: Automatic URL-friendly slug creation from post titles
- **Publishing Control**: Draft and publish states for posts
- **Import/Export**: Export posts to JSON and import from JSON files
- **Search and Filter**: Find posts by category or publication status
- **SQLite Database**: Lightweight and efficient data storage

## Prerequisites
- Python 3.x
- SQLite3 (included with Python)
- Python-Markdown (for optional Markdown support)

## Installation
```bash
pip install markdown
```

## How to Run
```bash
python main.py
```

## Usage

### Creating Posts
1. Choose option 1 from the main menu
2. Enter post details:
   - Title (required)
   - Content (required)
   - Author (required)
   - Categories (comma-separated, optional)
   - Publication status (y/n)

### Managing Posts
- **Update**: Modify existing post content and metadata
- **Delete**: Remove posts and their associated comments
- **View**: Display post details and content
- **List**: Browse posts with filtering options

### Comment System
- **Add Comments**: Readers can add comments to posts
- **Moderation**: Approve or delete comments
- **View Comments**: See all comments for a post

### Categories
- **Automatic Creation**: Categories are created automatically when used
- **Post Counts**: View how many posts are in each category
- **Filtering**: Filter posts by specific categories

## Database Schema
The application uses four SQLite tables:

### Posts Table
- `id`: Primary key
- `title`, `content`: Post content
- `author`: Post author
- `created_at`, `updated_at`: Timestamps
- `published`: Publication status
- `slug`: URL-friendly identifier

### Categories Table
- `id`: Primary key
- `name`: Category name (unique)
- `description`: Optional description

### Post_Categories Table
- Junction table linking posts to categories
- `post_id`: Foreign key to posts
- `category_id`: Foreign key to categories

### Comments Table
- `id`: Primary key
- `post_id`: Foreign key to posts
- `author`, `content`: Comment details
- `created_at`: Timestamp
- `approved`: Moderation status

## Content Management
- **Slug Generation**: Automatic conversion of titles to URL-friendly slugs
- **Content Validation**: Required fields enforcement
- **Timestamps**: Automatic tracking of creation and modification times
- **Publication Control**: Separate draft and published states

## Comment Moderation
- **Approval System**: Comments require approval before display
- **Moderation Tools**: Approve or delete comments individually
- **Comment Viewing**: See all comments for moderation

## Import/Export
### Export Format
JSON files include:
- Complete post data
- Associated comments
- Category information
- All metadata

### Import Format
- Supports the same JSON format as export
- Preserves post relationships
- Maintains comment threads

## Customization
You can extend the platform by:
- Adding Markdown support for content
- Implementing a web interface
- Adding user authentication
- Creating RSS feeds
- Adding image uploads
- Implementing search functionality
- Adding social sharing
- Creating a theme system
- Adding post scheduling
- Implementing analytics

## Security Considerations
- Input validation for all user inputs
- SQL injection protection through parameterized queries
- Comment moderation to prevent spam
- No authentication system (single-user application)

## Performance
- SQLite provides excellent performance for small to medium blogs
- Efficient database indexing
- Optimized queries for common operations
- Suitable for hundreds of posts and comments

## File Structure
```
simple-blog-platform/
├── main.py          # Main application
├── blog.db          # SQLite database (created automatically)
└── requirements.txt # Python dependencies
```

## Troubleshooting
- Ensure write permissions for database file creation
- Check that required fields are provided when creating posts
- Verify JSON file format during import/export
- Ensure sufficient disk space for database operations

## Backup Recommendations
- Regularly export posts to JSON for backup
- Copy the SQLite database file for full backup
- Store backups in multiple locations

## Future Enhancements
- Web-based administration interface
- Markdown editor integration
- User authentication system
- Post scheduling
- RSS feed generation
- Social media integration
- Image gallery support
- Search functionality
- Tagging system
- Post templates
- Analytics dashboard
- Email notifications
- Multi-user support
- Theme customization
- Mobile app version

## Content Management Best Practices
- Use descriptive titles for better SEO
- Organize content with relevant categories
- Moderate comments regularly
- Keep content updated and relevant
- Use consistent formatting
- Backup content regularly

## Legal Compliance
- Include privacy policy for comment data
- Implement GDPR compliance for EU users
- Add terms of service
- Include copyright notices
- Implement data retention policies

## Support
For issues and feature requests, please check the application documentation or consult the source code comments. The platform is designed to be extensible and can be customized to fit specific needs.
