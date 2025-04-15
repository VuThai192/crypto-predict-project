import json
from utils.ollama_client import OllamaClient

class ChronosForecaster:
    def __init__(self, model="chronos:13b"):
        self.client = OllamaClient(model)
        self.prompt_template = """[INST]
        As a crypto price forecasting model, analyze the following OHLCV data 
        and predict next 48 timesteps (30m interval). 
        Use CSV format for input and return JSON format.
        
        Input:
        {input_data}
        
        Output format:
        {{
            "predictions": [
                {{
                    "timestamp": "YYYY-MM-DD HH:MM:SS",
                    "value": float,
                    "confidence": 0.0-1.0
                }}
            ]
        }}
        [/INST]"""
        
    def format_input(self, df):
        return df[['open','high','low','close','volume']].to_csv()
        
    def predict(self, df):
        prompt = self.prompt_template.format(
            input_data=self.format_input(df))
        response = self.client.generate(prompt)
        return json.loads(response)