# web
import gc
import logging
from app.core.config import settings
from fastapi import APIRouter
from fastapi import Form, File, UploadFile, Request, HTTPException
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
    servingSelect: str = Form(""),
    modelSelect: str = Form(""),
    files: List[UploadFile] = File(...)
):
    logging.info(f"서빙 선택: {servingSelect}")
    logging.info(f"모델 선택: {modelSelect}")
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

    prompt = """
        이 이미지에서 모든 텍스트를 누락 없이 전부 추출해.
        요약내용(summary)과 전체내용(content)을 구분해서 json 형태로 출력해.
        [출력 예시]
        {
            "summary": "한글 요약내용",
            "content": "원문 전체내용(Raw Text Compilation)"
        }
    """
    if "ollama" == servingSelect:
        result = await serving_ollama.text_completion(settings.OLLAMA_ENDPOINT, settings.OLLAMA_API_KEY, modelSelect, prompt, base64_images)
        # result = await serving_ollama.chat_completion(modelSelect, base64_images)
    elif "openai" == servingSelect:
        result = await serving_openai.chat_completion(settings.OPENAI_ENDPOINT, settings.OPENAI_API_KEY, modelSelect, prompt, base64_images)

    logging.info(f"분석 종료: {idx}")
    result["idx"] = idx
    results.append(result)

    # 메모리 정리
    gc.collect()
    
    return JSONResponse(content={"status": "success", "data": results})

@api_v1_router.post("/proxy")
async def proxy(request: Request):
    result = await serving_ollama.text_completion("http://localhost:11434", settings.OLLAMA_API_KEY, "gemma4:e2b", "안녕", [])
    return JSONResponse(result)