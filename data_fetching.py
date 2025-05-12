import requests
import pandas as pd
from config import start_date, end_date, FRED_API_KEY

def fetch_fred_series(series_id):
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': series_id,
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'observation_start': start_date,
        'observation_end': end_date
    }
    response = requests.get(url, params=params)
    data = response.json().get('observations', [])
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date']).dt.date
    df[series_id] = pd.to_numeric(df['value'], errors='coerce')
    return df[['date', series_id]].dropna()

