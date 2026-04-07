# web
import os
from typing import List
from fastapi import APIRouter
from fastapi import File, UploadFile, HTTPException, Response, Form
from fastapi.responses import FileResponse, JSONResponse
# vml
import gc
from model.ocr_deepseek import ocr_deepseek
from model.vml_gemma import vlm_gemma
from model.vml_llama import vlm_llama
from model.vml_llava import vlm_llava
from model.vml_qwen import vlm_qwen
# util
from python_util import PythonUtil

# 라우터 객체
router = APIRouter()
# html 위치
HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html")

@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@router.get("/")
async def index():
    return FileResponse(os.path.join(HTML_PATH, "index.html"))

@router.post("/analyze_images")
async def analyze_images(
    model: str = Form(""),
    files: List[UploadFile] = File(...)
):
    print(f"model: {model}")
    # 파일 업로드 확인
    if not files or len(files) == 0:
        raise HTTPException(status_code=400, detail="이미지 파일이 전송되지 않았습니다.")
    
    results = []
    try:
        # 이미지 변환
        base64_images = []
        for file in files:
            if not file.content_type.startswith("image/"):
                continue
            bytes_image = await file.read()
            base64_images.append(PythonUtil.bytes_to_base64(bytes_image, 512))
        
        # 이미지 확인
        if len(base64_images) == 0:
            raise HTTPException(status_code=400, detail="읽을 수 있는 이미지 파일이 없습니다.")
        
        # 이미지 분석 - 하나씩 따로 분석
        model_map = {
            "gemma": vlm_gemma,
            "llama": vlm_llama,
            "llava": vlm_llava,
            "qwen": vlm_qwen,
            "deepseek": ocr_deepseek
        }
        model_get = model_map.get(model, vlm_gemma)

        for idx, base64_image in enumerate(base64_images):
            result = model_get([base64_image])
            result['idx'] = idx
            results.append(result)
            # 메모리 정리
            gc.collect()
    
    except Exception as e:
        print(f"[Server Error] {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(content={"status": "success", "data": results})