# web
import os
from typing import List
from fastapi import APIRouter
from fastapi import File, UploadFile, HTTPException, Response, Form
from fastapi.responses import FileResponse, JSONResponse
# vml
import cv2
import gc
import numpy as np
from models.ocr_deepseek import ocr_deepseek
from models.vml_gemma import vlm_gemma
from models.vml_llama import vlm_llama
from models.vml_llava import vlm_llava
from models.vml_qwen import vlm_qwen
# util
from python_util import PythonUtil

# 라우터 객체
router = APIRouter()
# html 위치
HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html")

@router.get("/")
async def index():
    return FileResponse(os.path.join(HTML_PATH, "index.html"))

@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204) # 204: 콘텐츠 없음 (성공)

@router.post("/analyze_images")
async def analyze_images(
    model: str = Form("modelSelect"),
    files: List[UploadFile] = File(...)
):
    print(model)
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
                cv2_image = PythonUtil.image_resize(cv2_image, 512)
                cv2_images.append(cv2_image)
        
        # 이미지 확인
        if len(cv2_images) == 0:
            raise HTTPException(status_code=400, detail="읽을 수 있는 이미지 파일이 없습니다.")
        
        # 이미지 분석
        for idx, cv2_image in enumerate(cv2_images):
            if model == "gemma":
                result = vlm_gemma([cv2_image])
            elif model == "llama":
                result = vlm_llama([cv2_image])
            elif model == "llava":
                result = vlm_llava([cv2_image])
            elif model == "qwen":
                result = vlm_qwen([cv2_image])
            elif model == "deepseek":
                result = ocr_deepseek([cv2_image])
            else:
                result = vlm_gemma([cv2_image])
            
            result['idx'] = idx
            results.append(result)
            # 메모리 정리
            gc.collect()
    
    except Exception as e:
        print(f"[Server Error] {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(content={"status": "success", "data": results})