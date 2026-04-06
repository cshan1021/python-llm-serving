# web
import uvicorn
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
# vml
import cv2
import numpy as np
from python_gemma import vlm_gemma

app = FastAPI()

@app.get("/")
async def index():
    return FileResponse('index.html')

@app.post("/analyze_images")
async def analyze_images(files: List[UploadFile] = File(...)):
    # 파일 업로드 확인
    if not files or len(files) == 0:
        raise HTTPException(status_code=400, detail="이미지 파일이 전송되지 않았습니다.")
    
    try:
        # 이미지 변환
        # image_full_path = './data/image/1.jpg'
        # cv2_image = cv2.imread(image_full_path)
        cv2_images = []
        for file in files:
            if not file.content_type.startswith("image/"):
                continue
            
            file_bytes = await file.read()
            nparr = np.frombuffer(file_bytes, np.uint8)
            cv2_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if cv2_image is not None:
                cv2_images.append(cv2_image)
        
        # 이미지 확인
        if len(cv2_images) == 0:
            raise HTTPException(status_code=400, detail="읽을 수 있는 이미지 파일이 없습니다.")
        
        # 이미지 분석
        result = vlm_gemma(cv2_images)
    
    except Exception as e:
        print(f"[Server Error] {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return result

if __name__ == "__main__":
    # 8090 포트로 서버 실행
    uvicorn.run(app, host="0.0.0.0", port=8090)