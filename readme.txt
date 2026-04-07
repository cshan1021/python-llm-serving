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
python python_web.py

* 테스트
http://localhost:8090/
http://localhost:8090/docs

* llava
ollama pull llava:7b

* llama
ollama pull llama3.2-vision

* qwen3
ollama pull qwen3-vl:2b

* deepseek
ollama pull deepseek-ocr



비교 항목,추천 모델,Ollama 명령어
Gemma와 가장 유사,Llama 4 (8B),ollama run llama4
코딩 및 한국어 성능,Qwen 2.5/3.5,ollama run qwen2.5
저사양 / 빠른 속도,Phi-4 Mini,ollama run phi4
복잡한 논리 추론,DeepSeek-R1,ollama run deepseek-r1