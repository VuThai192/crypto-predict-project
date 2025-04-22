import json
from datetime import datetime
from config.settings import Config
from utils.data_loader import DataProcessor
from models.mistral_forecaster import MistralForecaster
from models.finance_analyst import FinancialAnalyst
from models.ensemble import PredictionEnsembler
from utils.plotter import ForecastVisualizer
from utils.binance_downloader import BinanceDataCollector

def main(args):
    # Khởi tạo data collector
    collector = BinanceDataCollector()
    
    if args.mode == 'live':
        print("Starting live data collection...")
        collector.live_data_update()
    else:
        # Chế độ batch
        raw_data = collector.fetch_historical_data()
        collector.save_data(raw_data)
        
    # Xử lý dữ liệu
  
    
    # Initialize components
    processor = DataProcessor('ETHUSDT')
    forecaster = MistralForecaster()
    analyst = FinancialAnalyst()
    ensembler = PredictionEnsembler()
    visualizer = ForecastVisualizer()
    
    # Load and process data
    df = processor.get_latest_data()
    
    # Generate predictions
    # chronos_pred = forecaster.predict(df)
    processed_data = processor.load_and_preprocess()
    predictions = forecaster.predict(processed_data)  # Đã có format_input
    
    sentiment = analyst.analyze(news_text="Tin tức mới nhất về ETF Bitcoin...")
    
    # Kết hợp sentiment vào dự báo
    # adjusted_pred = predictions * (1 + sentiment.get('sentiment_score', 0) * 0.15)
    
    # Sửa phần kết hợp dự báo
    if predictions and isinstance(predictions, list):
        sentiment_score = sentiment.get("sentiment_score", 0)
        adjusted_pred = [p * (1 + sentiment_score * 0.15) for p in predictions]
    else:
        print("Không có dự báo hợp lệ")
        adjusted_pred = []
    print(f"processed_data: {processed_data}")
    
    final_pred = ensembler.combine(
        adjusted_pred,
        sentiment.get('sentiment_score', 0),
        {'rsi': processed_data['rsi'].iloc[-1].item()}  # Thêm .item()
    )
    
    # Generate plot
    fig = visualizer.create_plot(
        history_df=processed_data,
        predictions=final_pred,
        future_steps=48,
        interval_minutes=30
    )
    fig.write_html("data/forecasts/forecast.html")
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['live', 'batch'], default='batch')
    args = parser.parse_args()
    main(args)