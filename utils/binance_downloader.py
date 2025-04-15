import pandas as pd
from binance.client import Client
from apscheduler.schedulers.background import BackgroundScheduler
import os
from dotenv import load_dotenv

load_dotenv()

class BinanceDataCollector:
    def __init__(self, symbol='ETHUSDT', interval='30m'):
        self.client = Client(
            api_key=os.getenv('BINANCE_API_KEY'),
            api_secret=os.getenv('BINANCE_API_SECRET')
        )
        self.symbol = symbol
        self.interval = interval
        self.scheduler = BackgroundScheduler()
        
    def fetch_historical_data(self, days=90):
        """Lấy dữ liệu lịch sử 3 tháng"""
        frame = pd.DataFrame(self.client.get_historical_klines(
            symbol=self.symbol,
            interval=self.interval,
            start_str=f"{days} days ago UTC"
        ))
        
        # Xử lý columns
        frame = frame.iloc[:, :6]
        frame.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        frame = frame.astype(float)
        frame['timestamp'] = pd.to_datetime(frame['timestamp'], unit='ms')
        
        return frame

    def save_data(self, df, path='data/raw'):
        """Lưu dữ liệu thành CSV"""
        filename = f"{path}/{self.symbol}_{self.interval}.csv"
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def live_data_update(self):
        """Cập nhật dữ liệu real-time mỗi 30 phút"""
        self.scheduler.add_job(
            self._update_job,
            'interval',
            minutes=30,
            next_run_time=datetime.now()
        )
        self.scheduler.start()

    def _update_job(self):
        new_data = self.fetch_historical_data(days=1)
        existing_data = pd.read_csv(self._current_data_path())
        updated_data = pd.concat([existing_data, new_data]).drop_duplicates()
        self.save_data(updated_data)

    def _current_data_path(self):
        return f"data/raw/{self.symbol}_{self.interval}.csv"