import base64
import cv2
import json
import ollama

# OCR 모델 - base64 형식 안됨
prompt_text = '''
    <image>\nFree OCR.
'''
# <image>\nFree OCR. Extract all text into JSON: {"summary":"", "content":""}

def ocr_deepseek(cv2_images):
    prompt_images = []
    for cv2_image in cv2_images:
        _, buffer = cv2.imencode('.jpg', cv2_image)
        prompt_images.append(base64.b64encode(buffer).decode('utf-8'))
    
    if not prompt_images:
        print("유효하게 인코딩된 이미지가 0개입니다.")
        return {}

    try:
        response = ollama.chat(
            model='deepseek-ocr',
            messages=[{
                'role': 'user',
                'content': prompt_text,
                'images': ["./data/image/1.jpg"],
            }],
            # 0: 즉시 해제, 3600: 1시간 유지, -1: 무한 유지 (기본값은 5분)
            keep_alive=0
        )

        content = response['message']['content']
        print(content)
        # ocr 모델이라 내용만 있음
        content =     {
            "summary": "",
            "content": content
        }
        return content
    
    except Exception as e:
        print(f"[분석 에러] {e}")
        return {}