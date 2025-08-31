import requests
from bs4 import BeautifulSoup
import csv
import time
import os

def scrape_quotes():
    """Scrape quotes from quotes.toscrape.com and save to CSV"""
    base_url = "http://quotes.toscrape.com"
    url = base_url
    quotes_data = []
    page = 1
    
    print("Starting web scraping...")
    
    while url:
        try:
            print(f"Scraping page {page}...")
            
            # Send GET request
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all quote elements
            quotes = soup.find_all('div', class_='quote')
            
            for quote in quotes:
                text = quote.find('span', class_='text').get_text()
                author = quote.find('small', class_='author').get_text()
                tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
                
                quotes_data.append({
                    'text': text,
                    'author': author,
                    'tags': ', '.join(tags)
                })
            
            # Check for next page
            next_button = soup.find('li', class_='next')
            if next_button:
                next_page = next_button.find('a')['href']
                url = base_url + next_page
                page += 1
                time.sleep(1)  # Be polite and wait between requests
            else:
                url = None
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page: {e}")
            break
        except Exception as e:
            print(f"Error parsing page: {e}")
            break
    
    return quotes_data

def save_to_csv(quotes_data, filename='quotes.csv'):
    """Save scraped data to CSV file"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['text', 'author', 'tags']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for quote in quotes_data:
                writer.writerow(quote)
        
        print(f"Data saved to {filename}")
        print(f"Total quotes scraped: {len(quotes_data)}")
        
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def main():
    print("Web Scraper - Quotes from quotes.toscrape.com")
    print("=============================================")
    
    # Check if required packages are available
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("Please install required packages:")
        print("pip install requests beautifulsoup4")
        return
    
    # Scrape quotes
    quotes = scrape_quotes()
    
    if quotes:
        # Save to CSV
        save_to_csv(quotes)
        print("\nScraping completed successfully!")
    else:
        print("No quotes were scraped.")

if __name__ == "__main__":
    main()
