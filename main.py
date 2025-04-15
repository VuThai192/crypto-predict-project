import json
from datetime import datetime
from config.settings import Config
from utils.data_loader import DataProcessor
from models.chronos import ChronosForecaster
from models.finllama import FinLlamaAnalyzer
from models.ensemble import PredictionEnsembler
from utils.plotter import ForecastVisualizer
from utils.binance_loader import BinanceDataCollector

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
    processor = DataProcessor()
    df = processor.get_latest_data()
    
    # Initialize components
    processor = DataProcessor()
    forecaster = ChronosForecaster()
    analyzer = FinLlamaAnalyzer()
    ensembler = PredictionEnsembler()
    visualizer = ForecastVisualizer()
    
    # Load and process data
    df = processor.load_data(f"{Config.DATA_PATH}/eth.csv")
    processed_df = processor.add_features(df)
    
    # Generate predictions
    chronos_pred = forecaster.predict(processed_df)
    sentiment = analyzer.analyze_news("Latest crypto news...")
    
    # Combine predictions
    final_pred = ensembler.combine(
        chronos_pred,
        sentiment['sentiment_score'],
        {'rsi': processed_df['momentum_rsi'][-1]}
    )
    
    # Generate plot
    fig = visualizer.create_plot(df, final_pred)
    fig.write_html("./forecast.html")
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['live', 'batch'], default='batch')
    args = parser.parse_args()
    main(args)