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

* InternVL
ollama pull blaifa/InternVL3_5:8b

* 구조화 - [아래의 내용을 번역하지 말고 그대로 json으로 만들어.]
deepseek-r1 구조화
ollama pull qwen2.5-coder:7b 구조화

* 실행 - 개발자용 - 실행 후 소스 바뀌면 자동 리로드
uvicorn python_web:app --reload --host 0.0.0.0 --port 8090

* 실행 - 백그라운드 실행/종료 - 리눅스
nohup uvicorn python_web:app --host 0.0.0.0 --port 8090 &
fuser -k 8090/tcp

* 실행 - 백그라운드 실행/종료 - 윈도우 PowerShell 관리자 권한
Start-Process python -ArgumentList "-m uvicorn python_web:app --host 0.0.0.0 --port 8090" -WindowStyle Hidden
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8090).OwningProcess -Force