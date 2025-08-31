import sqlite3
import json
from datetime import datetime
import markdown
import os
from typing import List, Dict, Optional

class SimpleBlogPlatform:
    def __init__(self, db_name='blog.db'):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        """Initialize the database"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # Create posts table
        c.execute('''CREATE TABLE IF NOT EXISTS posts
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      content TEXT NOT NULL,
                      author TEXT NOT NULL,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      published BOOLEAN DEFAULT FALSE,
                      slug TEXT UNIQUE NOT NULL)''')
        
        # Create categories table
        c.execute('''CREATE TABLE IF NOT EXISTS categories
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT UNIQUE NOT NULL,
                      description TEXT)''')
        
        # Create post_categories junction table
        c.execute('''CREATE TABLE IF NOT EXISTS post_categories
                     (post_id INTEGER,
                      category_id INTEGER,
                      PRIMARY KEY (post_id, category_id),
                      FOREIGN KEY (post_id) REFERENCES posts (id),
                      FOREIGN KEY (category_id) REFERENCES categories (id))''')
        
        # Create comments table
        c.execute('''CREATE TABLE IF NOT EXISTS comments
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      post_id INTEGER,
                      author TEXT NOT NULL,
                      content TEXT NOT NULL,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      approved BOOLEAN DEFAULT FALSE,
                      FOREIGN KEY (post_id) REFERENCES posts (id))''')
        
        conn.commit()
        conn.close()
    
    def generate_slug(self, title: str) -> str:
        """Generate a URL-friendly slug from title"""
        import re
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        slug = re.sub(r'^-+|-+$', '', slug)
        return slug
    
    def create_post(self, title: str, content: str, author: str, 
                   categories: List[str] = None, published: bool = False) -> Optional[int]:
        """Create a new blog post"""
        if not title or not content or not author:
            print("Title, content, and author are required")
            return None
        
        slug = self.generate_slug(title)
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        try:
            # Insert the post
            c.execute('''INSERT INTO posts (title, content, author, published, slug)
                         VALUES (?, ?, ?, ?, ?)''',
                      (title, content, author, published, slug))
            
            post_id = c.lastrowid
            
            # Add categories if provided
            if categories:
                for category_name in categories:
                    category_id = self.get_or_create_category(category_name)
                    if category_id:
                        c.execute('INSERT INTO post_categories (post_id, category_id) VALUES (?, ?)',
                                  (post_id, category_id))
            
            conn.commit()
            print(f"Post created successfully (ID: {post_id})")
            return post_id
            
        except sqlite3.IntegrityError:
            print("Slug already exists. Please choose a different title.")
            return None
        finally:
            conn.close()
    
    def update_post(self, post_id: int, **kwargs) -> bool:
        """Update a blog post"""
        allowed_fields = ['title', 'content', 'author', 'published']
        update_fields = []
        update_values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                update_fields.append(f"{field} = ?")
                update_values.append(value)
        
        if not update_fields:
            print("No valid fields to update")
            return False
        
        # If title is being updated, generate new slug
        if 'title' in kwargs:
            new_slug = self.generate_slug(kwargs['title'])
            update_fields.append("slug = ?")
            update_values.append(new_slug)
        
        update_values.append(datetime.now().isoformat())
        update_values.append(post_id)
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        try:
            query = f'''UPDATE posts 
                       SET {', '.join(update_fields)}, updated_at = ?
                       WHERE id = ?'''
            c.execute(query, update_values)
            
            if c.rowcount == 0:
                print("Post not found")
                return False
            
            conn.commit()
            print("Post updated successfully")
            return True
            
        except sqlite3.IntegrityError:
            print("Slug already exists. Please choose a different title.")
            return False
        finally:
            conn.close()
    
    def delete_post(self, post_id: int) -> bool:
        """Delete a blog post and its associated data"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        try:
            # Delete associated categories
            c.execute('DELETE FROM post_categories WHERE post_id = ?', (post_id,))
            
            # Delete associated comments
            c.execute('DELETE FROM comments WHERE post_id = ?', (post_id,))
            
            # Delete the post
            c.execute('DELETE FROM posts WHERE id = ?', (post_id,))
            
            if c.rowcount == 0:
                print("Post not found")
                return False
            
            conn.commit()
            print("Post deleted successfully")
            return True
            
        finally:
            conn.close()
    
    def get_post(self, post_id: int = None, slug: str = None) -> Optional[Dict]:
        """Get a specific post by ID or slug"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        if post_id:
            c.execute('''SELECT p.*, GROUP_CONCAT(c.name, ', ') as categories
                         FROM posts p
                         LEFT JOIN post_categories pc ON p.id = pc.post_id
                         LEFT JOIN categories c ON pc.category_id = c.id
                         WHERE p.id = ?
                         GROUP BY p.id''', (post_id,))
        elif slug:
            c.execute('''SELECT p.*, GROUP_CONCAT(c.name, ', ') as categories
                         FROM posts p
                         LEFT JOIN post_categories pc ON p.id = pc.post_id
                         LEFT JOIN categories c ON pc.category_id = c.id
                         WHERE p.slug = ?
                         GROUP BY p.id''', (slug,))
        else:
            conn.close()
            return None
        
        row = c.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            'id': row[0],
            'title': row[1],
            'content': row[2],
            'author': row[3],
            'created_at': row[4],
            'updated_at': row[5],
            'published': bool(row[6]),
            'slug': row[7],
            'categories': row[8] if row[8] else ''
        }
    
    def get_posts(self, published_only: bool = True, category: str = None, 
                 limit: int = None, offset: int = 0) -> List[Dict]:
        """Get multiple posts with optional filtering"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        query = '''SELECT p.*, GROUP_CONCAT(c.name, ', ') as categories
                   FROM posts p
                   LEFT JOIN post_categories pc ON p.id = pc.post_id
                   LEFT JOIN categories c ON pc.category_id = c.id'''
        
        conditions = []
        params = []
        
        if published_only:
            conditions.append('p.published = TRUE')
        
        if category:
            conditions.append('c.name = ?')
            params.append(category)
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        
        query += ' GROUP BY p.id ORDER BY p.created_at DESC'
        
        if limit:
            query += ' LIMIT ? OFFSET ?'
            params.extend([limit, offset])
        
        c.execute(query, params)
        posts = []
        
        for row in c.fetchall():
            post = {
                'id': row[0],
                'title': row[1],
                'content': row[2],
                'author': row[3],
                'created_at': row[4],
                'updated_at': row[5],
                'published': bool(row[6]),
                'slug': row[7],
                'categories': row[8] if row[8] else ''
            }
            posts.append(post)
        
        conn.close()
        return posts
    
    def get_or_create_category(self, category_name: str) -> Optional[int]:
        """Get category ID or create if it doesn't exist"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('SELECT id FROM categories WHERE name = ?', (category_name,))
        row = c.fetchone()
        
        if row:
            category_id = row[0]
        else:
            c.execute('INSERT INTO categories (name) VALUES (?)', (category_name,))
            category_id = c.lastrowid
            conn.commit()
        
        conn.close()
        return category_id
    
    def get_categories(self) -> List[Dict]:
        """Get all categories with post counts"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('''SELECT c.id, c.name, c.description, COUNT(pc.post_id) as post_count
                     FROM categories c
                     LEFT JOIN post_categories pc ON c.id = pc.category_id
                     GROUP BY c.id
                     ORDER BY c.name''')
        
        categories = []
        for row in c.fetchall():
            categories.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'post_count': row[3]
            })
        
        conn.close()
        return categories
    
    def add_comment(self, post_id: int, author: str, content: str, approved: bool = False) -> Optional[int]:
        """Add a comment to a post"""
        if not author or not content:
            print("Author and content are required")
            return None
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        try:
            c.execute('''INSERT INTO comments (post_id, author, content, approved)
                         VALUES (?, ?, ?, ?)''',
                      (post_id, author, content, approved))
            
            comment_id = c.lastrowid
            conn.commit()
            print("Comment added successfully")
            return comment_id
            
        finally:
            conn.close()
    
    def get_comments(self, post_id: int, approved_only: bool = True) -> List[Dict]:
        """Get comments for a post"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        query = 'SELECT * FROM comments WHERE post_id = ?'
        params = [post_id]
        
        if approved_only:
            query += ' AND approved = TRUE'
        
        query += ' ORDER BY created_at DESC'
        
        c.execute(query, params)
        comments = []
        
        for row in c.fetchall():
            comments.append({
                'id': row[0],
                'post_id': row[1],
                'author': row[2],
                'content': row[3],
                'created_at': row[4],
                'approved': bool(row[5])
            })
        
        conn.close()
        return comments
    
    def approve_comment(self, comment_id: int) -> bool:
        """Approve a comment"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('UPDATE comments SET approved = TRUE WHERE id = ?', (comment_id,))
        
        if c.rowcount == 0:
            print("Comment not found")
            conn.close()
            return False
        
        conn.commit()
        conn.close()
        print("Comment approved")
        return True
    
    def delete_comment(self, comment_id: int) -> bool:
        """Delete a comment"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
        
        if c.rowcount == 0:
            print("Comment not found")
            conn.close()
            return False
        
        conn.commit()
        conn.close()
        print("Comment deleted")
        return True
    
    def export_posts(self, filename: str = 'blog_export.json'):
        """Export all posts to JSON"""
        posts = self.get_posts(published_only=False)
        
        export_data = []
        for post in posts:
            post_data = post.copy()
            # Get comments for each post
            post_data['comments'] = self.get_comments(post['id'], approved_only=False)
            export_data.append(post_data)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            print(f"Posts exported to {filename}")
            return True
            
        except Exception as e:
            print(f"Error exporting posts: {e}")
            return False
    
    def import_posts(self, filename: str):
        """Import posts from JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            imported_count = 0
            for post_data in import_data:
                # Create the post
                post_id = self.create_post(
                    title=post_data['title'],
                    content=post_data['content'],
                    author=post_data['author'],
                    published=post_data['published'],
                    categories=post_data['categories'].split(', ') if post_data['categories'] else []
                )
                
                if post_id:
                    imported_count += 1
                    # Import comments
                    for comment in post_data.get('comments', []):
                        self.add_comment(
                            post_id=post_id,
                            author=comment['author'],
                            content=comment['content'],
                            approved=comment['approved']
                        )
            
            print(f"Imported {imported_count} posts")
            return True
            
        except FileNotFoundError:
            print("File not found")
            return False
        except Exception as e:
            print(f"Error importing posts: {e}")
            return False

def display_post(post: Dict):
    """Display a post in a formatted way"""
    print(f"\n=== {post['title']} ===")
    print(f"ID: {post['id']}")
    print(f"Author: {post['author']}")
    print(f"Published: {'Yes' if post['published'] else 'No'}")
    print(f"Slug: {post['slug']}")
    if post['categories']:
        print(f"Categories: {post['categories']}")
    print(f"Created: {post['created_at']}")
    print(f"Updated: {post['updated_at']}")
    print(f"\nContent:\n{post['content'][:200]}..." if len(post['content']) > 200 else post['content'])

def main():
    """Main function"""
    blog = SimpleBlogPlatform()
    
    while True:
        print("\n=== Simple Blog Platform ===")
        print("1. Create Post")
        print("2. Update Post")
        print("3. Delete Post")
        print("4. View Post")
        print("5. List Posts")
        print("6. List Categories")
        print("7. Add Comment")
        print("8. View Comments")
        print("9. Moderate Comments")
        print("10. Export Posts")
        print("11. Import Posts")
        print("12. Exit")
        
        choice = input("\nEnter your choice (1-12): ").strip()
        
        if choice == "1":
            print("\nCreate New Post")
            title = input("Title: ").strip()
            content = input("Content: ").strip()
            author = input("Author: ").strip()
            categories = input("Categories (comma-separated): ").strip()
            published = input("Publish? (y/n): ").strip().lower() == 'y'
            
            category_list = [cat.strip() for cat in categories.split(',')] if categories else []
            blog.create_post(title, content, author, category_list, published)
        
        elif choice == "2":
            post_id = input("Enter Post ID to update: ").strip()
            if not post_id.isdigit():
                print("Invalid post ID")
                continue
            
            post = blog.get_post(int(post_id))
            if not post:
                print("Post not found")
                continue
            
            print("\nLeave field blank to keep current value")
            updates = {}
            
            title = input(f"Title ({post['title']}): ").strip()
            if title: updates['title'] = title
            
            content = input(f"Content ({post['content'][:50]}...): ").strip()
            if content: updates['content'] = content
            
            author = input(f"Author ({post['author']}): ").strip()
            if author: updates['author'] = author
            
            published = input(f"Published ({post['published']}): ").strip()
            if published.lower() in ['y', 'yes', 'true']:
                updates['published'] = True
            elif published.lower() in ['n', 'no', 'false']:
                updates['published'] = False
            
            if updates:
                blog.update_post(int(post_id), **updates)
            else:
                print("No changes made")
        
        elif choice == "3":
            post_id = input("Enter Post ID to delete: ").strip()
            if not post_id.isdigit():
                print("Invalid post ID")
                continue
            
            confirm = input("Are you sure? This will delete all comments too. (y/n): ").strip().lower()
            if confirm == 'y':
                blog.delete_post(int(post_id))
        
        elif choice == "4":
            post_id = input("Enter Post ID or slug: ").strip()
            if post_id.isdigit():
                post = blog.get_post(post_id=int(post_id))
            else:
                post = blog.get_post(slug=post_id)
            
            if post:
                display_post(post)
            else:
                print("Post not found")
        
        elif choice == "5":
            published_only = input("Show only published posts? (y/n): ").strip().lower() != 'n'
            category = input("Filter by category (leave blank for all): ").strip() or None
            limit = input("Limit (default 10): ").strip()
            limit = int(limit) if limit.isdigit() else 10
            
            posts = blog.get_posts(published_only, category, limit)
            
            if not posts:
                print("No posts found")
                continue
            
            print(f"\nFound {len(posts)} posts:")
            for post in posts:
                status = "✓" if post['published'] else "✗"
                print(f"{status} {post['id']}: {post['title']} - {post['author']} "
                      f"({post['created_at']})")
        
        elif choice == "6":
            categories = blog.get_categories()
            
            if not categories:
                print("No categories found")
                continue
            
            print("\nCategories:")
            for cat in categories:
                print(f"{cat['name']} ({cat['post_count']} posts)")
                if cat['description']:
                    print(f"  {cat['description']}")
        
        elif choice == "7":
            post_id = input("Enter Post ID: ").strip()
            if not post_id.isdigit():
                print("Invalid post ID")
                continue
            
            author = input("Your name: ").strip()
            content = input("Comment: ").strip()
            
            blog.add_comment(int(post_id), author, content)
        
        elif choice == "8":
            post_id = input("Enter Post ID: ").strip()
            if not post_id.isdigit():
                print("Invalid post ID")
                continue
            
            comments = blog.get_comments(int(post_id))
            
            if not comments:
                print("No comments found")
                continue
            
            print(f"\nComments for post {post_id}:")
            for comment in comments:
                status = "✓" if comment['approved'] else "✗"
                print(f"{status} {comment['author']}: {comment['content']} "
                      f"({comment['created_at']})")
        
        elif choice == "9":
            print("\nComment Moderation")
            print("1. Approve comment")
            print("2. Delete comment")
            
            mod_choice = input("Enter choice (1-2): ").strip()
            
            if mod_choice == "1":
                comment_id = input("Enter Comment ID to approve: ").strip()
                if comment_id.isdigit():
                    blog.approve_comment(int(comment_id))
                else:
                    print("Invalid comment ID")
            
            elif mod_choice == "2":
                comment_id = input("Enter Comment ID to delete: ").strip()
                if comment_id.isdigit():
                    blog.delete_comment(int(comment_id))
                else:
                    print("Invalid comment ID")
            
            else:
                print("Invalid choice")
        
        elif choice == "10":
            filename = input("Export filename (default: blog_export.json): ").strip()
            filename = filename or 'blog_export.json'
            blog.export_posts(filename)
        
        elif choice == "11":
            filename = input("Import filename: ").strip()
            if filename:
                blog.import_posts(filename)
        
        elif choice == "12":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
