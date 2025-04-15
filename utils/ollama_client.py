import ollama
import time

class OllamaClient:
    def __init__(self, model, max_retries=3):
        self.model = model
        self.max_retries = max_retries
        
    def generate(self, prompt):
        for _ in range(self.max_retries):
            try:
                response = ollama.generate(
                    model=self.model,
                    prompt=prompt,
                    format='json'
                )
                return response['response']
            except Exception as e:
                time.sleep(1)
        raise ConnectionError("Ollama API failed")
        
    def generate_json(self, prompt):
        response = self.generate(prompt)
        return json.loads(response)