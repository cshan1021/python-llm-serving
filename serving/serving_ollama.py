import httpx
import json
import logging

async def model_availability(api_url, model_name):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{api_url}/api/tags", timeout=5.0)
            if response.status_code == 200:
                models_data = response.json().get("models", [])
                available_models = [m.get("name") for m in models_data]
                # 모델 ID 목록 추출 및 비교
                if model_name in available_models:
                    logging.info(f"Ollama 모델 '{model_name}' 사용 가능 확인.")
                    return True
                logging.warning(f"Ollama 모델 '{model_name}'이 존재하지 않습니다. 사용 가능 목록: {available_models}")
            else:
                logging.error(f"Ollama 서버 상태 비정상 (HTTP {response.status_code})")
    except Exception as e:
        logging.error(f"Ollama 서버 연결 또는 모델 확인 중 오류 발생: {str(e)}")
    return False

async def text_completion(api_url, api_key, model_name, prompt, base64_images):
    if not await model_availability(api_url, model_name):
        return {}
    
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {"model": model_name, "prompt": prompt, "stream": False}
    if base64_images and len(base64_images) > 0:
        payload["images"] = base64_images
        
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{api_url}/api/generate", headers=headers, json=payload, timeout=300.0)
            response = response.json()
            return get_content(response)
        except Exception as e:
            logging.error(f"오류: {str(e)}")
            return {}

async def chat_completion(api_url, api_key, model_name, prompt, base64_images):
    if not await model_availability(api_url, model_name):
        return {}

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    message = {"role": "user", "content": prompt}
    if base64_images and len(base64_images) > 0:
        message["images"] = base64_images
    payload = {"model": model_name, "messages": [message], "stream": False}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{api_url}/api/chat", headers=headers, json=payload, timeout=300.0)
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