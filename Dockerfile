FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Ollama
RUN curl -L https://ollama.ai/download/ollama-linux-amd64 -o /usr/bin/ollama \
    && chmod +x /usr/bin/ollama

# Thêm environment variables
ENV BINANCE_API_KEY=${BINANCE_API_KEY}
ENV BINANCE_API_SECRET=${BINANCE_API_SECRET}

# Thêm volume lưu data
VOLUME ["/app/data"]

# Copy project files
COPY . .

# Expose Ollama port
EXPOSE 11434

# Start Ollama and run application
CMD ollama serve & sleep 10 && ollama pull chronos:13b && python main.py