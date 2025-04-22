import numpy as np

class PredictionEnsembler:
    def __init__(self, weights=None):
        self.weights = weights or {
            'chronos': 0.6,
            'sentiment': 0.3,
            'technical': 0.1
        }
        
    def apply_technical_bias(self, preds, rsi_value):
        """Điều chỉnh dự báo dựa trên RSI"""
        # Chuyển đổi thành giá trị số nếu là pandas object
        if hasattr(rsi_value, 'item'):
            rsi = rsi_value.item()
        else:
            rsi = float(rsi_value)
            
        if rsi > 70:
            return preds * 0.98
        elif rsi < 30:
            return preds * 1.02
        return preds
        
    def combine(self, chronos_pred, sentiment_score, technical_data):
        base = np.array(chronos_pred)
        
        # Áp dụng sentiment
        adjusted = base * (1 + sentiment_score * 0.2)
        
        # Lấy giá trị RSI cuối cùng
        rsi_value = technical_data['rsi']
        
        # Áp dụng hiệu chỉnh kỹ thuật
        final = self.apply_technical_bias(adjusted, rsi_value)
        
        # Thêm nhiễu ngẫu nhiên
        noise = np.random.normal(0, 0.01, len(final))
        return final * (1 + noise)