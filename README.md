# Currency Converter from Tenge

A Python application with a Tkinter GUI for converting KZT (Kazakhstani Tenge) to other currencies using real-time exchange rates, with automatic caching and logging.

## Features

- Convert amounts from KZT to any available currency
- Fetch exchange rates from an external API
- Use cached data when offline
- Log all operations
- Graphical user interface


The JSON file contains the response from the ExchangeRate-API, specifically the exchange rate data relative to KZT.
Used API: API_URL = "https://api.exchangerate-api.com/v4/latest/KZT"
Code includes comments for clarity.

## Dependencies

- Python 3.7 и больше
- `requests`

## Installation

1. Install dependencies:
   pip install requests
2. Run the application:
   python main.py
