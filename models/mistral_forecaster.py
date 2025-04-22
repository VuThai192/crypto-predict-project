from utils.ollama_client import OllamaClient
import pandas as pd
import json

class MistralForecaster:
    def __init__(self, model="mistral:7b-instruct"):
        self.client = OllamaClient(model)
        self.prompt_template = """[INST]
        You are a financial forecasting expert. Analyze this cryptocurrency data:
        {input_data}
        
        Predict next 48 time steps (30m interval). Use JSON format:
        {{"predictions": [{{"timestamp": "YYYY-MM-DD HH:MM:SS", "value": float}}]}}
        [/INST]"""

    # Thêm phương thức format_input
    def format_input(self, df: pd.DataFrame) -> str:
        """Chuẩn bị dữ liệu đầu vào cho model"""
        return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']].to_csv(index=False)

    def predict(self, df):
        prompt = self.prompt_template.format(
            input_data=self.format_input(df.tail(100)))
        
        try:
            response = self.client.generate(prompt)
            parsed = self._parse_response(response)
            # Trích xuất mảng giá trị số từ JSON
            return [p["value"] for p in parsed["predictions"]]  # Thêm dòng này
        except Exception as e:
            print(f"Lỗi dự báo: {str(e)}")
            return []

    def _parse_response(self, response: str) -> dict:
        try:
            data = json.loads(response)
            # Validate response structure
            if "predictions" not in data:
                raise ValueError("Invalid response format")
            for p in data["predictions"]:
                if "value" not in p:
                    raise ValueError("Missing 'value' in predictions")
            return data
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response")