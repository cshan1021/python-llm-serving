# web
import os
from typing import List
from fastapi import APIRouter
from fastapi import File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
# vml
import cv2
import gc
import numpy as np
from python_gemma import vlm_gemma
from python_llama import vlm_llama
from python_llava import vlm_llava
from python_qwen import vlm_qwen

# 라우터 객체
router = APIRouter()
# html 위치
HTML_PATH = os.path.dirname(os.path.abspath(__file__))

@router.get("/")
async def index():
    return FileResponse(os.path.join(HTML_PATH, "index.html"))

@router.post("/analyze_images")
async def analyze_images(files: List[UploadFile] = File(...)):
    # 파일 업로드 확인
    if not files or len(files) == 0:
        raise HTTPException(status_code=400, detail="이미지 파일이 전송되지 않았습니다.")
    
    results = []
    try:
        # 이미지 변환
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
        for idx, cv2_image in enumerate(cv2_images):
            
            # result = vlm_gemma([cv2_image])
            # result = vlm_llama([cv2_image])
            # result = vlm_llava([cv2_image])
            result = vlm_qwen([cv2_image])
            
            result['idx'] = idx
            results.append(result)
            # 메모리 정리
            gc.collect()
    
    except Exception as e:
        print(f"[Server Error] {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(content={"status": "success", "data": results})