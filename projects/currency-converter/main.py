import requests
import json
import os

API_KEY = "your_api_key_here"  # Replace with your ExchangeRate-API key
BASE_URL = "https://v6.exchangerate-api.com/v6"

def get_exchange_rates(base_currency):
    """Get exchange rates from the API"""
    try:
        url = f"{BASE_URL}/{API_KEY}/latest/{base_currency}"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        if data['result'] == 'success':
            return data['conversion_rates']
        else:
            print(f"API Error: {data.get('error-type', 'Unknown error')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return None
    except json.JSONDecodeError:
        print("Error parsing API response")
        return None

def convert_currency(amount, from_currency, to_currency, rates):
    """Convert currency using the provided rates"""
    if from_currency not in rates or to_currency not in rates:
        return None
    
    # Convert to USD first (base currency), then to target currency
    if from_currency == to_currency:
        return amount
    
    # Convert from source currency to base currency (USD)
    amount_in_base = amount / rates[from_currency]
    
    # Convert from base currency to target currency
    result = amount_in_base * rates[to_currency]
    
    return round(result, 2)

def get_currency_symbol(currency_code):
    """Get currency symbol for display"""
    symbols = {
        'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥', 'CNY': '¥',
        'INR': '₹', 'RUB': '₽', 'KRW': '₩', 'BRL': 'R$', 'MXN': '$',
        'CAD': '$', 'AUD': '$', 'NZD': '$', 'CHF': 'Fr', 'SEK': 'kr',
        'NOK': 'kr', 'DKK': 'kr', 'TRY': '₺', 'ZAR': 'R', 'HKD': '$'
    }
    return symbols.get(currency_code, currency_code)

def display_currencies(rates):
    """Display available currencies"""
    print("\nAvailable currencies:")
    currencies = list(rates.keys())
    for i in range(0, len(currencies), 5):
        print("  " + "  ".join(currencies[i:i+5]))

def main():
    """Main function"""
    print("Currency Converter")
    print("==================")
    
    # Check if API key is set
    if API_KEY == "your_api_key_here":
        print("\n⚠️  Please get a free API key from ExchangeRate-API:")
        print("https://www.exchangerate-api.com/")
        print("Replace 'your_api_key_here' in main.py with your actual API key")
        return
    
    base_currency = "USD"  # Using USD as base currency for the API
    
    rates = get_exchange_rates(base_currency)
    if not rates:
        print("Could not fetch exchange rates. Please try again later.")
        return
    
    while True:
        print("\nOptions:")
        print("1. Convert currency")
        print("2. Show available currencies")
        print("3. Show current exchange rates")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            display_currencies(rates)
            
            from_curr = input("\nEnter source currency code: ").upper().strip()
            to_curr = input("Enter target currency code: ").upper().strip()
            
            if from_curr not in rates or to_curr not in rates:
                print("Invalid currency code(s)!")
                continue
            
            try:
                amount = float(input("Enter amount to convert: "))
                if amount <= 0:
                    print("Amount must be positive!")
                    continue
                
                result = convert_currency(amount, from_curr, to_curr, rates)
                if result is not None:
                    from_symbol = get_currency_symbol(from_curr)
                    to_symbol = get_currency_symbol(to_curr)
                    
                    print(f"\n{from_symbol}{amount:,.2f} {from_curr} = {to_symbol}{result:,.2f} {to_curr}")
                else:
                    print("Conversion failed!")
                    
            except ValueError:
                print("Please enter a valid number!")
        
        elif choice == "2":
            display_currencies(rates)
        
        elif choice == "3":
            print("\nCurrent Exchange Rates (based on USD):")
            print("=" * 40)
            for currency, rate in list(rates.items())[:20]:  # Show first 20 for brevity
                symbol = get_currency_symbol(currency)
                print(f"{symbol} {currency}: {rate:.4f}")
            
            if len(rates) > 20:
                print(f"... and {len(rates) - 20} more currencies")
        
        elif choice == "4":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

def get_free_rates():
    """Alternative function using free tier with limited currencies"""
    # This is a fallback option with hardcoded rates for demonstration
    # Note: These rates are examples and may not be current
    return {
        'USD': 1.0,    # US Dollar
        'EUR': 0.85,   # Euro
        'GBP': 0.75,   # British Pound
        'JPY': 110.0,  # Japanese Yen
        'CAD': 1.25,   # Canadian Dollar
        'AUD': 1.35,   # Australian Dollar
        'CHF': 0.92,   # Swiss Franc
        'CNY': 6.45,   # Chinese Yuan
        'INR': 74.0,   # Indian Rupee
        'BRL': 5.25,   # Brazilian Real
        'MXN': 20.0,   # Mexican Peso
        'RUB': 73.5,   # Russian Ruble
        'KRW': 1180.0, # South Korean Won
        'TRY': 8.5,    # Turkish Lira
        'ZAR': 14.5,   # South African Rand
        'NZD': 1.45,   # New Zealand Dollar
        'SEK': 8.7,    # Swedish Krona
        'NOK': 8.9,    # Norwegian Krone
        'DKK': 6.3,    # Danish Krone
        'HKD': 7.8     # Hong Kong Dollar
    }

if __name__ == "__main__":
    main()
