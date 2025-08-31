# Currency Converter

A command-line currency conversion application that uses real-time exchange rates from the ExchangeRate-API. This application allows users to convert between different currencies and view current exchange rates.

## Features
- **Real-time Exchange Rates**: Fetches current exchange rates from ExchangeRate-API
- **Currency Conversion**: Convert between 160+ world currencies
- **Currency Symbols**: Displays appropriate currency symbols for better readability
- **Available Currencies**: View list of all supported currencies
- **Exchange Rate Display**: Show current exchange rates for major currencies
- **Fallback Option**: Includes hardcoded rates for demonstration when API is unavailable

## Prerequisites
- Python 3.x
- Requests library for API calls
- Free ExchangeRate-API key

## Installation
```bash
pip install requests
```

## API Key Setup
1. Get a free API key from [ExchangeRate-API](https://www.exchangerate-api.com/)
2. Replace `your_api_key_here` in `main.py` with your actual API key

## How to Run
```bash
python main.py
```

## Usage
1. Start the application by running `main.py`.
2. Choose from the menu options:
   - **Convert currency**: Enter source and target currencies with amount
   - **Show available currencies**: View all supported currency codes
   - **Show current exchange rates**: Display current rates for major currencies
   - **Exit**: Quit the application

## Example
```
# Convert 100 USD to EUR
Enter source currency code: USD
Enter target currency code: EUR
Enter amount to convert: 100

$100.00 USD = €85.00 EUR
```

## Supported Currencies
The application supports 160+ currencies including:
- USD (US Dollar)
- EUR (Euro)
- GBP (British Pound)
- JPY (Japanese Yen)
- CAD (Canadian Dollar)
- AUD (Australian Dollar)
- CHF (Swiss Franc)
- CNY (Chinese Yuan)
- INR (Indian Rupee)
- And many more...

## API Information
- **Provider**: ExchangeRate-API
- **Free Tier**: 1,500 requests per month
- **Base Currency**: USD
- **Update Frequency**: Rates are updated every 24 hours

## Fallback Mode
If the API key is not configured, the application uses hardcoded exchange rates for demonstration purposes. These rates are examples and may not reflect current market rates.

## Security Considerations
- API keys should be kept secure and not shared publicly
- Consider using environment variables for API keys in production
- The application only makes read requests to the API

## Customization
You can extend the application by:
- Adding historical exchange rate data
- Implementing currency conversion charts
- Adding support for cryptocurrency conversions
- Creating a graphical user interface
- Adding currency rate alerts

## Troubleshooting
- Ensure you have an active internet connection for real-time rates
- Verify your API key is correct and active
- Check the ExchangeRate-API status if rates aren't updating

## Note
Exchange rates are provided by third-party APIs and may have usage limitations. For production use, consider using a paid API plan or implementing rate limiting.
