# web
import uvicorn
from fastapi import FastAPI
from python_routes import router as router

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    # 8090 포트로 서버 실행
    uvicorn.run(app, host="0.0.0.0", port=8090)