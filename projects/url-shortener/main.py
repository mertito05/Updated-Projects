import sqlite3
import hashlib
import string
import random
from urllib.parse import urlparse
import validators

class URLShortener:
    def __init__(self, db_name='url_shortener.db'):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        """Initialize the database"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # Create URLs table
        c.execute('''CREATE TABLE IF NOT EXISTS urls
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      original_url TEXT NOT NULL,
                      short_code TEXT UNIQUE NOT NULL,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      clicks INTEGER DEFAULT 0)''')
        
        # Create analytics table
        c.execute('''CREATE TABLE IF NOT EXISTS analytics
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      short_code TEXT NOT NULL,
                      click_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      ip_address TEXT,
                      user_agent TEXT,
                      referrer TEXT)''')
        
        conn.commit()
        conn.close()
    
    def is_valid_url(self, url):
        """Check if URL is valid"""
        return validators.url(url)
    
    def generate_short_code(self, url, length=6):
        """Generate a short code for the URL"""
        # Use hash of URL plus random characters for uniqueness
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=length-4))
        return url_hash[:4] + random_chars
    
    def shorten_url(self, original_url, custom_code=None):
        """Shorten a URL"""
        if not self.is_valid_url(original_url):
            return None, "Invalid URL"
        
        if custom_code:
            # Check if custom code is available
            if self.get_original_url(custom_code):
                return None, "Custom code already exists"
            short_code = custom_code
        else:
            # Generate unique short code
            while True:
                short_code = self.generate_short_code(original_url)
                if not self.get_original_url(short_code):
                    break
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        try:
            c.execute('INSERT INTO urls (original_url, short_code) VALUES (?, ?)',
                      (original_url, short_code))
            conn.commit()
            return short_code, None
        except sqlite3.IntegrityError:
            return None, "Short code already exists"
        finally:
            conn.close()
    
    def get_original_url(self, short_code):
        """Get original URL from short code"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
        result = c.fetchone()
        
        conn.close()
        return result[0] if result else None
    
    def record_click(self, short_code, ip_address=None, user_agent=None, referrer=None):
        """Record a click for analytics"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # Update click count
        c.execute('UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?', (short_code,))
        
        # Record analytics
        c.execute('''INSERT INTO analytics (short_code, ip_address, user_agent, referrer)
                     VALUES (?, ?, ?, ?)''',
                  (short_code, ip_address, user_agent, referrer))
        
        conn.commit()
        conn.close()
    
    def get_click_stats(self, short_code):
        """Get click statistics for a short URL"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # Get total clicks
        c.execute('SELECT clicks FROM urls WHERE short_code = ?', (short_code,))
        total_clicks = c.fetchone()[0] if c.fetchone() else 0
        
        # Get recent clicks (last 24 hours)
        c.execute('''SELECT COUNT(*) FROM analytics 
                     WHERE short_code = ? AND click_time > datetime('now', '-1 day')''',
                  (short_code,))
        daily_clicks = c.fetchone()[0]
        
        conn.close()
        return total_clicks, daily_clicks
    
    def get_all_urls(self):
        """Get all shortened URLs"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('SELECT short_code, original_url, clicks, created_at FROM urls ORDER BY created_at DESC')
        urls = c.fetchall()
        
        conn.close()
        return urls
    
    def delete_url(self, short_code):
        """Delete a shortened URL"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # Delete from both tables
        c.execute('DELETE FROM urls WHERE short_code = ?', (short_code,))
        c.execute('DELETE FROM analytics WHERE short_code = ?', (short_code,))
        
        conn.commit()
        conn.close()
        
        return c.rowcount > 0

def main():
    """Main function"""
    shortener = URLShortener()
    
    while True:
        print("\n=== URL Shortener ===")
        print("1. Shorten URL")
        print("2. Get original URL")
        print("3. View all URLs")
        print("4. Get click statistics")
        print("5. Delete URL")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            url = input("Enter URL to shorten: ").strip()
            custom_code = input("Enter custom short code (optional): ").strip()
            custom_code = custom_code if custom_code else None
            
            short_code, error = shortener.shorten_url(url, custom_code)
            if short_code:
                print(f"Shortened URL: http://localhost:5000/{short_code}")
            else:
                print(f"Error: {error}")
        
        elif choice == "2":
            short_code = input("Enter short code: ").strip()
            original_url = shortener.get_original_url(short_code)
            if original_url:
                print(f"Original URL: {original_url}")
            else:
                print("Short code not found")
        
        elif choice == "3":
            urls = shortener.get_all_urls()
            if urls:
                print("\nAll Shortened URLs:")
                print("-" * 80)
                for short_code, original_url, clicks, created_at in urls:
                    print(f"{short_code:8} -> {original_url:40} | Clicks: {clicks:3} | Created: {created_at}")
            else:
                print("No URLs shortened yet")
        
        elif choice == "4":
            short_code = input("Enter short code: ").strip()
            total_clicks, daily_clicks = shortener.get_click_stats(short_code)
            print(f"Total clicks: {total_clicks}")
            print(f"Daily clicks: {daily_clicks}")
        
        elif choice == "5":
            short_code = input("Enter short code to delete: ").strip()
            if shortener.delete_url(short_code):
                print("URL deleted successfully")
            else:
                print("URL not found")
        
        elif choice == "6":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
