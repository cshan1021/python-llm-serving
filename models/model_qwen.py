import ollama
from app.core.config import settings
from app.utils import util_image

# 설명 중심의 모델
prompt = '''
    이 이미지에서 모든 텍스트를 누락 없이 전부 추출해.
    요약내용(summary)과 전체내용(content)을 구분해서 json 형태로 출력해.
    [출력 예시]
    {
        "summary": "한글 요약내용",
        "content": "원문 전체내용"
    }
'''

def model_qwen(base64_images):
    try:
        response = ollama.chat(
            model ='qwen3.5:2b',
            messages = [{
                'role': 'user',
                'content': prompt,
                'images': base64_images,
            }],
            keep_alive = settings.MODEL_KEEP_ALIVE,
            options = settings.MODEL_OPTIONS
        )
        return util_image.ollama_to_json(response)
    
    except Exception as e:
        print(f"[분석 에러] {e}")
        return {}
