import httpx
import json
import logging
from app.core.config import settings

prompt = """
    이 이미지에서 모든 텍스트를 누락 없이 전부 추출해.
    요약내용(summary)과 전체내용(content)을 구분해서 json 형태로 출력해.
    [출력 예시]
    {
        "summary": "한글 요약내용",
        "content": "원문 전체내용(Raw Text Compilation)"
    }
"""

async def model_availability(model):
    try:
        tags_url = f"{settings.OLLAMA_ENDPOINT}/api/tags"

        async with httpx.AsyncClient() as client:
            response = await client.get(tags_url, timeout=5.0)
            if response.status_code == 200:
                models_data = response.json().get("models", [])
                # 모델 이름 목록 추출 (예: 'llama3:latest')
                available_models = [m.get("name") for m in models_data]
                
                if model in available_models:
                    logging.info(f"Ollama 모델 '{model}' 사용 가능 확인.")
                    return True
                logging.warning(f"Ollama 모델 '{model}'이 존재하지 않습니다. 사용 가능 목록: {available_models}")
            else:
                logging.error(f"Ollama 서버 상태 비정상 (HTTP {response.status_code})")
    except Exception as e:
        logging.error(f"Ollama 서버 연결 또는 모델 확인 중 오류 발생: {str(e)}")
    return False

async def text_completion(model, base64_images):
    if not await model_availability(model):
        return {}

    payload = {
        "model": model,
        "prompt": prompt,
        "images": base64_images,
        "stream": False
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{settings.OLLAMA_ENDPOINT}/api/generate", json=payload, timeout=600.0)
            response = response.json()
            return get_content(response)
        except Exception as e:
            logging.error(f"오류: {str(e)}")
            return {}

async def chat_completion(model, base64_images):
    if not await model_availability(model):
        return {}

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
            response = await client.post(f"{settings.OLLAMA_ENDPOINT}/api/chat", json=payload, timeout=600.0)
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