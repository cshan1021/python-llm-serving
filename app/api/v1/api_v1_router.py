# web
import gc
import logging
from fastapi import APIRouter
from fastapi import File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import List
# serving
from serving import serving_ollama
from serving import serving_openai
# util
from app.utils import util_image

# 라우터 객체
api_v1_router = APIRouter()

@api_v1_router.post("/analyze_images")
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
        bytes_image = util_image.bytes_resize(bytes_image, 640)
        base64_images.append(util_image.bytes_to_base64(bytes_image))
    
    # 이미지 확인
    if len(base64_images) == 0:
        raise HTTPException(status_code=400, detail="읽을 수 있는 이미지 파일이 없습니다.")
    
    # 이미지 분석 - 여러개 한번에
    idx = 0
    logging.info(f"분석 시작: {idx}")

    result = await serving_ollama.text_completion(model, base64_images)
    # result = await serving_ollama.chat_completion(model, base64_images)
    # result = await serving_openai.chat_completion(model, base64_images)

    logging.info(f"분석 종료: {idx}")
    result["idx"] = idx
    results.append(result)

    # 메모리 정리
    gc.collect()
    
    return JSONResponse(content={"status": "success", "data": results})