# Blog Platform

A simple web-based blog platform built with Flask and SQLite that allows users to create, read, and manage blog posts.

## Features
- **Create Posts**: Write and publish blog posts with titles, content, and author information
- **View Posts**: Browse all posts on the homepage with excerpts
- **Post Details**: Read full blog posts with proper formatting
- **Responsive Design**: Clean, modern interface that works on desktop and mobile devices
- **Database Storage**: All posts are stored in a SQLite database
- **Navigation**: Easy navigation between different sections of the blog

## Prerequisites
- Python 3.x
- Flask web framework
- SQLite (included with Python)

## Installation
```bash
pip install flask
```

## How to Run
1. Navigate to the project directory:
   ```bash
   cd projects/blog-platform
   ```

2. Run the Flask application:
   ```bash
   python main.py
   ```

3. Open your web browser and go to:
   ```
   http://localhost:5000
   ```

## Usage
1. **Home Page**: View all blog posts in reverse chronological order
2. **Create Post**: Click "Create Post" to write a new blog entry
3. **Read Posts**: Click on any post title to read the full content
4. **About Page**: Learn more about the blog platform

## File Structure
```
blog-platform/
├── main.py              # Main Flask application
├── blog.db              # SQLite database (created automatically)
├── templates/           # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── index.html       # Homepage with all posts
│   ├── post_detail.html # Individual post view
│   ├── create_post.html # Create new post form
│   └── about.html       # About page
├── static/              # Static files
│   └── style.css        # CSS stylesheet
└── requirements.txt     # Python dependencies
```

## API Endpoints
- `GET /` - Homepage with all posts
- `GET /post/<post_id>` - View individual post
- `GET /create` - Create new post form
- `POST /create` - Submit new post
- `GET /about` - About page

## Database Schema
The application uses a SQLite database with the following table:
```sql
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    author TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Customization
You can extend the platform by:
- Adding user authentication and authorization
- Implementing post categories and tags
- Adding comment functionality
- Including image uploads for posts
- Adding search functionality
- Implementing pagination for posts

## Security Considerations
- This is a basic implementation without user authentication
- For production use, implement proper security measures
- Consider using a more robust database system for production

## Troubleshooting
- Ensure Flask is installed correctly
- Check that port 5000 is available
- Verify database file permissions if issues occur

## Note
This project is intended for educational purposes and can be expanded with additional features for production use.
