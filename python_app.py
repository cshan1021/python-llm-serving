# web
import logging
import uvicorn
import sys
from config import settings
from fastapi import FastAPI
from python_routes import router as router

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(settings.PROJECT_NAME)

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    # 8090 포트로 서버 실행
    uvicorn.run(app, host="0.0.0.0", port=8090)