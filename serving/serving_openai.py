import httpx
import json
import logging

async def model_availability(api_url, model_name):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{api_url}/v1/models", timeout=5.0)
            if response.status_code == 200:
                models_data = response.json().get("data", [])
                # 모델 ID 목록 추출 및 비교
                available_models = [m.get("id") for m in models_data if isinstance(m, dict)]
                if model_name in available_models:
                    logging.info(f"모델 '{model_name}' 사용 가능 확인.")
                    return True
                logging.warning(f"모델 '{model_name}'이 서버에 존재하지 않습니다. 사용 가능 목록: {available_models}")
            else:
                logging.error(f"API 서버 상태 비정상 (HTTP {response.status_code})")
    except Exception as e:
        logging.error(f"API 서버 연결 또는 모델 확인 중 오류 발생: {str(e)}")
    return False

async def text_completion(api_url, api_key, model_name, prompt):
    # 모델명 확인 안함
    # if not await model_availability(api_url, model_name):
    #    return {}

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {"model": model_name, "prompt": prompt, "stream": False}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{api_url}/v1/completions", headers=headers, json=payload, timeout=300.0)
            response = response.json()
            return get_content(response)
        except Exception as e:
            logging.error(f"오류: {str(e)}")
            return {}

async def chat_completion(api_url, api_key, model_name, prompt, base64_images):
    # 모델명 확인 안함
    # if not await model_availability(api_url, model_name):
    #    return {}

    headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
    }
    payload = {
        "model": model_name,
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
            response = await client.post(f"{api_url}/v1/chat/completions", headers=headers, json=payload, timeout=300.0)
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