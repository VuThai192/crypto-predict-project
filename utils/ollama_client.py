import ollama
import time
import json

class OllamaClient:
    def __init__(self, model, max_retries=3):
        self.model = model
        self.max_retries = max_retries
        
    def generate(self, prompt):
        last_error = None  # Thêm biến lưu lỗi cuối cùng
        for _ in range(self.max_retries):
            try:
                response = ollama.generate(
                    model=self.model,
                    prompt=prompt,
                    format='json'
                )
                return response['response']
            except Exception as e:
                last_error = e  # Gán lỗi vào biến
                time.sleep(1)
        # Sử dụng last_error thay vì e
        raise ConnectionError(f"Ollama API failed: {str(last_error)}") 

    def generate_json(self, prompt):
        try:
            response = self.generate(prompt)
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {str(e)}")
        
    # Thêm timeout và retry logic mới
    def generate(self, prompt):
        last_error = None
        for _ in range(self.max_retries):
            try:
                response = ollama.generate(
                    model=self.model,
                    prompt=prompt,
                    format='json',
                    options={'timeout': 120}  # Tăng timeout
                )
                return response['response']
            except Exception as e:
                last_error = e
                time.sleep(2)
        raise ConnectionError(f"Request failed after {self.max_retries} tries. Last error: {str(last_error)}")