from utils.ollama_client import OllamaClient
import json

class FinancialAnalyst:
    def __init__(self, model="starling-lm:7b"):
        self.client = OllamaClient(model)
        self.prompt_template = """[INST]
        <<SYS>>Bạn là chuyên gia phân tích thị trường crypto. Hãy đánh giá sentiment từ thông tin sau:<</SYS>>
        
        {input_text}  # Đổi tên placeholder
        
        Trả lời theo JSON format:
        {{
            "sentiment_score": -1.0 đến 1.0,
            "key_factors": ["factor1", "factor2"],
            "confidence": 0.0-1.0
        }}
        [/INST]"""

    # Sửa tên tham số thành news_text
    def analyze(self, news_text: str) -> dict:  # Đổi text → news_text
        prompt = self.prompt_template.format(input_text=news_text[:2000])  # Đổi tên biến
        try:
            response = self.client.generate(prompt)
            return json.loads(response)
        except Exception as e:
            print(f"Phân tích thất bại: {str(e)}")
            return {"error": str(e)}