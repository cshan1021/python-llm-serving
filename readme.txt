* 프로젝트 생성
git init -b main
git remote add origin https://github.com/cshan1021/python-llm-serving
git pull origin main

* venv 환경 - Python 3.14.4
python -m venv .venv 또는 py -m venv .venv
.\.venv\Scripts\activate

* 웹서비스 - fastapi
python -m pip install fastapi uvicorn python-multipart
python -m pip install pydantic-settings
python -m pip install tldextract
python -m pip install httpx
python -m pip install jinja2

* 이미지
python -m pip install opencv-python

* ollama 설치
윈도우는 https://ollama.com/download/windows

* ollama 모델 다운로드
ollama pull gemma4:e4b
ollama pull qwen3.5:4b
ollama pull llama3.2-vision:11b
ollama pull llava:7b

* 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8090

* llm serving frameworks
llama.cpp
ollama
LM Studio
LocalAI

* llama.cpp - v3 검사 예외 설정 필요 - data/llamacpp bat 파일 참고
https://github.com/ggml-org/llama.cpp/releases
Windows x64 (CPU)
Windows x64 (CUDA 12) - CUDA 12.4 DLLs
cudart-llama-bin-win-cuda-12.4-x64.zip

* gguf 모델
https://huggingface.co/lmstudio-community/gemma-4-E4B-it-GGUF/tree/main
gemma-4-E4B-it-Q4_K_M.gguf
mmproj-gemma-4-E4B-it-BF16.gguf

https://huggingface.co/lmstudio-community/Qwen3.5-4B-GGUF/tree/main
Qwen3.5-4B-Q4_K_M.gguf
mmproj-Qwen3.5-4B-BF16.gguf
