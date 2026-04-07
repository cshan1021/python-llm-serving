# web
import uvicorn
from fastapi import FastAPI
from python_routes import router as router

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    # 8090 포트로 서버 실행
    uvicorn.run(app, host="0.0.0.0", port=8090)

# 개발자용 - 실행 후 소스 바뀌면 자동 리로드
# uvicorn python_web:app --reload --host 0.0.0.0 --port 8090

# 백그라운드 실행/종료 - 리눅스
# nohup uvicorn python_web:app --host 0.0.0.0 --port 8090 &
# fuser -k 8090/tcp

# 백그라운드 실행/종료 - 윈도우 PowerShell 관리자 권한
# Start-Process python -ArgumentList "-m uvicorn python_web:app --host 0.0.0.0 --port 8090" -WindowStyle Hidden
# Stop-Process -Id (Get-NetTCPConnection -LocalPort 8090).OwningProcess -Force