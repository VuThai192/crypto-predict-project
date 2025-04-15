import pandas as pd

class DataProcessor:
    def __init__(self, symbol='', interval='30m'):
        self.symbol = symbol
        self.interval = interval
        
    def get_latest_data(self):
        """Load dữ liệu mới nhất từ file CSV"""
        path = f"data/raw/{self.symbol}_{self.interval}.csv"
        return pd.read_csv(path, parse_dates=['timestamp'])