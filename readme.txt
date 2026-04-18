* 프로젝트 생성
git init -b main
git remote add origin https://github.com/cshan1021/python-ollama
git pull origin main

* venv 환경 - Python 3.14.0
python -m venv .venv 또는 py -m venv .venv
.\.venv\Scripts\activate

* ollama 설치 - ollama version is 0.20.2
윈도우는 https://ollama.com/download/windows

* ollama 라이브러리
python -m pip install ollama

* gemma4 모델 다운로드
ollama pull gemma4:e4b

* 웹서비스 - fastapi
python -m pip install fastapi uvicorn python-multipart
python -m pip install pydantic-settings
python -m pip install tldextract
python -m pip install httpx
python -m pip install jinja2

* 이미지
python -m pip install opencv-python

* 모델
ollama pull llava:7b
ollama pull llama3.2-vision
ollama pull qwen3.5:2b
ollama pull deepseek-ocr
ollama pull blaifa/InternVL3_5:8b

* 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8090

* 테스트
http://localhost:8090/
http://localhost:8090/docs


* llm serving
ollama
LM Studio
llama.cpp
ramalama
koboldcpp
Jan AI
Text Generation Web UI
LoLLMs

* lm-studio
https://lmstudio.ai/

* llama.cpp
https://github.com/ggml-org/llama.cpp/releases
Windows x64 (CPU)
Windows x64 (CUDA 12) - CUDA 12.4 DLLs
cudart-llama-bin-win-cuda-12.4-x64.zip

* gemma-4 gguf 모델
https://huggingface.co/bartowski/google_gemma-4-E4B-it-GGUF/tree/main
google_gemma-4-E4B-it-Q4_K_M.gguf
mmproj-google_gemma-4-E4B-it-bf16.gguf