import numpy as np

class PredictionEnsembler:
    def __init__(self, weights=None):
        self.weights = weights or {
            'chronos': 0.6,
            'sentiment': 0.3,
            'technical': 0.1
        }
        
    def apply_technical_bias(self, preds, rsi):
        """Adjust predictions based on RSI"""
        if rsi > 70:
            return preds * 0.98  # Overbought correction
        elif rsi < 30:
            return preds * 1.02  # Oversold bounce
        return preds
        
    def combine(self, chronos_pred, sentiment_score, technical_data):
        base = np.array([p['value'] for p in chronos_pred])
        
        # Apply sentiment
        adjusted = base * (1 + sentiment_score * 0.2)
        
        # Apply technical adjustment
        final = self.apply_technical_bias(adjusted, technical_data['rsi'])
        
        # Add noise
        noise = np.random.normal(0, 0.01, len(final))
        return final * (1 + noise)