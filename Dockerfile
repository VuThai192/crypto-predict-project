FROM python:3.10-slim

WORKDIR /app

# 1. Cài đặt system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# 2. Cài đặt Ollama
RUN curl -L https://ollama.ai/install.sh | sh

# 3. Copy source code
COPY . .

# 4. Cài đặt Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Tạo thư mục và script khởi tạo thông minh
RUN mkdir -p /root/.ollama && \
    echo '#!/bin/bash\n\
    timeout 120 bash -c "until nc -z 127.0.0.1 11434; do sleep 2; done"\n\
    declare -a models=("codellama:7b" "mistral:7b-instruct" "starling-lm:7b")\n\
    for model in "${models[@]}"; do\n\
        echo "Checking for $model..."\n\
        if ollama list | grep -q "$model"; then\n\
            echo "✓ $model already exists"\n\
        else\n\
            echo "⏳ Pulling $model..."\n\
            ollama pull "$model" || echo "⚠️ Failed to pull $model"\n\
        fi\n\
    done\n\
    echo "Starting application..."\n\
    python main.py' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

EXPOSE 11434

CMD ["sh", "-c", "ollama serve & /app/entrypoint.sh"]