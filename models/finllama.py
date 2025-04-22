from utils.ollama_client import OllamaClient 

class FinLlamaAnalyzer:
    def __init__(self, model="finllama:7b"):
        self.client = OllamaClient(model)
        self.news_template = """[INST]
        Analyze crypto market sentiment from recent news (max 20 words).
        Return JSON with sentiment_score (-1 to 1) and key_terms.
        
        News: {news_text}
        
        Example response:
        {{
            "sentiment_score": 0.75,
            "key_terms": ["ETF approval", "Fed rate cut"]
        }}
        [/INST]"""
        
    def analyze_news(self, news_text):
        prompt = self.news_template.format(news_text=news_text[:1000])
        return self.client.generate_json(prompt)