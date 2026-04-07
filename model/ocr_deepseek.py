import json
import ollama
from datetime import datetime

# OCR 모델 - base64 형식 안됨
prompt = '''
    <image>\nFree OCR.
'''
# <image>\nFree OCR. Extract all text into JSON: {"summary":"", "content":""}

def ocr_deepseek(base64_images):
    try:
        print(f"분석 시작: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
        response = ollama.chat(
            model='deepseek-ocr',
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': ["./data/image/1.jpg"],
            }],
            # 0: 즉시 해제, 3600: 1시간 유지, -1: 무한 유지 (기본값은 5분)
            keep_alive=0
        )
        print(f"분석 종료: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")

        content = response['message']['content']
        # ocr 모델이라 내용만 있음
        content =     {
            "summary": "",
            "content": content
        }
        return content
    
    except Exception as e:
        print(f"[분석 에러] {e}")
        return {}