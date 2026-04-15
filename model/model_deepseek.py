import ollama
from config import settings
from datetime import datetime

# OCR 모델
prompt = '''
    <image>\nFree OCR.
'''
# <image>\nFree OCR. Extract all text into JSON: {"summary":"", "content":""}

def model_deepseek(base64_images):
    try:
        response = ollama.chat(
            model = 'deepseek-ocr',
            messages = [{
                'role': 'user',
                'content': prompt,
                'images': base64_images,
            }],
            keep_alive = settings.MODEL_KEEP_ALIVE,
            options = settings.MODEL_OPTIONS
        )
        content = response['message']['content']
        # ocr 모델이라 내용만 있음
        return {"summary": "", "content": content}
    
    except Exception as e:
        print(f"[분석 에러] {e}")
        return {}
