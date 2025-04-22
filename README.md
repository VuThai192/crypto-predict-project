# crypto-predict-prokect

docker build -t crypto-predict-prokect .

docker run -p 11434:11434 crypto-predict-prokect

docker exec -it 2933c9099a6fc395a67186500d16a6da94d8b4d88b2e73f102869dbc140b64cd sh

docker build -t crypto-predict-project --build-arg BINANCE_API_KEY=MTYPqvjaGuAJr5O4g5QnMT6xz1xasPBUV9fw7ul6xkftv11fn8I0RlnXZlTJ03L3 --build-arg BINANCE_API_SECRET=eLWzr5ma9vJLCBgDLzvgdNDJFPWNAVAZPMQrTFlmPZt1ZCh5qUoI16nhNq34V2Zp .

docker run -p 11434:11434 -v ollama_data:/root/.ollama crypto-predict-project

docker exec -it 7c9f7101e6c2 ollama list

docker build -t crypto-predict-project .
docker run -it --gpus all -p 11434:11434 -v "$(pwd):/app" -e BINANCE_API_KEY="MTYPqvjaGuAJr5O4g5QnMT6xz1xasPBUV9fw7ul6xkftv11fn8I0RlnXZlTJ03L3" -e BINANCE_API_SECRET="eLWzr5ma9vJLCBgDLzvgdNDJFPWNAVAZPMQrTFlmPZt1ZCh5qUoI16nhNq34V2Zp" crypto-predict-project

 && \
    ollama pull chronos:7b-instruct-q4_0 && \
    ollama pull finllama:7b

docker exec 2933c9099a6fc395a67186500d16a6da94d8b4d88b2e73f102869dbc140b64cd ollama list
docker compose restart crypto-predict-prokect