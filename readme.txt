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

* gemma4 vl 모델 다운로드
ollama pull gemma4:e2b

* FastAPI - 웹서비스
python -m pip install fastapi uvicorn python-multipart
python -m pip install opencv-python
python -m pip install pydantic-settings
python python_web.py

* 테스트
http://localhost:8090/
http://localhost:8090/docs

* llava
ollama pull llava:7b

* llama
ollama pull llama3.2-vision

* qwen3
ollama pull qwen3.5:2b

* deepseek
ollama pull deepseek-ocr