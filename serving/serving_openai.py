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

async def check_model_availability(model):
    """
    OpenAI API 서버 상태와 요청된 모델의 존재 여부를 확인합니다.
    """
    try:
        models_url = f"{settings.OPENAI_ENDPOINT}/v1/models"

        async with httpx.AsyncClient() as client:
            response = await client.get(models_url, timeout=5.0)
            if response.status_code == 200:
                models_data = response.json().get("data", [])
                # 모델 ID 목록 추출 및 비교
                available_models = [m.get("id") for m in models_data if isinstance(m, dict)]
                if model in available_models:
                    logging.info(f"모델 '{model}' 사용 가능 확인.")
                    return True
                logging.warning(f"모델 '{model}'이 서버에 존재하지 않습니다. 사용 가능 목록: {available_models}")
            else:
                logging.error(f"API 서버 상태 비정상 (HTTP {response.status_code})")
    except Exception as e:
        logging.error(f"API 서버 연결 또는 모델 확인 중 오류 발생: {str(e)}")
    return False

async def text_completion(model):
    if not await check_model_availability(model):
        return {}

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{settings.OPENAI_ENDPOINT}/v1/completions", json=payload, timeout=600.0)
            response = response.json()
            return get_content(response)
        except Exception as e:
            logging.error(f"오류: {str(e)}")
            return {}

async def chat_completion(model, base64_images):
    if not await check_model_availability(model):
        return {}

    payload = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                *[
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image}"}
                    } for image in base64_images
                ]
            ]
        }],
        "stream": False
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{settings.OPENAI_ENDPOINT}/v1/chat/completions", json=payload, timeout=600.0)
            response = response.json()
            return get_content(response)
        except Exception as e:
            logging.error(f"오류: {str(e)}")
            return {}

def get_content(response):
    if "text" in response:
        logging.info("OpenAI Text API입니다.")
        content = response["text"]
    elif "choices" in response:
        logging.info("OpenAI Chat API입니다.")
        content = response["choices"][0]["message"]["content"]

    content = content.replace("```json", "").replace("```", "").strip()
    return json.loads(content)