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

* 구조화 예정 - [아래의 내용을 번역하지 말고 그대로 json으로 만들어.]
ollama pull qwen2.5-coder:7b 구조화