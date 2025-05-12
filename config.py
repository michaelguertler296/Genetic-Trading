import datetime

# Model Configuration
FRED_API_KEY = '6bc36d2b4bdf3faa81193c774871d354' # Guertler API Key for FRED

# Date Range for Data Fetching
end_date = datetime.datetime.now().date()
start_date = end_date - datetime.timedelta(days=365) # 1 year of data