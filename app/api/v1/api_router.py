# web
import logging
from typing import List
from fastapi import APIRouter
from fastapi import File, UploadFile, HTTPException, Response, Form
from fastapi.responses import FileResponse, JSONResponse
# vml
import gc
from model.model_deepseek import model_deepseek
from model.model_gemma import model_gemma
from model.model_internvl import model_internvl
from model.model_llama import model_llama
from model.model_llava import model_llava
from model.model_qwen import model_qwen

# util
from app.core.config import settings
from app.utils.util_image import UtilImage

# 라우터 객체
apiRouter = APIRouter()

@apiRouter.post("/analyze_images")
async def analyze_images(
    model: str = Form(""),
    files: List[UploadFile] = File(...)
):
    logging.info(f"모델 선택: {model}")
    # 파일 업로드 확인
    if not files or len(files) == 0:
        raise HTTPException(status_code=400, detail="이미지 파일이 전송되지 않았습니다.")
    
    results = []
    # 이미지 변환
    base64_images = []
    for file in files:
        if not file.content_type.startswith("image/"):
            continue
        bytes_image = await file.read()
        bytes_image = UtilImage.bytes_resize(bytes_image, 640)
        base64_images.append(UtilImage.bytes_to_base64(bytes_image))
    
    # 이미지 확인
    if len(base64_images) == 0:
        raise HTTPException(status_code=400, detail="읽을 수 있는 이미지 파일이 없습니다.")
    
    # 이미지 분석
    model_map = {
        "deepseek": model_deepseek,
        "gemma": model_gemma,
        "internvl": model_internvl,
        "llama": model_llama,
        "llava": model_llava,
        "qwen": model_qwen,
    }
    model_get = model_map.get(model, model_gemma)
    # 여러개 한번에
    idx = 0
    logging.info(f"분석 시작: {idx}")
    result = model_get(base64_images)
    logging.info(f"분석 종료: {idx}")
    result["idx"] = idx
    results.append(result)
    # 메모리 정리
    gc.collect()
    # 하나씩 여러번
    '''
    for idx, base64_image in enumerate(base64_images):
        logging.info(f"분석 시작: {idx}")
        result = model_get([base64_image])
        logging.info(f"분석 종료: {idx}")
        result["idx"] = idx
        results.append(result)
        # 메모리 정리
        gc.collect()
    '''
    
    return JSONResponse(content={"status": "success", "data": results})