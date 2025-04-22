class Config:
    # Data
    DATA_PATH = './data/raw'
    PROCESSED_PATH = './data/processed'
    
    # Models
    DEFAULT_MODELS = {
        'forecaster': 'chronos:7b',
        'sentiment': 'finllama:7b'
    }
    
    # Trading
    RISK_PARAMS = {
        'max_volatility': 0.05,
        'stop_loss_pct': 0.03
    }
    
    # Visualization
    PLOT_COLORS = {
        'historical': '#1f77b4',
        'forecast': '#ff7f0e'
    }