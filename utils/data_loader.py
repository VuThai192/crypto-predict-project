import pandas as pd
from ta import add_all_ta_features  # Thư viện technical analysis
from ta.momentum import RSIIndicator  # Thêm import RSI

class DataProcessor:
    def __init__(self, symbol='', interval='30m'):
        self.symbol = symbol
        self.interval = interval
        
    def get_latest_data(self):
        """Load dữ liệu mới nhất từ file CSV"""
        
        if self.symbol != '':
            path = f"data/raw/{self.symbol}_{self.interval}.csv"
            return pd.read_csv(path, parse_dates=['timestamp'])
        return
    
    def load_and_preprocess(self):
        path = f"data/raw/{self.symbol}_{self.interval}.csv"
        df = pd.read_csv(path)
        # Thêm RSI thủ công nếu cần
        df['rsi'] = RSIIndicator(df['close'], window=14).rsi()
        # Thêm technical indicators
        df = add_all_ta_features(
            df, 
            open="open", 
            high="high", 
            low="low", 
            close="close", 
            volume="volume"
        )
        
        # Xử lý missing values
        df.fillna(method='ffill', inplace=True)
        
        # Chuẩn hóa dữ liệu
        df['scaled_close'] = (df['close'] - df['close'].mean()) / df['close'].std()
        
        return df