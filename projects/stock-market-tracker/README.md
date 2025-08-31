# Stock Market Tracker

A comprehensive stock market tracking application that provides real-time stock quotes, historical data analysis, and visualization using the Alpha Vantage API. This tool helps investors monitor stock performance and analyze market trends.

## Features
- **Real-time Quotes**: Get current stock prices and market data
- **Historical Data**: Access historical stock prices and volumes
- **Data Visualization**: Plot stock price charts using Matplotlib
- **Financial Metrics**: Calculate basic financial statistics
- **Data Export**: Export historical data to CSV format
- **Caching System**: Intelligent caching to minimize API calls
- **Multiple Stocks**: Track multiple stock symbols

## Prerequisites
- Python 3.x
- Alpha Vantage API key (free tier available)
- Required Python libraries: requests, matplotlib, pandas, numpy

## Installation
```bash
pip install requests matplotlib pandas numpy
```

## API Key Setup
1. Get a free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Set environment variable:
   ```bash
   export ALPHAVANTAGE_API_KEY=your_api_key_here
   ```
   Or replace "demo" in the code with your actual API key

## How to Run
```bash
python main.py
```

## Usage

### Getting Started
1. Run the application
2. Choose from the menu options:
   - Get stock quotes
   - View historical data
   - Plot charts
   - Calculate metrics
   - Export data

### Example Commands
- Get quote for Apple: `AAPL`
- Plot 30-day chart for Microsoft: `MSFT`
- Export Google data: `GOOGL`

## API Integration
Uses Alpha Vantage API endpoints:
- `GLOBAL_QUOTE`: Real-time stock quotes
- `TIME_SERIES_DAILY`: Historical daily data
- Free tier: 5 requests per minute, 500 requests per day

## Data Provided
- Current price and change
- Trading volume
- Daily open, high, low, close prices
- Historical price data
- Volume information

## Caching System
- Quotes cached for 5 minutes
- Historical data cached for 1 hour
- Reduces API calls and improves performance
- Persistent cache stored in JSON file

## Visualization Features
- Interactive line charts
- Customizable time periods
- Price trends analysis
- Technical analysis support

## Financial Metrics
- Average price calculation
- Maximum and minimum prices
- Volume analysis
- Basic statistical analysis

## Export Capabilities
- CSV format for easy analysis
- Compatible with Excel and other tools
- Full historical data export
- Custom filename support

## Customization
You can extend the application by:
- Adding technical indicators (RSI, MACD, etc.)
- Implementing portfolio tracking
- Adding alert notifications
- Creating a web interface
- Adding cryptocurrency support
- Implementing backtesting
- Adding fundamental data analysis

## Performance Considerations
- API rate limiting (5 requests/minute)
- Cache system reduces external calls
- Efficient data processing with pandas
- Memory management for large datasets

## Error Handling
- Network connection errors
- API rate limit exceeded
- Invalid stock symbols
- Data parsing errors
- Cache file corruption

## Security
- API key management
- Secure data storage
- Input validation
- Error logging

## File Structure
```
stock-market-tracker/
├── main.py          # Main application
├── stock_cache.json # Cached data (auto-generated)
└── requirements.txt # Python dependencies
```

## Troubleshooting

### Common Issues
1. **API Limit Exceeded**: Wait 1 minute between requests or upgrade API plan
2. **Invalid Symbol**: Verify stock symbol format (e.g., AAPL, not apple)
3. **No Data**: Check internet connection and API key validity
4. **Chart Not Displaying**: Ensure matplotlib is properly installed

### Demo Mode Limitations
- Limited to certain symbols
- Delayed data (15+ minutes)
- Reduced functionality
- Higher rate limits

## Future Enhancements
- Real-time streaming data
- Advanced technical analysis
- Portfolio management
- Alert system
- Mobile app version
- Social sentiment analysis
- Earnings calendar
- Dividend tracking
- Options chain data
- International markets support

## Legal Disclaimer
This application is for educational and informational purposes only. It is not financial advice. Always conduct your own research and consult with a qualified financial advisor before making investment decisions.

## Data Sources
- Alpha Vantage API: Real-time and historical market data
- Free tier available for personal use
- Professional plans for commercial use

## Support
For API-related issues, contact Alpha Vantage support. For application issues, check the troubleshooting section or consult the documentation.
