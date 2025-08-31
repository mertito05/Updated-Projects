import requests
import json
import csv
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class StockTracker:
    def __init__(self, api_key=None):
        self.api_key = api_key or "demo"  # Use demo key by default
        self.base_url = "https://www.alphavantage.co/query"
        self.cache_file = "stock_cache.json"
        self.load_cache()
    
    def load_cache(self):
        """Load cached stock data"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    self.cache = json.load(f)
            else:
                self.cache = {}
        except:
            self.cache = {}
    
    def save_cache(self):
        """Save stock data to cache"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def get_stock_quote(self, symbol):
        """Get current stock quote"""
        if symbol in self.cache and 'quote' in self.cache[symbol]:
            cached_data = self.cache[symbol]['quote']
            # Check if cache is recent (less than 5 minutes old)
            cache_time = datetime.fromisoformat(cached_data['cache_time'])
            if datetime.now() - cache_time < timedelta(minutes=5):
                return cached_data['data']
        
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'Global Quote' in data:
                quote_data = data['Global Quote']
                cached_quote = {
                    'data': quote_data,
                    'cache_time': datetime.now().isoformat()
                }
                
                if symbol not in self.cache:
                    self.cache[symbol] = {}
                self.cache[symbol]['quote'] = cached_quote
                self.save_cache()
                
                return quote_data
            else:
                print(f"Error: {data.get('Note', 'Unknown error')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching stock quote: {e}")
            return None
    
    def get_historical_data(self, symbol, output_size='compact'):
        """Get historical stock data"""
        cache_key = f"historical_{output_size}"
        
        if symbol in self.cache and cache_key in self.cache[symbol]:
            cached_data = self.cache[symbol][cache_key]
            # Check if cache is recent (less than 1 hour old)
            cache_time = datetime.fromisoformat(cached_data['cache_time'])
            if datetime.now() - cache_time < timedelta(hours=1):
                return cached_data['data']
        
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': output_size,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'Time Series (Daily)' in data:
                historical_data = data['Time Series (Daily)']
                cached_historical = {
                    'data': historical_data,
                    'cache_time': datetime.now().isoformat()
                }
                
                if symbol not in self.cache:
                    self.cache[symbol] = {}
                self.cache[symbol][cache_key] = cached_historical
                self.save_cache()
                
                return historical_data
            else:
                print(f"Error: {data.get('Note', 'Unknown error')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching historical data: {e}")
            return None
    
    def display_quote(self, symbol):
        """Display current stock quote"""
        quote = self.get_stock_quote(symbol)
        if quote:
            print(f"\n=== {symbol} Stock Quote ===")
            print(f"Price: ${float(quote['05. price']):.2f}")
            print(f"Change: ${float(quote['09. change']):.2f}")
            print(f"Change %: {float(quote['10. change percent'].rstrip('%')):.2f}%")
            print(f"Volume: {int(quote['06. volume']):,}")
            print(f"Latest trading day: {quote['07. latest trading day']}")
        else:
            print(f"Could not fetch quote for {symbol}")
    
    def display_historical_summary(self, symbol):
        """Display historical data summary"""
        data = self.get_historical_data(symbol, 'compact')
        if data:
            dates = sorted(data.keys(), reverse=True)[:10]  # Last 10 days
            print(f"\n=== {symbol} Recent Prices ===")
            for date in dates:
                daily_data = data[date]
                print(f"{date}: ${float(daily_data['4. close']):.2f}")
    
    def plot_stock_chart(self, symbol, days=30):
        """Plot stock price chart"""
        data = self.get_historical_data(symbol, 'compact')
        if data:
            dates = []
            prices = []
            
            for date, daily_data in sorted(data.items()):
                if len(dates) >= days:
                    break
                dates.append(date)
                prices.append(float(daily_data['4. close']))
            
            # Reverse to show chronological order
            dates.reverse()
            prices.reverse()
            
            plt.figure(figsize=(12, 6))
            plt.plot(dates, prices, marker='o', linestyle='-')
            plt.title(f'{symbol} Stock Price - Last {days} Days')
            plt.xlabel('Date')
            plt.ylabel('Price ($)')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        else:
            print(f"Could not fetch data for {symbol}")
    
    def calculate_metrics(self, symbol):
        """Calculate basic financial metrics"""
        data = self.get_historical_data(symbol, 'compact')
        if data:
            closes = [float(daily_data['4. close']) for daily_data in data.values()]
            volumes = [int(daily_data['5. volume']) for daily_data in data.values()]
            
            # Basic statistics
            avg_price = np.mean(closes)
            max_price = max(closes)
            min_price = min(closes)
            avg_volume = np.mean(volumes)
            
            print(f"\n=== {symbol} Metrics ===")
            print(f"Average Price: ${avg_price:.2f}")
            print(f"Max Price: ${max_price:.2f}")
            print(f"Min Price: ${min_price:.2f}")
            print(f"Average Volume: {avg_volume:,.0f}")
    
    def export_to_csv(self, symbol, filename=None):
        """Export historical data to CSV"""
        data = self.get_historical_data(symbol, 'full')
        if data:
            if not filename:
                filename = f"{symbol}_historical_data.csv"
            
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for date, daily_data in sorted(data.items(), reverse=True):
                    writer.writerow({
                        'Date': date,
                        'Open': daily_data['1. open'],
                        'High': daily_data['2. high'],
                        'Low': daily_data['3. low'],
                        'Close': daily_data['4. close'],
                        'Volume': daily_data['5. volume']
                    })
            
            print(f"Data exported to {filename}")
        else:
            print(f"Could not fetch data for {symbol}")

def main():
    """Main function"""
    print("Stock Market Tracker")
    print("====================")
    
    # Check for API key
    api_key = os.environ.get('ALPHAVANTAGE_API_KEY')
    if not api_key:
        print("⚠️  Using demo API key (limited requests)")
        print("Get a free API key from: https://www.alphavantage.co/support/#api-key")
        api_key = "demo"
    
    tracker = StockTracker(api_key)
    
    while True:
        print("\nOptions:")
        print("1. Get stock quote")
        print("2. View historical data")
        print("3. Plot stock chart")
        print("4. Calculate metrics")
        print("5. Export to CSV")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            symbol = input("Enter stock symbol (e.g., AAPL, MSFT, GOOGL): ").upper()
            tracker.display_quote(symbol)
        
        elif choice == "2":
            symbol = input("Enter stock symbol: ").upper()
            tracker.display_historical_summary(symbol)
        
        elif choice == "3":
            symbol = input("Enter stock symbol: ").upper()
            try:
                days = int(input("Number of days to plot (default 30): ") or "30")
                tracker.plot_stock_chart(symbol, days)
            except ValueError:
                print("Invalid number of days")
        
        elif choice == "4":
            symbol = input("Enter stock symbol: ").upper()
            tracker.calculate_metrics(symbol)
        
        elif choice == "5":
            symbol = input("Enter stock symbol: ").upper()
            filename = input("Enter output filename (optional): ").strip()
            tracker.export_to_csv(symbol, filename or None)
        
        elif choice == "6":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
