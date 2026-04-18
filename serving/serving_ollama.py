import httpx
import json
import logging
from app.core.config import settings

# 구조화 중심의 모델
prompt = """
    이 이미지에서 모든 텍스트를 누락 없이 전부 추출해.
    요약내용(summary)과 전체내용(content)을 구분해서 json 형태로 출력해.
    [출력 예시]
    {
        "summary": "한글 요약내용",
        "content": "원문 전체내용(Raw Text Compilation)"
    }
"""

async def text_completion(model, base64_images):
    payload = {
        "model": model,
        "prompt": prompt,
        "images": base64_images,
        "stream": False
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(settings.OLLAMA_TEXT_ENDPOINT, json=payload, timeout=600.0)
            response = response.json()
            return get_content(response)
        except Exception as e:
            logging.error(f"오류: {str(e)}")
            return {}

async def chat_completion(model, base64_images):
    payload = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": prompt,
            "images": base64_images,
        }],
        "stream": False
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(settings.OLLAMA_CHAT_ENDPOINT, json=payload, timeout=600.0)
            response = response.json()
            return get_content(response)
        except Exception as e:
            logging.error(f"오류: {str(e)}")
            return {}

def get_content(response):
    if "response" in response:
        logging.info("Ollama Text API입니다.")
        content = response["response"]
    elif "message" in response:
        logging.info("Ollama Chat API입니다.")
        content = response["message"]["content"]
    content = content.replace("```json", "").replace("```", "").strip()
    return json.loads(content)